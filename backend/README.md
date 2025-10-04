# Backend API for Inclusive Sign Translator

Flask backend that provides gesture detection and classification APIs.

## 🚀 Quick Start

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Running the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check
- **GET** `/api/health`
- Returns server health status

### Model Status
- **GET** `/api/model-status`
- Returns model loading status and type

### Gesture Detection
- **POST** `/api/detect-gesture`
- **Body**: `{"image": "base64_encoded_image"}`
- **Response**: `{"gesture": "A", "confidence": 0.85}`

### Landmark Classification
- **POST** `/api/classify-landmarks`
- **Body**: `{"landmarks": [[x, y, z], ...]}`
- **Response**: `{"gesture": "A", "confidence": 0.85}`

### Training Data Upload
- **POST** `/api/upload-training-data`
- **Body**: `{"data": "training_data"}`
- **Response**: `{"success": true}`

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Development mode (development/production)
- `MODEL_PATH`: Path to trained model file
- `PORT`: Server port (default: 5000)

### Model Files
The backend expects these model files in `../model/saved_models/`:
- `asl_gesture_classifier.joblib`: Trained ML model
- `feature_extractor.pkl`: Feature extraction function

## 🧪 Testing

### Manual Testingawdawdadawdawdawd
```bash
# Health check
curl http://localhost:5000/api/health

# Model status
curl http://localhost:5000/api/model-status
```

### Unit Tests
```bash
pytest tests/
```

## 🔄 Integration with Frontend

The frontend can connect to this backend by setting the `VITE_API_URL` environment variable:

```bash
# In frontend directory
VITE_API_URL=http://localhost:5000 npm run dev
```

## 📝 Development Notes

- The backend currently uses placeholder gesture detection
- Real implementation requires Mediapipe + trained ML model
- CORS is enabled for frontend integration
- Error handling for missing model files
- Base64 image decoding for camera frames

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔧 Troubleshooting

### Common Issues
1. **Model not loading**: Check if model files exist in `../model/saved_models/`
2. **CORS errors**: Ensure Flask-CORS is installed and configured
3. **Image decoding errors**: Verify base64 image format

### Logs
Check console output for error messages and model loading status.
