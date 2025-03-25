import cv2
import subprocess
import json

def get_builtin_camera():
    """
    Specifically targets the MacBook's built-in camera using system information.
    Returns a cv2.VideoCapture object or None if no built-in camera is found.
    """
    try:
        # Use system_profiler to get camera information
        cmd = ['system_profiler', 'SPCameraDataType', '-json']
        result = subprocess.run(cmd, capture_output=True, text=True)
        cameras = json.loads(result.stdout)
        
        # Look for the built-in camera
        for camera in cameras.get('SPCameraDataType', []):
            if 'Built-in' in camera.get('_name', ''):
                # Found the built-in camera, try to open it
                cap = cv2.VideoCapture(0)  # Usually index 0 is built-in
                if cap.isOpened():
                    # Configure camera
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    return cap
                
                # If index 0 didn't work, try index 1
                cap = cv2.VideoCapture(1)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    return cap
    except Exception as e:
        print(f"Error detecting camera: {e}")
    
    # Fallback to simple method if system_profiler approach fails
    print("Falling back to default camera selection...")
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap
    
    return None 