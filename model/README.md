# Model - ASL Gesture Recognition

Machine learning models and training notebooks for ASL gesture recognition.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
cd model
pip install -r requirements.txt
```

### Running Training
```bash
jupyter notebook training_notebooks/
```

## 📁 Project Structure

```
model/
├── training_notebooks/       # Jupyter notebooks for training
│   ├── 01_data_collection.ipynb    # Data collection notebook
│   └── 02_model_training.ipynb     # Model training notebook
├── saved_models/             # Trained models
│   ├── asl_gesture_classifier.joblib
│   └── feature_extractor.pkl
├── data/                     # Training data
│   └── raw/                  # Raw collected data
├── mediapipe_test.py         # Mediapipe testing script
├── requirements.txt          # Python dependencies
└── README.md
```

## 🧠 Model Architecture

### Feature Extraction
- **Hand Landmarks**: 21 3D points from Mediapipe
- **Distances**: Between key finger points
- **Angles**: Between finger joints
- **Normalization**: Scale-invariant features

### Model Types
1. **Random Forest**: Ensemble method with good interpretability
2. **SVM**: Support Vector Machine with RBF kernel
3. **Neural Network**: Multi-layer perceptron

### Gesture Classes
- **A**: Fist with thumb out
- **B**: Open hand with fingers together
- **C**: Curved hand like letter C
- **D**: Index finger pointing up
- **E**: Fist with thumb tucked

## 📊 Training Process

### 1. Data Collection
```python
# Run data collection notebook
jupyter notebook training_notebooks/01_data_collection.ipynb
```

**Steps:**
1. Set up camera and Mediapipe
2. Collect samples for each gesture
3. Save landmarks and metadata
4. Validate data quality

### 2. Model Training
```python
# Run training notebook
jupyter notebook training_notebooks/02_model_training.ipynb
```

**Steps:**
1. Load and preprocess data
2. Extract features from landmarks
3. Split into train/test sets
4. Train multiple models
5. Evaluate and select best model
6. Save model and feature extractor

### 3. Model Evaluation
- **Accuracy**: Overall classification accuracy
- **Confusion Matrix**: Per-class performance
- **Precision/Recall**: Per-gesture metrics
- **Cross-validation**: Robustness testing

## 🔧 Usage

### Testing Mediapipe
```bash
python mediapipe_test.py
```

### Loading Trained Model
```python
import joblib
import pickle

# Load model
model = joblib.load('saved_models/asl_gesture_classifier.joblib')

# Load feature extractor
with open('saved_models/feature_extractor.pkl', 'rb') as f:
    feature_extractor = pickle.load(f)

# Extract features from landmarks
features = feature_extractor(landmarks)

# Predict gesture
gesture = model.predict([features])[0]
confidence = model.predict_proba([features]).max()
```

## 📈 Performance Metrics

### Target Performance
- **Accuracy**: >85% on test set
- **Latency**: <100ms per prediction
- **Robustness**: Works in various lighting conditions

### Evaluation Metrics
- **Precision**: Per-gesture accuracy
- **Recall**: Gesture detection rate
- **F1-Score**: Harmonic mean of precision/recall
- **Confusion Matrix**: Error analysis

## 🔄 Model Improvement

### Data Augmentation
- **Rotation**: Rotate hand landmarks
- **Scale**: Vary hand size
- **Noise**: Add landmark noise
- **Lighting**: Simulate different conditions

### Hyperparameter Tuning
- **Random Forest**: n_estimators, max_depth
- **SVM**: C, gamma parameters
- **Neural Network**: hidden layers, learning rate

### Cross-Validation
- **K-Fold**: 5-fold cross-validation
- **Stratified**: Maintain class balance
- **Time Series**: Respect temporal order

## 🚀 Deployment

### Model Export
```python
# Export for TensorFlow.js
import tensorflow as tf

# Convert to TensorFlow.js format
tf.saved_model.save(model, 'saved_models/tfjs_model')
```

### API Integration
```python
# Flask backend integration
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/classify', methods=['POST'])
def classify_gesture():
    landmarks = request.json['landmarks']
    features = feature_extractor(landmarks)
    gesture = model.predict([features])[0]
    confidence = model.predict_proba([features]).max()
    
    return jsonify({
        'gesture': gesture,
        'confidence': float(confidence)
    })
```

## 🔧 Development

### Adding New Gestures
1. Update gesture list in notebooks
2. Collect training data for new gestures
3. Retrain model with expanded dataset
4. Update frontend gesture display

### Model Monitoring
- **Drift Detection**: Monitor prediction accuracy
- **Performance Metrics**: Track model performance
- **Data Quality**: Validate input data

### A/B Testing
- **Model Comparison**: Test different models
- **Feature Engineering**: Experiment with new features
- **Hyperparameter Tuning**: Optimize model parameters

## 🐛 Troubleshooting

### Common Issues
1. **Low Accuracy**: Check data quality and quantity
2. **Overfitting**: Use regularization or more data
3. **Slow Training**: Optimize feature extraction
4. **Memory Issues**: Use batch processing

### Debug Tools
- **Visualization**: Plot confusion matrix
- **Feature Analysis**: Analyze feature importance
- **Error Analysis**: Examine misclassified samples

## 📚 References

- [Mediapipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands.html)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [ASL Gesture Recognition Papers](https://scholar.google.com/)
