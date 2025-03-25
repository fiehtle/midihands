import cv2
import subprocess
import json
import os
import time

def force_builtin_camera():
    """
    Forces the use of the built-in FaceTime camera by explicitly checking device names
    and blocking Continuity Camera.
    """
    try:
        # First, try to enumerate all video devices
        cmd = ['system_profiler', 'SPCameraDataType', '-json']
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        # Try to find the built-in camera index
        camera_index = None
        for idx in range(10):  # Check first 10 indices to be thorough
            cap = cv2.VideoCapture(idx)
            if not cap.isOpened():
                continue
                
            # Get camera name
            name = cap.getBackendName()
            if "FaceTime" in name or "Built-in" in name:
                camera_index = idx
                cap.release()
                break
            cap.release()
        
        if camera_index is not None:
            # Found the built-in camera
            cap = cv2.VideoCapture(camera_index)
            
            # Set specific properties for MacBook camera
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Verify we can actually get frames
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"Successfully connected to built-in camera (index {camera_index})")
                return cap
            else:
                cap.release()
    
    except Exception as e:
        print(f"Error during camera detection: {e}")
    
    # If all else fails, try the most common built-in camera index
    print("Attempting fallback to default built-in camera...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap
    
    return None

def get_builtin_camera():
    """
    Wrapper function that ensures we get the built-in camera with multiple retries
    if needed.
    """
    # Set environment variable to disable Continuity Camera
    os.environ['OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS'] = '0'
    os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'avoid_video_capture_apis=1'
    
    # Try multiple times to get the built-in camera
    for attempt in range(3):
        cap = force_builtin_camera()
        if cap is not None:
            return cap
        print(f"Camera initialization attempt {attempt + 1} failed, retrying...")
        time.sleep(1)  # Wait a bit before retrying
    
    print("Failed to initialize built-in camera after multiple attempts")
    return None 