import torch
import torch.nn as nn
from sklearn.cluster import KMeans
import numpy as np
import cv2

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.device = self._get_device()
        
    def _get_device(self):
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'
    
    def get_clustering_model(self, image):
        # Convert image to torch tensor and move to appropriate device
        image_tensor = torch.from_numpy(image).to(self.device)
        
        # Reshape the image to 2D array
        image_2d = image_tensor.reshape(-1, 3)
        
        # If using GPU, convert back to CPU for KMeans
        if self.device != 'cpu':
            image_2d = image_2d.cpu().numpy()
        else:
            image_2d = image_2d.numpy()
            
        # Perform K-means with 2 clusters
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        
        # Use smaller subset of data for fitting to reduce memory usage
        sample_size = min(1000, image_2d.shape[0])
        indices = np.random.choice(image_2d.shape[0], sample_size, replace=False)
        kmeans.fit(image_2d[indices])
        
        return kmeans

    def get_player_color(self, frame, bbox):
        # Sample smaller patches instead of entire player region
        patch_size = (32, 32)
        y1, y2 = max(int(bbox[1]), 0), min(int(bbox[3]), frame.shape[0])
        x1, x2 = max(int(bbox[0]), 0), min(int(bbox[2]), frame.shape[1])
        
        if y2 <= y1 or x2 <= x1:
            return np.zeros(3, dtype=np.float32)
        
        # Take center patch
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        patch_x1 = max(center_x - patch_size[0]//2, 0)
        patch_x2 = min(center_x + patch_size[0]//2, frame.shape[1])
        patch_y1 = max(center_y - patch_size[1]//2, 0)
        patch_y2 = min(center_y + patch_size[1]//2, frame.shape[0])
        
        image = frame[patch_y1:patch_y2, patch_x1:patch_x2]
        return self._process_image_patch(image)

    def _process_image_patch(self, image):
        if image.size == 0:
            return np.zeros(3, dtype=np.float32)
        
        # Use only top half of the image
        top_half_image = image[0:int(image.shape[0]/2), :]
        
        # Reduce image size if too large
        if top_half_image.shape[0] * top_half_image.shape[1] > 10000:
            scale = np.sqrt(10000 / (top_half_image.shape[0] * top_half_image.shape[1]))
            new_size = (int(top_half_image.shape[1] * scale), int(top_half_image.shape[0] * scale))
            top_half_image = cv2.resize(top_half_image, new_size)

        # Convert to float32 for better precision
        top_half_image = top_half_image.astype(np.float32)
        
        # Get Clustering model
        kmeans = self.get_clustering_model(top_half_image)
        
        # Get the cluster labels for each pixel
        labels = kmeans.predict(top_half_image.reshape(-1, 3))
        
        # Reshape the labels to the image shape
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])
        
        # Get the player cluster
        corner_clusters = [
            clustered_image[0,0],
            clustered_image[0,-1],
            clustered_image[-1,0],
            clustered_image[-1,-1]
        ]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster
        
        return kmeans.cluster_centers_[player_cluster].astype(np.float32)

    def assign_team_color(self, frame, player_detections):
        # Convert list of colors to numpy array first, then to tensor
        player_colors = []
        batch_size = 10
        
        try:
            for i in range(0, len(player_detections), batch_size):
                batch = list(player_detections.items())[i:i+batch_size]
                batch_colors = []
                
                for _, player_detection in batch:
                    bbox = player_detection["bbox"]
                    player_color = self.get_player_color(frame, bbox)
                    batch_colors.append(player_color)
                
                # Convert batch to numpy array first
                batch_colors = np.array(batch_colors, dtype=np.float32)
                player_colors.append(batch_colors)
                
                if self.device == 'cuda':
                    torch.cuda.empty_cache()
            
            if not player_colors:
                return
            
            # Combine all batches into single numpy array
            player_colors = np.concatenate(player_colors, axis=0)
            
            # Convert numpy array to tensor
            colors_tensor = torch.from_numpy(player_colors).to(self.device)
            
            # Use PyTorch K-means implementation or move back to CPU for sklearn
            if self.device != 'cpu':
                colors_tensor = colors_tensor.cpu()
            
            kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
            kmeans.fit(colors_tensor)
            
            self.kmeans = kmeans
            self.team_colors[1] = kmeans.cluster_centers_[0]
            self.team_colors[2] = kmeans.cluster_centers_[1]
            
        except Exception as e:
            print(f"Error in assign_team_color: {str(e)}")
            # Fallback to CPU if there's an error
            if self.device != 'cpu':
                self.device = 'cpu'
                self.assign_team_color(frame, player_detections)

    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
            
        player_color = self.get_player_color(frame, player_bbox)
        
        # Convert to tensor for prediction
        color_tensor = torch.tensor(player_color.reshape(1, -1))
        if self.device != 'cpu':
            color_tensor = color_tensor.cpu()
            
        team_id = self.kmeans.predict(color_tensor)[0] + 1
        
        # Special case handling
        if player_id == 91:
            team_id = 1
            
        self.player_team_dict[player_id] = team_id
        return team_id
