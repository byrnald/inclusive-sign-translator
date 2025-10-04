"""
Simplified Flask Backend for Inclusive Sign Translator
This is a minimal version that works without complex dependencies
"""

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import json
    from datetime import datetime
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available, using mock server")

if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'message': 'Backend is running!'
        })
    
    @app.route('/api/model-status', methods=['GET'])
    def model_status():
        """Get model status"""
        return jsonify({
            'model_loaded': False,
            'model_type': 'placeholder',
            'feature_extractor_loaded': False,
            'message': 'Using placeholder model'
        })
    
    @app.route('/api/detect-gesture', methods=['POST'])
    def detect_gesture():
        """Detect gesture from image data (placeholder)"""
        try:
            data = request.get_json()
            
            if not data or 'image' not in data:
                return jsonify({
                    'error': 'No image data provided'
                }), 400
            
            # Placeholder gesture detection
            import random
            gestures = ['A', 'B', 'C', 'D', 'E']
            gesture = random.choice(gestures)
            confidence = random.uniform(0.6, 0.95)
            
            return jsonify({
                'gesture': gesture,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using placeholder detection'
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Detection failed: {str(e)}'
            }), 500
    
    @app.route('/api/classify-landmarks', methods=['POST'])
    def classify_landmarks():
        """Classify gesture from hand landmarks (placeholder)"""
        try:
            data = request.get_json()
            
            if not data or 'landmarks' not in data:
                return jsonify({
                    'error': 'No landmarks data provided'
                }), 400
            
            # Placeholder classification
            import random
            gestures = ['A', 'B', 'C', 'D', 'E']
            gesture = random.choice(gestures)
            confidence = random.uniform(0.7, 0.9)
            
            return jsonify({
                'gesture': gesture,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'note': 'Using placeholder classification'
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Classification failed: {str(e)}'
            }), 500
    
    if __name__ == '__main__':
        print("Starting Flask backend...")
        print("Backend will be available at: http://localhost:5000")
        print("Health check: http://localhost:5000/api/health")
        app.run(debug=True, host='0.0.0.0', port=5000)

else:
    # Mock server for when Flask is not available
    print("Flask not available. Please install Flask to run the backend.")
    print("You can still run the frontend with placeholder detection.")
    print("\nTo install Flask, try:")
    print("1. python -m pip install flask flask-cors")
    print("2. Or use: pip install flask flask-cors")
    print("3. Or install Python from python.org if using Windows Store version")
