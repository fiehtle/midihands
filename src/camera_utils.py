import cv2
import subprocess
import json
import os
import time

def force_builtin_camera():
    """
    Forces the use of the built-in FaceTime camera using AVFoundation backend.
    """
    try:
        # On macOS, index 0 with AVFoundation should be the built-in camera
        cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            # Set specific properties for MacBook camera
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Verify we can actually get frames
            ret, frame = cap.read()
            if ret and frame is not None:
                print("Successfully connected to built-in camera using AVFoundation")
                return cap
            else:
                cap.release()
    except Exception as e:
        print(f"Error during camera detection: {e}")
    
    return None

def get_builtin_camera():
    """
    Wrapper function that ensures we get the built-in camera with multiple retries
    if needed.
    """
    # Explicitly set backend to AVFoundation
    os.environ['OPENCV_CAMERA_BACKEND'] = 'avfoundation'
    
    # Try multiple times to get the built-in camera
    for attempt in range(3):
        cap = force_builtin_camera()
        if cap is not None:
            return cap
        print(f"Camera initialization attempt {attempt + 1} failed, retrying...")
        time.sleep(1)  # Wait a bit before retrying
    
    print("Failed to initialize built-in camera after multiple attempts")
    return None 