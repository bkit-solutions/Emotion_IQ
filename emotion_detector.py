import os
import cv2
from typing import Optional
from fer import FER

# Disable GPU (safe for CPU systems)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Initialize FER detector
detector = FER(mtcnn=False)

def detect_emotion(image_path: str) -> Optional[str]:
    """Return the top detected emotion, or None if no face/emotion detected."""
    
    img = cv2.imread(image_path)
    
    if img is None:
        return None  # Image not found or unreadable

    detected_emotions = detector.detect_emotions(img)

    if not detected_emotions:
        return None  # No face detected

    # Get dominant emotion from first detected face
    emotions = detected_emotions[0]['emotions']
    top_emotion = max(emotions, key=emotions.get)

    return top_emotion
