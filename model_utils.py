# src/model_utils.py
import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model

MODEL_PATH = os.path.join(os.path.dirname(__file__), "braille_model.h5")

def load_model_and_labels():
    # Load the keras model and define labels
    model = load_model(MODEL_PATH)
    # labels are A-Z
    labels = [chr(i) for i in range(65, 91)]
    return model, labels

def preprocess_for_model(img_path, target_size=(64,64)):
    # Read as color and resize to target size used in training
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(img_path)
    # ensure RGB
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    return img

def predict_single(img_path, model, labels):
    img = preprocess_for_model(img_path)
    img_arr = np.expand_dims(img, axis=0)
    probs = model.predict(img_arr)[0]
    idx = int(np.argmax(probs))
    letter = labels[idx]
    confidence = float(np.max(probs))
    return {"filename": os.path.basename(img_path), "letter": letter, "confidence": round(confidence, 3)}

def predict_images_batch(img_paths, model, labels):
    preds = []
    # predict one-by-one (you can batch for speed)
    for p in img_paths:
        try:
            res = predict_single(p, model, labels)
        except Exception as e:
            res = {"filename": os.path.basename(p), "letter": "?", "confidence": 0.0}
        preds.append(res)
    return preds
