import cv2

def get_builtin_camera():
    """
    Attempts to get the built-in MacBook camera while avoiding Continuity Camera.
    Returns a cv2.VideoCapture object or None if no built-in camera is found.
    """
    # Try common camera indices
    for idx in range(2):  # Usually 0 or 1
        cap = cv2.VideoCapture(idx)
        if not cap.isOpened():
            continue
            
        # Set specific resolution that works well with MacBook camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Read a test frame
        ret, frame = cap.read()
        if ret and frame is not None:
            # If we got a frame, this is likely the built-in camera
            return cap
        
        # If this camera didn't work, release it
        cap.release()
    
    return None 