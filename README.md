# braille-to-audio-converter

## Braille Dataset

The dataset is hosted externally on Google Drive. To download and extract it, run:

```bash
pip install gdown
python dataset.py

Braille to Audio Converter
📌 Project Overview

The Braille to Audio Converter is an assistive technology project designed to help visually impaired individuals access Braille content through audio output. The system captures Braille text in image form, recognizes Braille dot patterns using image processing and machine learning techniques, converts them into readable text, and finally generates corresponding speech using Text-to-Speech (TTS).

📌 Features

Detects Braille characters from input images
Uses image preprocessing techniques to enhance Braille dot recognition
Converts recognized Braille patterns into readable text
Generates clear audio output using Text-to-Speech
Designed to work under different lighting and image quality conditions

📌 Technologies Used

Python – core programming language
OpenCV – image preprocessing and Braille dot detection
TensorFlow / CNN – Braille character classification
OCR / Pattern Recognition – text conversion
Text-to-Speech (TTS) – audio generation

📌 System Workflow

Input Braille image is captured or uploaded
Image preprocessing is applied (grayscale, noise removal, thresholding)
Braille dot patterns are detected and segmented
CNN model classifies Braille characters
Recognized text is converted into audio output
Audio is played for the user
