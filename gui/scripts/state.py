# Global state variables
is_analyzing = False

def set_analyzing_state(state):
    global is_analyzing
    is_analyzing = state

def get_analyzing_state():
    return is_analyzing 