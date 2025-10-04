"""
Improved Hand Detection using Contour Analysis
This script detects fingers and hand landmarks using OpenCV contour analysis
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

class ImprovedHandDetector:
    def __init__(self):
        self.min_contour_area = 10000  # Minimum area for hand detection
        self.max_contour_area = 100000  # Maximum area for hand detection

    def detect_hands(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Detect hands and extract finger landmarks using contour analysis
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (hand_detected, landmarks)
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
        
        if not contours:
            return False, None
        
        # Find the largest contour (likely the hand)
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        # Check if the contour is large enough to be a hand
        if area < self.min_contour_area or area > self.max_contour_area:
            return False, None
        
        # Extract finger landmarks using convex hull and defects
        landmarks = self._extract_finger_landmarks(largest_contour, image.shape)
        
        if landmarks and len(landmarks) >= 5:  # At least 5 key points
            return True, landmarks
        
        return False, None
    
    def _extract_finger_landmarks(self, contour: np.ndarray, image_shape: Tuple) -> Optional[List]:
        """
        Extract finger landmarks using convex hull and convexity defects
        
        Args:
            contour: Hand contour
            image_shape: Shape of the input image
            
        Returns:
            List of landmark points
        """
        try:
            # Find convex hull
            hull = cv2.convexHull(contour, returnPoints=False)
            hull_points = cv2.convexHull(contour, returnPoints=True)
            
            # Find convexity defects
            defects = cv2.convexityDefects(contour, hull)
            
            if defects is None:
                return None
            
            # Extract finger tips and valleys
            landmarks = []
            
            # Get the wrist point (bottom of the hand)
            moments = cv2.moments(contour)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                wrist_point = [cx / image_shape[1], cy / image_shape[0], 0.0]
                landmarks.append(wrist_point)
            
            # Extract finger tips from convex hull
            finger_tips = []
            for i in range(len(hull_points)):
                point = hull_points[i][0]
                # Check if this point is likely a finger tip (high y-coordinate)
                if point[1] < cy - 50:  # Above wrist center
                    finger_tips.append(point)
            
            # Sort finger tips by x-coordinate
            finger_tips.sort(key=lambda x: x[0])
            
            # Add finger tips as landmarks
            for tip in finger_tips[:5]:  # Maximum 5 fingers
                normalized_tip = [tip[0] / image_shape[1], tip[1] / image_shape[0], 0.0]
                landmarks.append(normalized_tip)
            
            # Extract finger valleys from convexity defects
            valleys = []
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                
                # Calculate the angle between the lines
                a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                
                # Calculate angle using cosine rule
                angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
                
                # If angle is less than 90 degrees, it's a finger valley
                if angle <= np.pi/2 and d > 10000:  # Distance threshold
                    valleys.append(far)
            
            # Add valleys as landmarks
            for valley in valleys[:4]:  # Maximum 4 valleys
                normalized_valley = [valley[0] / image_shape[1], valley[1] / image_shape[0], 0.0]
                landmarks.append(normalized_valley)
            
            # If we don't have enough landmarks, create synthetic ones
            while len(landmarks) < 21:
                # Create synthetic landmarks based on existing ones
                if len(landmarks) >= 2:
                    # Interpolate between existing points
                    p1 = landmarks[-2]
                    p2 = landmarks[-1]
                    synthetic = [
                        (p1[0] + p2[0]) / 2,
                        (p1[1] + p2[1]) / 2,
                        0.0
                    ]
                    landmarks.append(synthetic)
                else:
                    # Add random points if we don't have enough
                    landmarks.append([0.5, 0.5, 0.0])
            
            return landmarks[:21]  # Return exactly 21 landmarks
            
        except Exception as e:
            print(f"Error extracting landmarks: {e}")
            return None
    
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
            # Draw landmarks as circles with different colors for different types
            for i, landmark in enumerate(landmarks):
                # Convert normalized coordinates back to pixel coordinates
                x = int(landmark[0] * image.shape[1])
                y = int(landmark[1] * image.shape[0])
                
                # Color code different types of landmarks
                if i == 0:  # Wrist
                    color = (255, 0, 0)  # Red
                    radius = 5
                elif i <= 5:  # Finger tips
                    color = (0, 255, 0)  # Green
                    radius = 4
                else:  # Other points
                    color = (0, 0, 255)  # Blue
                    radius = 3
                
                # Draw circle for each landmark
                cv2.circle(annotated_image, (x, y), radius, color, -1)
                
                # Add landmark number
                cv2.putText(annotated_image, str(i), (x + 5, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return annotated_image
    
    def draw_hand_contour(self, image: np.ndarray) -> np.ndarray:
        """
        Draw the detected hand contour on the image
        
        Args:
            image: Input image
            
        Returns:
            Image with hand contour drawn
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
        
        annotated_image = image.copy()
        
        if contours:
            # Find the largest contour (likely the hand)
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Check if the contour is large enough to be a hand
            if self.min_contour_area < area < self.max_contour_area:
                # Draw the contour
                cv2.drawContours(annotated_image, [largest_contour], -1, (0, 255, 0), 2)
                
                # Draw convex hull
                hull = cv2.convexHull(largest_contour)
                cv2.drawContours(annotated_image, [hull], -1, (255, 0, 0), 2)
        
        return annotated_image

def test_improved_hand_detection():
    """Test improved hand detection with webcam"""
    detector = ImprovedHandDetector()
    cap = cv2.VideoCapture(0)
    
    print("Testing Improved Hand Detection...")
    print("Press 'q' to quit")
    print("Press 'c' to toggle contour view")
    print("Red = Wrist, Green = Finger Tips, Blue = Other landmarks")
    
    show_contour = False
    
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
            cv2.putText(frame, "Hand Detected (Improved)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show contour if requested
        if show_contour:
            frame = detector.draw_hand_contour(frame)
            cv2.putText(frame, "Contour View", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Display the frame
        cv2.imshow('Improved Hand Detection', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_contour = not show_contour
    
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
    if not landmarks or len(landmarks) < 5:
        return np.array([])
    
    landmarks = np.array(landmarks)
    
    # Calculate distances between key points
    # Use the first 5 landmarks (wrist + 4 finger tips)
    key_points = landmarks[:5]
    
    # Calculate distances
    distances = []
    for i in range(len(key_points)):
        for j in range(i + 1, len(key_points)):
            dist = np.linalg.norm(key_points[i] - key_points[j])
            distances.append(dist)
    
    # Calculate angles
    angles = []
    if len(key_points) >= 3:
        for i in range(len(key_points) - 2):
            v1 = key_points[i] - key_points[i + 1]
            v2 = key_points[i + 1] - key_points[i + 2]
            if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                angle = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1))
                angles.append(angle)
    
    # Combine features
    features = np.concatenate([distances, angles])
    
    return features

if __name__ == "__main__":
    test_improved_hand_detection()
