import cv2
import mediapipe as mp
import pyautogui
import time
import math
from collections import deque

class HandGestureController:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Gesture tracking variables
        self.last_action_time = 0
        self.action_cooldown = 0.5  # Cooldown between actions (seconds)
        self.last_finger_count = 0
        self.stable_count_frames = 0
        self.required_stable_frames = 3  # Frames needed for stable gesture
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        
    def detect_finger_count(self, landmarks):
        """Detect how many fingers are being held up"""
        if not landmarks:
            return 0
        
        # Landmark indices for fingertips and joints
        tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        pip_ids = [3, 6, 10, 14, 18]  # Corresponding PIP joints
        
        fingers_up = []
        
        # Thumb (special case - check x-coordinate)
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers_up.append(1)
        else:
            fingers_up.append(0)
            
        # Other fingers (check y-coordinate)
        for i in range(1, 5):
            if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
                
        return sum(fingers_up)

    def is_fist(self, landmarks):
        """Detect if hand is making a fist"""
        return self.detect_finger_count(landmarks) == 0

    def perform_game_action(self, action):
        """Execute game controls based on detected gesture"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_action_time < self.action_cooldown:
            return False
            
        if action == "left":
            pyautogui.press('left')
            print("Action: Move Left (1 finger)")
        elif action == "right":
            pyautogui.press('right')
            print("Action: Move Right (2 fingers)")
        elif action == "jump":
            pyautogui.press('up')
            print("Action: Jump (3 fingers)")
        elif action == "slide":
            pyautogui.press('down')
            print("Action: Slide (4 fingers)")
        elif action == "fist_jump":
            pyautogui.press('space')
            print("Action: Jump (Fist)")
            
        self.last_action_time = current_time
        return True

    def process_finger_gesture(self, finger_count):
        """Process finger count and execute corresponding action"""
        # Check if finger count is stable
        if finger_count == self.last_finger_count:
            self.stable_count_frames += 1
        else:
            self.stable_count_frames = 0
            self.last_finger_count = finger_count
            
        # Only act if gesture is stable for required frames
        if self.stable_count_frames >= self.required_stable_frames:
            if finger_count == 1:
                return self.perform_game_action("left")
            elif finger_count == 2:
                return self.perform_game_action("right")
            elif finger_count == 3:
                return self.perform_game_action("jump")
            elif finger_count == 4:
                return self.perform_game_action("slide")
            elif finger_count == 5:
                return self.perform_game_action("jump")  # Alternative jump
                
        return False

    def draw_landmarks_and_info(self, image, landmarks, gesture_info):
        """Draw hand landmarks and gesture information on the image"""
        # Draw hand landmarks
        if landmarks:
            # Draw landmarks
            self.mp_draw.draw_landmarks(
                image, landmarks, self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
        
        # Draw gesture information
        finger_count, gesture_name = gesture_info
        cv2.putText(image, f"Fingers: {finger_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(image, f"Gesture: {gesture_name}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Draw stability indicator
        stability = min(self.stable_count_frames / self.required_stable_frames, 1.0)
        bar_width = int(200 * stability)
        cv2.rectangle(image, (10, 100), (10 + bar_width, 120), (0, 255, 0), -1)
        cv2.rectangle(image, (10, 100), (210, 120), (255, 255, 255), 2)
        cv2.putText(image, "Stability", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw instructions
        instructions = [
            "1 finger: Move Left",
            "2 fingers: Move Right", 
            "3 fingers: Jump",
            "4 fingers: Slide",
            "5 fingers: Jump",
            "Fist: Jump",
            "Press 'q' to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(image, instruction, (10, image.shape[0] - 180 + i * 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    def run(self):
        """Main loop for gesture detection and control"""
        print("Finger Counting Hand Gesture Controller for Subway Surfers")
        print("Make sure Subway Surfers is running and in focus!")
        print("Controls:")
        print("- 1 finger: Move left")
        print("- 2 fingers: Move right")
        print("- 3 fingers: Jump")
        print("- 4 fingers: Slide")
        print("- 5 fingers: Jump (alternative)")
        print("- Fist (0 fingers): Jump")
        print("- Press 'q' to quit")
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = self.hands.process(rgb_frame)
            
            finger_count = 0
            gesture_name = "None"
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Count fingers
                    finger_count = self.detect_finger_count(hand_landmarks.landmark)
                    
                    # Check for fist
                    if finger_count == 0:
                        gesture_name = "Fist (Jump)"
                        if self.perform_game_action("fist_jump"):
                            pass  # Action performed
                    else:
                        # Process finger gesture
                        gesture_names = {
                            1: "One (Left)",
                            2: "Two (Right)", 
                            3: "Three (Jump)",
                            4: "Four (Slide)",
                            5: "Five (Jump)"
                        }
                        gesture_name = gesture_names.get(finger_count, f"{finger_count} fingers")
                        self.process_finger_gesture(finger_count)
                    
                    # Draw landmarks and info
                    self.draw_landmarks_and_info(frame, hand_landmarks, (finger_count, gesture_name))
                    break  # Only process first hand
            else:
                # No hand detected
                self.draw_landmarks_and_info(frame, None, (0, "No hand detected"))
                self.stable_count_frames = 0
                self.last_finger_count = 0
            
            # Display frame
            cv2.imshow('Finger Counting Subway Surfers Controller', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = HandGestureController()
    controller.run()