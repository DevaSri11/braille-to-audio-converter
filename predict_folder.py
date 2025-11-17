# import os
# import cv2
# import numpy as np
# import tensorflow as tf
# from gtts import gTTS
# import pygame

# # ====== Paths ======
# MODEL_PATH = r"C:\Users\DevaSri\braille-to-audio\src\braille_model.h5"
# FOLDER_PATH = r"C:\Users\DevaSri\braille-to-audio\data\Braille Dataset\A"
# # ===================

# # Load the trained model
# model = tf.keras.models.load_model(MODEL_PATH)

# # Class labels (A–Z)
# CLASSES = [chr(i) for i in range(65, 91)]

# # Preprocess each image
# def preprocess_image(img_path):
#     img = cv2.imread(img_path)
#     if img is None:
#         raise FileNotFoundError(f"Image not found: {img_path}")
#     img = cv2.resize(img, (64, 64))
#     img = img / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img

# # Predict one Braille image
# def predict_character(img_path):
#     img = preprocess_image(img_path)
#     preds = model.predict(img)
#     idx = np.argmax(preds)
#     return CLASSES[idx]

# # Read all images in folder and form text
# def predict_folder(folder_path):
#     images = sorted([
#         os.path.join(folder_path, f)
#         for f in os.listdir(folder_path)
#         if f.lower().endswith(('.jpg', '.jpeg', '.png'))
#     ])

#     if not images:
#         print("⚠️ No Braille images found in the folder.")
#         return ""

#     predicted_text = ""
#     for img_path in images:
#         letter = predict_character(img_path)
#         print(f"🖼 {os.path.basename(img_path)} -> {letter}")
#         predicted_text += letter

#     print(f"\n✅ Full predicted text: {predicted_text}")
#     return predicted_text

# # Convert text to speech
# def speak_text(text):
#     tts = gTTS(f"The Braille text is {text}")
#     audio_path = os.path.join(os.getcwd(), "braille_output.mp3")
#     tts.save(audio_path)
#     pygame.mixer.init()
#     pygame.mixer.music.load(audio_path)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pass
#     pygame.quit()

# if __name__ == "__main__":
#     text = predict_folder(FOLDER_PATH)
#     if text:
#         speak_text(text)

# output saved as mp3 file
# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import pygame

# # ---------------- CONFIG ----------------
# MODEL_PATH = r"C:\Users\DevaSri\braille-to-audio\src\braille_model.h5"
# DATASET_ROOT = r"C:\Users\DevaSri\braille-to-audio\data\Braille Dataset"
# IMG_SIZE = (64, 64)                        # image size used in training
# # ----------------------------------------

# # Initialize pygame mixer for audio playback
# pygame.mixer.init()

# # Load trained model
# print("🔁 Loading model...")
# model = load_model(MODEL_PATH)
# print("✅ Model loaded successfully!\n")

# # Function to predict a single character
# def predict_character(img_path):
#     # Load image in RGB mode (fix for 3-channel input)
#     img = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE, color_mode='rgb')
#     img = tf.keras.utils.img_to_array(img)
#     img = np.expand_dims(img, axis=0) / 255.0  # normalize

#     # Predict class
#     pred = model.predict(img, verbose=0)
#     predicted_label = np.argmax(pred, axis=1)[0]

#     # Convert numeric label to corresponding letter (A–Z)
#     letter = chr(predicted_label + ord('A'))
#     print(f"🖼 {os.path.basename(img_path)} -> {letter}")
#     return letter

# # Function to process all folders in the dataset
# def predict_from_all_folders(dataset_root):
#     full_text = ""

#     for folder_name in sorted(os.listdir(dataset_root)):
#         folder_path = os.path.join(dataset_root, folder_name)

#         if not os.path.isdir(folder_path):
#             continue

#         print(f"\n📁 Processing folder: {folder_name}")

#         # Predict for all images inside folder
#         folder_text = ""
#         for filename in sorted(os.listdir(folder_path)):
#             if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 img_path = os.path.join(folder_path, filename)
#                 letter = predict_character(img_path)
#                 folder_text += letter

#         print(f"📝 Predicted text for folder {folder_name}: {folder_text}")
#         full_text += folder_text

#     print("\n✅ Full predicted text:", full_text)
#     return full_text

# # Function to speak out the predicted text
# def speak_text(text):
#     from gtts import gTTS
#     tts = gTTS(text)
#     tts.save("braille_audio.mp3")
#     pygame.mixer.music.load("braille_audio.mp3")
#     pygame.mixer.music.play()
#     print("\n🔊 Speaking the predicted text...")

# # -------------- MAIN EXECUTION --------------
# if __name__ == "__main__":
#     text = predict_from_all_folders(DATASET_ROOT)
#     speak_text(text)

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from gtts import gTTS
import pygame
import time

# ---------------- CONFIG ---------------- #
MODEL_PATH = r"C:\Users\DevaSri\braille-to-audio\src\braille_model.h5"
DATASET_ROOT = r"C:\Users\DevaSri\braille-to-audio\data\Braille Dataset"
CONFIDENCE_THRESHOLD = 0.60  # only accept predictions above this confidence
IMG_SIZE = (64, 64)
# ---------------------------------------- #

# Classes must match the order during training
CLASSES = sorted(os.listdir(DATASET_ROOT))
print("Loaded Classes:", CLASSES)

# Initialize Pygame for speech playback
pygame.mixer.init()

# Load trained model
print("🔁 Loading model...")
model = load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# ---------------- HELPER FUNCTIONS ---------------- #

def preprocess_image(img_path):
    """Load and preprocess a single image."""
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def predict_letter_variants(variant_images):
    """Average predictions from multiple image variants (rot, dim, etc.)"""
    predictions = []
    for img_path in variant_images:
        img_array = preprocess_image(img_path)
        pred = model.predict(img_array, verbose=0)[0]
        predictions.append(pred)

    # Average predictions
    avg_pred = np.mean(predictions, axis=0)
    max_conf = np.max(avg_pred)
    predicted_idx = np.argmax(avg_pred)

    if max_conf < CONFIDENCE_THRESHOLD:
        return "_", max_conf
    else:
        return CLASSES[predicted_idx], max_conf

def predict_from_all_folders(dataset_root):
    """Predict all Braille folders and combine output text."""
    full_text = ""

    for folder_name in sorted(os.listdir(dataset_root)):
        folder_path = os.path.join(dataset_root, folder_name)
        if not os.path.isdir(folder_path):
            continue

        print(f"\n📁 Processing folder: {folder_name}")
        folder_predictions = []
        images = sorted(os.listdir(folder_path))

        # Group by base filename (before 'rot', 'dim', etc.)
        grouped = {}
        for img_file in images:
            base = ''.join([c for c in img_file if not c.isdigit()])[:2]  # e.g. "a1"
            grouped.setdefault(base, []).append(os.path.join(folder_path, img_file))

        for base, variant_imgs in grouped.items():
            letter, conf = predict_letter_variants(variant_imgs)
            print(f"🖼 {os.path.basename(variant_imgs[0])} -> {letter} ({conf:.2f})")
            folder_predictions.append(letter)

        text_for_folder = ''.join(folder_predictions)
        print(f"📝 Predicted text for folder {folder_name}: {text_for_folder}")
        full_text += text_for_folder

    print("\n✅ Full predicted text:", full_text)
    return full_text

# def speak_text(text):
#     """Convert predicted text to speech (play immediately)."""
#     if not text.strip():
#         print("⚠️ No valid text to speak.")
#         return

#     tts = gTTS(text=text, lang='en')
#     tts.save("temp_output.mp3")

#     pygame.mixer.music.load("temp_output.mp3")
#     pygame.mixer.music.play()

#     # Wait until playback finishes
#     while pygame.mixer.music.get_busy():
#         time.sleep(0.5)

#     os.remove("temp_output.mp3")
def speak_text(text):
    try:
        print("\n🔊 Speaking output...")
        tts = gTTS(text=text, lang='en')
        tts.save("temp_output.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("temp_output.mp3")
        pygame.mixer.music.play()

        # Wait until audio playback completes
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)

        pygame.mixer.music.unload()  # release file
        os.remove("temp_output.mp3")  # now safe to delete
        print("✅ Done speaking!\n")

    except Exception as e:
        print(f"⚠️ Error in audio playback: {e}")

def evaluate_model_accuracy(test_dir):
    """Evaluate model accuracy if you have a test set directory."""
    test_gen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    test_data = test_gen.flow_from_directory(
        test_dir,
        target_size=IMG_SIZE,
        batch_size=32,
        class_mode='categorical'
    )
    loss, acc = model.evaluate(test_data)
    print(f"📊 Test Accuracy: {acc * 100:.2f}% | Loss: {loss:.4f}")

# ---------------- MAIN EXECUTION ---------------- #
if __name__ == "__main__":
    # Optional: Uncomment this if you have a 'Braille_Test' folder
    # evaluate_model_accuracy(r"C:\Users\DevaSri\braille-to-audio\Braille_Test")

    text = predict_from_all_folders(DATASET_ROOT)
    speak_text(text)
