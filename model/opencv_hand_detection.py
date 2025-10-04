"""
OpenCV-based Hand Detection Script
Alternative to MediaPipe for Python 3.13 compatibility
This script uses OpenCV's built-in hand detection capabilities
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

class OpenCVHandDetector:
    def __init__(self):
        # Initialize OpenCV's hand cascade classifier
        # Note: This is a simplified approach - for production, consider using
        # a pre-trained hand detection model or MediaPipe when available
        self.hand_cascade = None
        
        # Try to load a hand cascade if available
        try:
            # This would require a hand cascade XML file
            # For now, we'll use a simple color-based detection
            self.use_color_detection = True
        except:
            self.use_color_detection = True

    def detect_hands(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Detect hands in the image using color-based detection
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (hand_detected, landmarks)
        """
        if self.use_color_detection:
            return self._detect_hands_by_color(image)
        else:
            return self._detect_hands_by_cascade(image)
    
    def _detect_hands_by_color(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Simple hand detection using skin color detection
        This is a basic approach - for production, use MediaPipe or a trained model
        """
        # Convert BGR to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create mask for skin color
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (likely the hand)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Check if the contour is large enough to be a hand
            area = cv2.contourArea(largest_contour)
            if area > 5000:  # Minimum area threshold
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Create simple "landmarks" based on bounding box
                # This is a simplified approach - real landmarks would be more complex
                landmarks = self._create_simple_landmarks(x, y, w, h)
                
                return True, landmarks
        
        return False, None
    
    def _create_simple_landmarks(self, x: int, y: int, w: int, h: int) -> List:
        """
        Create simplified landmarks based on bounding box
        This is a placeholder - real hand landmarks would be 21 3D points
        """
        landmarks = []
        
        # Create 21 simplified landmark points
        # These are based on typical hand proportions
        for i in range(21):
            # Distribute points across the hand area
            if i < 5:  # Thumb
                px = x + (i * w // 4)
                py = y + h // 2
            elif i < 9:  # Index finger
                px = x + w // 2
                py = y + (i - 5) * h // 4
            elif i < 13:  # Middle finger
                px = x + w // 2 + w // 8
                py = y + (i - 9) * h // 4
            elif i < 17:  # Ring finger
                px = x + w // 2 + w // 4
                py = y + (i - 13) * h // 4
            else:  # Pinky
                px = x + w // 2 + 3 * w // 8
                py = y + (i - 17) * h // 4
            
            # Normalize coordinates (0-1 range)
            landmarks.append([px / 640.0, py / 480.0, 0.0])  # Assuming 640x480 image
        
        return landmarks
    
    def _detect_hands_by_cascade(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Hand detection using Haar cascade (if available)
        """
        # This would require a hand cascade XML file
        # For now, return False
        return False, None
    
    def draw_landmarks(self, image: np.ndarray, landmarks: List) -> np.ndarray:
        """
        Draw hand landmarks on the image
        
        Args:
            image: Input image
            landmarks: Hand landmarks
            
        Returns:
            Image with landmarks drawn
        """
        annotated_image = image.copy()
        
        if landmarks:
            # Draw landmarks as circles
            for i, landmark in enumerate(landmarks):
                # Convert normalized coordinates back to pixel coordinates
                x = int(landmark[0] * image.shape[1])
                y = int(landmark[1] * image.shape[0])
                
                # Draw circle for each landmark
                cv2.circle(annotated_image, (x, y), 3, (0, 255, 0), -1)
                
                # Add landmark number
                cv2.putText(annotated_image, str(i), (x + 5, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        return annotated_image

def test_hand_detection():
    """Test hand detection with webcam"""
    detector = OpenCVHandDetector()
    cap = cv2.VideoCapture(0)
    
    print("Testing OpenCV-based hand detection...")
    print("Press 'q' to quit")
    print("Note: This is a simplified detection method.")
    print("For production, use MediaPipe or a trained hand detection model.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))
        
        # Detect hands
        hand_detected, landmarks = detector.detect_hands(frame)
        
        if hand_detected:
            print(f"Hand detected! Landmarks: {len(landmarks)} points")
            
            # Draw landmarks
            frame = detector.draw_landmarks(frame, landmarks)
            
            # Display confidence
            cv2.putText(frame, "Hand Detected (OpenCV)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow('OpenCV Hand Detection Test', frame)
        
        # Break on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def extract_hand_features(landmarks: List) -> np.ndarray:
    """
    Extract features from hand landmarks for gesture classification
    
    Args:
        landmarks: List of hand landmarks
        
    Returns:
        Feature vector
    """
    if not landmarks:
        return np.array([])
    
    landmarks = np.array(landmarks)
    
    # Calculate distances between key points
    # Using simplified landmark indices
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    
    # Calculate distances
    distances = []
    key_points = [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]
    
    for i in range(len(key_points)):
        for j in range(i + 1, len(key_points)):
            dist = np.linalg.norm(key_points[i] - key_points[j])
            distances.append(dist)
    
    # Calculate angles
    angles = []
    for i in range(len(key_points) - 2):
        v1 = key_points[i] - key_points[i + 1]
        v2 = key_points[i + 1] - key_points[i + 2]
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angles.append(angle)
    
    # Combine features
    features = np.concatenate([distances, angles])
    
    return features

if __name__ == "__main__":
    test_hand_detection()
