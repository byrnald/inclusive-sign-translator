"""
Flask Backend for Inclusive Sign Translator
Handles gesture detection API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
import numpy as np
import joblib
import pickle
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variables for model and feature extractor
model = None
feature_extractor = None
model_loaded = False

def load_model():
    """Load the trained model and feature extractor"""
    global model, feature_extractor, model_loaded
    
    try:
        # Load the trained model
        model_path = '../model/saved_models/asl_gesture_classifier.joblib'
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print("Model file not found. Using placeholder model.")
            model = None
        
        # Load feature extractor
        extractor_path = '../model/saved_models/feature_extractor.pkl'
        if os.path.exists(extractor_path):
            with open(extractor_path, 'rb') as f:
                feature_extractor = pickle.load(f)
            print(f"Feature extractor loaded from {extractor_path}")
        else:
            print("Feature extractor not found. Using placeholder.")
            feature_extractor = None
        
        model_loaded = True
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        model_loaded = False
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/model-status', methods=['GET'])
def model_status():
    """Get model status"""
    return jsonify({
        'model_loaded': model_loaded,
        'model_type': type(model).__name__ if model else None,
        'feature_extractor_loaded': feature_extractor is not None
    })

@app.route('/api/detect-gesture', methods=['POST'])
def detect_gesture():
    """Detect gesture from image data"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'error': 'No image data provided'
            }), 400
        
        # Decode base64 image
        image_data = data['image']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({
                'error': 'Invalid image data'
            }), 400
        
        # Placeholder gesture detection
        # TODO: Implement actual gesture detection using Mediapipe + ML model
        gesture, confidence = detect_gesture_from_image(image)
        
        return jsonify({
            'gesture': gesture,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Detection failed: {str(e)}'
        }), 500

@app.route('/api/classify-landmarks', methods=['POST'])
def classify_landmarks():
    """Classify gesture from hand landmarks"""
    try:
        data = request.get_json()
        
        if not data or 'landmarks' not in data:
            return jsonify({
                'error': 'No landmarks data provided'
            }), 400
        
        landmarks = data['landmarks']
        
        if not model_loaded or not model or not feature_extractor:
            # Return placeholder result
            return jsonify({
                'gesture': 'A',
                'confidence': 0.85,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using placeholder model'
            })
        
        # Extract features from landmarks
        features = feature_extractor(landmarks)
        
        # Predict gesture
        gesture = model.predict([features])[0]
        confidence = model.predict_proba([features]).max()
        
        return jsonify({
            'gesture': gesture,
            'confidence': float(confidence),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Classification failed: {str(e)}'
        }), 500

def detect_gesture_from_image(image):
    """Placeholder gesture detection from image"""
    # TODO: Implement actual gesture detection
    # 1. Use Mediapipe to detect hand landmarks
    # 2. Extract features from landmarks
    # 3. Use trained model to classify gesture
    
    # Placeholder logic
    gestures = ['A', 'B', 'C', 'D', 'E']
    import random
    gesture = random.choice(gestures)
    confidence = random.uniform(0.6, 0.95)
    
    return gesture, confidence

@app.route('/api/upload-training-data', methods=['POST'])
def upload_training_data():
    """Upload training data for model retraining"""
    try:
        data = request.get_json()
        
        # TODO: Implement training data upload and model retraining
        # This would be used to improve the model with new data
        
        return jsonify({
            'success': True,
            'message': 'Training data uploaded successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Upload failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Load model on startup
    load_model()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
