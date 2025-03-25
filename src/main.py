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
        
        # Define finger indices
        self.finger_indices = {
            'thumb': 4,
            'index': 8,
            'middle': 12,
            'ring': 16,
            'pinky': 20
        }
    
    def is_finger_extended(self, hand_landmarks, finger_tip_idx, threshold=0.1):
        """
        Check if a finger is extended by comparing it with its neighbors and base joints.
        Uses relative positions to handle different hand orientations.
        """
        # Get the base, middle, and tip of the finger
        base = finger_tip_idx - 3
        middle = finger_tip_idx - 2
        tip = finger_tip_idx
        
        # Get the landmarks
        base_point = hand_landmarks.landmark[base]
        middle_point = hand_landmarks.landmark[middle]
        tip_point = hand_landmarks.landmark[tip]
        
        # For thumb, check the angle with index finger base
        if finger_tip_idx == self.finger_indices['thumb']:
            index_base = hand_landmarks.landmark[5]  # Index finger base
            # Check if thumb is more to the side than the index base
            return tip_point.x < index_base.x
        
        # For other fingers, check if tip is higher than middle joint
        # and maintain a minimum distance to consider it "extended"
        vertical_distance = middle_point.y - tip_point.y
        return vertical_distance > threshold
        
    def interpret_counting_gesture(self, hand_landmarks):
        """
        Interpret the hand gesture as a counting number based on cultural finger counting patterns.
        Returns a number 1-5 based on the gesture.
        """
        # Check each finger's state
        is_thumb_up = self.is_finger_extended(hand_landmarks, self.finger_indices['thumb'])
        is_index_up = self.is_finger_extended(hand_landmarks, self.finger_indices['index'])
        is_middle_up = self.is_finger_extended(hand_landmarks, self.finger_indices['middle'])
        is_ring_up = self.is_finger_extended(hand_landmarks, self.finger_indices['ring'])
        is_pinky_up = self.is_finger_extended(hand_landmarks, self.finger_indices['pinky'])
        
        # Pattern matching for numbers 1-5
        if is_index_up and not (is_middle_up or is_ring_up or is_pinky_up or is_thumb_up):
            return 1  # Index only
        elif is_index_up and is_middle_up and not (is_ring_up or is_pinky_up or is_thumb_up):
            return 2  # Peace sign
        elif is_index_up and is_middle_up and is_ring_up and not (is_pinky_up or is_thumb_up):
            return 3  # First three fingers
        elif is_index_up and is_middle_up and is_ring_up and is_pinky_up and not is_thumb_up:
            return 4  # All fingers except thumb
        elif is_index_up and is_middle_up and is_ring_up and is_pinky_up and is_thumb_up:
            return 5  # All fingers
            
        # If no recognized pattern is found, return 0
        return 0

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
                    
                    # Interpret the counting gesture
                    count = self.interpret_counting_gesture(hand_landmarks)
                    
                    # Get chord information if we have a valid count
                    if count > 0:
                        chord_info = self.chord_mappings.get(count, (None, None))
                        left_hand_info = (count, chord_info)
        
        # Display information on frame
        if left_hand_info:
            count, (roman_numeral, chord_name) = left_hand_info
            
            # Display finger count
            cv2.putText(
                frame,
                f'Count: {count}',
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