import React, { useState, useEffect } from 'react'

const GestureDisplay = ({ gesture, confidence, isDetecting }) => {
  const [gestureHistory, setGestureHistory] = useState([])
  const [gestureStats, setGestureStats] = useState({})
  const getConfidenceColor = (conf) => {
    if (conf >= 0.8) return 'text-green-400'
    if (conf >= 0.6) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getConfidenceText = (conf) => {
    if (conf >= 0.8) return 'High'
    if (conf >= 0.6) return 'Medium'
    return 'Low'
  }

  // Update gesture history and stats
  useEffect(() => {
    if (gesture && gesture !== 'none' && confidence > 0.5) {
      const newEntry = {
        gesture,
        confidence,
        timestamp: new Date().toLocaleTimeString()
      }
      
      setGestureHistory(prev => [newEntry, ...prev.slice(0, 9)]) // Keep last 10
      
      setGestureStats(prev => ({
        ...prev,
        [gesture]: (prev[gesture] || 0) + 1
      }))
    }
  }, [gesture, confidence])

  return (
    <div className="space-y-6">
      {/* Main Gesture Display */}
      <div className="text-center">
        <div className="text-8xl font-bold text-gradient mb-4">
          {gesture || '?'}
        </div>
        <p className="text-gray-400 text-lg">
          {gesture ? `Detected: ${gesture}` : 'No gesture detected'}
        </p>
      </div>

      {/* Confidence Meter */}
      {gesture && (
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-400">Confidence</span>
            <span className={`text-sm font-medium ${getConfidenceColor(confidence)}`}>
              {getConfidenceText(confidence)} ({Math.round(confidence * 100)}%)
            </span>
          </div>
          <div className="w-full bg-dark-border rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-300 ${
                confidence >= 0.8 ? 'bg-green-400' : 
                confidence >= 0.6 ? 'bg-yellow-400' : 'bg-red-400'
              }`}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Status */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-400">Status</span>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              isDetecting ? 'bg-green-400 animate-pulse' : 'bg-gray-500'
            }`} />
            <span className="text-sm font-medium">
              {isDetecting ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>
      </div>

      {/* Supported Gestures */}
      <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
        <h4 className="text-sm font-medium text-white mb-3">Supported Gestures</h4>
        <div className="grid grid-cols-5 gap-2">
          {['A', 'B', 'C', 'D', 'E'].map((letter) => (
            <div
              key={letter}
              className={`text-center p-2 rounded-lg border transition-colors ${
                gesture === letter
                  ? 'bg-accent border-accent text-white'
                  : 'bg-dark-bg border-dark-border text-gray-400'
              }`}
            >
              <div className="text-lg font-bold">{letter}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Gesture History */}
      {gestureHistory.length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
          <h4 className="text-sm font-medium text-white mb-3">Recent Gestures</h4>
          <div className="space-y-2">
            {gestureHistory.slice(0, 5).map((entry, index) => (
              <div key={index} className="flex justify-between items-center text-sm">
                <span className="text-white font-bold">{entry.gesture}</span>
                <span className="text-gray-400">{entry.timestamp}</span>
                <span className={`text-xs ${getConfidenceColor(entry.confidence)}`}>
                  {Math.round(entry.confidence * 100)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Gesture Statistics */}
      {Object.keys(gestureStats).length > 0 && (
        <div className="bg-dark-surface border border-dark-border rounded-lg p-4">
          <h4 className="text-sm font-medium text-white mb-3">Gesture Statistics</h4>
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(gestureStats).map(([gesture, count]) => (
              <div key={gesture} className="text-center">
                <div className="text-lg font-bold text-accent">{gesture}</div>
                <div className="text-sm text-gray-400">{count}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default GestureDisplay

