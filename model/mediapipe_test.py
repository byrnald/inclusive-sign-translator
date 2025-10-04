"""
Mediapipe Hands Test Script
This script tests Mediapipe hand detection and landmark extraction
"""

import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Detect hands in the image and return landmarks
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (hand_detected, landmarks)
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.hands.process(rgb_image)
        
        if results.multi_hand_landmarks:
            # Get the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Convert landmarks to numpy array
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.append([landmark.x, landmark.y, landmark.z])
            
            return True, landmarks
        else:
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
        # Convert landmarks to Mediapipe format
        hand_landmarks = self.mp_hands.HandLandmark
        mp_landmarks = []
        
        for i, landmark in enumerate(landmarks):
            mp_landmark = self.mp_hands.HandLandmark()
            mp_landmark.x = landmark[0]
            mp_landmark.y = landmark[1]
            mp_landmark.z = landmark[2]
            mp_landmarks.append(mp_landmark)
        
        # Draw landmarks
        annotated_image = image.copy()
        self.mp_drawing.draw_landmarks(
            annotated_image,
            mp_landmarks,
            self.mp_hands.HAND_CONNECTIONS
        )
        
        return annotated_image

def test_hand_detection():
    """Test hand detection with webcam"""
    detector = HandDetector()
    cap = cv2.VideoCapture(0)
    
    print("Testing hand detection...")
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect hands
        hand_detected, landmarks = detector.detect_hands(frame)
        
        if hand_detected:
            print(f"Hand detected! Landmarks: {len(landmarks)} points")
            
            # Draw landmarks
            frame = detector.draw_landmarks(frame, landmarks)
            
            # Display confidence
            cv2.putText(frame, "Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow('Hand Detection Test', frame)
        
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

