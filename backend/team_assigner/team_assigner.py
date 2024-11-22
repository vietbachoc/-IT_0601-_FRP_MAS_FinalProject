import logging
import torch
import umap
import cv2
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Optional, Tuple
from transformers import AutoProcessor, SiglipVisionModel

from .constants import (
    SIGLIP_MODEL_NAME, 
    BATCH_SIZE, 
    IMAGE_SIZE,
    UMAP_CONFIG,
    TEAM_COLORS,
    MIN_PLAYERS
)

logger = logging.getLogger(__name__)

class TeamClassifier:
    """Classifies players into teams using computer vision and clustering"""
    
    def __init__(self, device: str = 'cpu'):
        """
        Initialize team classifier
        Args:
            device: Computing device ('cpu', 'cuda', or 'mps')
        """
        self.device = device
        self.batch_size = BATCH_SIZE
        self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize vision and clustering models"""
        try:
            self.model = SiglipVisionModel.from_pretrained(SIGLIP_MODEL_NAME).to(self.device)
            self.processor = AutoProcessor.from_pretrained(SIGLIP_MODEL_NAME)
            self.reducer = umap.UMAP(**UMAP_CONFIG)
            self.kmeans = KMeans(n_clusters=2, random_state=42)
        except Exception as e:
            logger.error(f"Model initialization failed: {str(e)}")
            raise

    def _create_batches(self, crops: List[np.ndarray]) -> List[List[np.ndarray]]:
        """Create batches of images for processing"""
        return [crops[i:i + self.batch_size] for i in range(0, len(crops), self.batch_size)]

    def _extract_features(self, crops: List[np.ndarray]) -> np.ndarray:
        """Extract features from player crops using vision model"""
        try:
            features = []
            crops = [cv2.cvtColor(crop, cv2.COLOR_BGR2RGB) for crop in crops]
            
            with torch.no_grad():
                for batch in self._create_batches(crops):
                    inputs = self.processor(images=batch, return_tensors="pt").to(self.device)
                    outputs = self.model(**inputs)
                    batch_features = torch.mean(outputs.last_hidden_state, dim=1)
                    features.append(batch_features.cpu().numpy())
                    
            return np.concatenate(features)
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise

    def _get_player_crop(self, frame: np.ndarray, bbox: List[float]) -> Optional[np.ndarray]:
        """Extract and resize player crop from frame"""
        try:
            y1, y2 = max(int(bbox[1]), 0), min(int(bbox[3]), frame.shape[0])
            x1, x2 = max(int(bbox[0]), 0), min(int(bbox[2]), frame.shape[1])
            
            if y2 <= y1 or x2 <= x1:
                return None
                
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                return None
                
            return cv2.resize(crop, (IMAGE_SIZE, IMAGE_SIZE))
        except Exception as e:
            logger.error(f"Crop extraction failed: {str(e)}")
            return None

    def fit(self, frame: np.ndarray, player_detections: Dict) -> None:
        """Fit the classifier on current frame's player detections"""
        try:
            crops = []
            for _, player in player_detections.items():
                crop = self._get_player_crop(frame, player["bbox"])
                if crop is not None:
                    crops.append(crop)
            
            if len(crops) < MIN_PLAYERS:
                logger.warning("Not enough players detected for classification")
                return
                
            features = self._extract_features(crops)
            reduced_features = self.reducer.fit_transform(features)
            self.kmeans.fit(reduced_features)
            
        except Exception as e:
            logger.error(f"Team classification failed: {str(e)}")
            raise

    def predict(self, frame: np.ndarray, bbox: List[float]) -> int:
        """Predict team for a single player"""
        try:
            crop = self._get_player_crop(frame, bbox)
            if crop is None:
                return 1
                
            features = self._extract_features([crop])
            reduced_features = self.reducer.transform(features)
            team_id = self.kmeans.predict(reduced_features)[0] + 1
            
            return team_id
        except Exception as e:
            logger.error(f"Team prediction failed: {str(e)}")
            return 1

class TeamAssigner:
    """Assigns players to teams and manages team colors"""
    
    def __init__(self):
        """Initialize team assigner"""
        self.device = self._get_device()
        self.classifier = TeamClassifier(device=self.device)
        self.player_team_dict: Dict[int, int] = {}
        self.team_colors = {
            team_id: self._hex_to_bgr(color)
            for team_id, color in TEAM_COLORS.items()
        }

    @staticmethod
    def _get_device() -> str:
        """Determine best available computing device"""
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        return 'cpu'

    @staticmethod
    def _hex_to_bgr(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to BGR format for OpenCV"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return rgb[2], rgb[1], rgb[0]

    def assign_team_color(self, frame: np.ndarray, player_detections: Dict) -> None:
        """Assign team colors to detected players"""
        try:
            self.classifier.fit(frame, player_detections)
        except Exception as e:
            logger.error(f"Team color assignment failed: {str(e)}")
            if self.device != 'cpu':
                logger.info("Falling back to CPU processing")
                self.device = 'cpu'
                self.classifier = TeamClassifier(device=self.device)
                self.assign_team_color(frame, player_detections)

    def get_player_team(self, frame: np.ndarray, player_bbox: List[float], 
                       player_id: int) -> int:
        """Get team assignment for a player"""
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
            
        team_id = self.classifier.predict(frame, player_bbox)
        self.player_team_dict[player_id] = team_id
        return team_id
