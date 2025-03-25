import cv2
import mediapipe as mp
import numpy as np
import sys
from camera_utils import get_builtin_camera

class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Define chord mappings for C Major
        self.chord_mappings = {
            1: ("I", "C"),
            2: ("IV", "F"),
            3: ("V", "G"),
            4: ("VI", "Am"),
            5: ("II", "Dm")
        }
        
    def count_fingers(self, hand_landmarks):
        """Count number of extended fingers"""
        finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky tip indices
        thumb_tip = 4
        finger_count = 0
        
        # Check thumb
        if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
            finger_count += 1
            
        # Check other fingers
        for tip in finger_tips:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                finger_count += 1
                
        return finger_count

    def process_frame(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # Initialize variables for left hand information
        left_hand_info = None
        
        # Draw hand landmarks if detected
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Determine if this is the left hand
                if results.multi_handedness[idx].classification[0].label == "Left":
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Count fingers for left hand
                    finger_count = self.count_fingers(hand_landmarks)
                    
                    # Get chord information
                    chord_info = self.chord_mappings.get(finger_count, (None, None))
                    left_hand_info = (finger_count, chord_info)
        
        # Display information on frame
        if left_hand_info:
            finger_count, (roman_numeral, chord_name) = left_hand_info
            
            # Display finger count
            cv2.putText(
                frame,
                f'Fingers: {finger_count}',
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Display chord information
            if roman_numeral and chord_name:
                cv2.putText(
                    frame,
                    f'Chord: {roman_numeral} ({chord_name})',
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
        else:
            # Display "No Left Hand" message
            cv2.putText(
                frame,
                "No Left Hand Detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
                
        return frame

def main():
    print("Initializing camera...")
    cap = get_builtin_camera()
    if cap is None:
        print("Error: Could not initialize built-in camera. Please ensure no other application is using it.")
        sys.exit(1)
    
    print("Camera initialized successfully. Starting hand detection...")
    detector = HandGestureDetector()
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Process frame
            processed_frame = detector.process_frame(frame)
            
            # Display the frame
            cv2.imshow('Hand Gesture Detection - C Major Scale', processed_frame)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up...")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 