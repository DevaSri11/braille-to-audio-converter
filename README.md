<h1 align="center">Braille to Audio Converter</h1>


An assistive technology system that converts **Braille text into readable text and audio output**, enabling visually impaired users to access written information through speech.
This project combines **Computer Vision**, **Machine Learning**, and **Text-to-Speech (TTS)** to automate the conversion of Braille content into audio.

---
<img width="911" height="905" alt="Screenshot 2026-01-06 223541" src="https://github.com/user-attachments/assets/3f8d6d92-f360-4132-850f-be5f9225a311" />
<hr>

## Problem Statement

Visually impaired individuals rely on Braille for reading, but face challenges such as:

<ul>
  <li><b>Limited access to Braille translators</b></li>
  <li><b>Difficulty in converting physical Braille into digital content</b></li>
  <li><b>Lack of affordable assistive tools</b></li>
  <li><b>Time-consuming manual interpretation</b></li>
</ul>

<b>Goal:</b>
<ul>
  <li>Automatically recognize Braille characters from images</li>
  <li>Convert Braille patterns into readable text</li>
  <li>Generate clear audio output for easy understanding</li>
</ul>

---

## What is Braille Recognition in This Project?

Braille recognition involves:

<ul>
  <li>Detecting raised dot patterns from a Braille image</li>
  <li>Interpreting dot combinations using machine learning</li>
  <li>Mapping detected patterns to corresponding characters</li>
</ul>

Each Braille character is identified based on its **dot configuration**.

---

## System Overview

<ul>
  <li><b>Input:</b> Image containing Braille text</li>
  <li><b>Processing:</b> Image preprocessing + Braille pattern recognition</li>
  <li><b>Conversion:</b> Braille to text mapping</li>
  <li><b>Output:</b> Audio generation using Text-to-Speech</li>
</ul>

---

## Technologies Used

<ul>
  <li><b>Programming Language:</b> Python</li>
  <li><b>Image Processing:</b> OpenCV</li>
  <li><b>Machine Learning:</b> CNN (TensorFlow / Keras)</li>
  <li><b>Pattern Recognition:</b> Braille dot classification</li>
  <li><b>Audio Output:</b> Text-to-Speech (TTS)</li>
</ul>

---

## Key Features

<ul>
  <li>Automatic detection of Braille characters from images</li>
  <li>Image preprocessing for noise removal and clarity</li>
  <li>Accurate Braille pattern recognition using CNN</li>
  <li>Conversion of Braille patterns into readable text</li>
  <li>Clear and understandable audio output</li>
</ul>

---

## System Workflow

<ul>
  <li>Upload or capture a Braille image</li>
  <li>Convert image to grayscale and apply preprocessing</li>
  <li>Detect and segment Braille dots</li>
  <li>Classify Braille characters using CNN</li>
  <li>Convert recognized characters into text</li>
  <li>Generate audio output using Text-to-Speech</li>
</ul>

---

## Single Input Conversion

For a given Braille image, the system provides:
<ul>
  <li>Recognized Braille characters</li>
  <li>Converted readable text</li>
  <li>Audio output of the recognized text</li>
</ul>

---

## Folder Structure

<pre>
Braille-to-Audio-Converter/
│
├── dataset/
│   └── braille_images/
│
├── model/
│   └── braille_cnn_model.h5
│
├── src/
│   ├── preprocess.py
│   ├── detect_dots.py
│   ├── braille_to_text.py
│   └── text_to_audio.py
│
├── main.py
├── requirements.txt
└── README.md
</pre>

---

## Code Explanation & Usage

The main logic of the project is executed from `main.py`.  
It processes a Braille image, converts it into text, and generates audio output.

### Sample Code (`main.py`)

```python
import cv2
from braille_to_text import convert_braille_to_text
from text_to_audio import text_to_speech

# Load Braille image
image = cv2.imread("sample_braille.jpg")

# Convert Braille image to text
recognized_text = convert_braille_to_text(image)
print("Recognized Text:", recognized_text)

# Convert text to audio
text_to_speech(recognized_text)

```
## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/braille-to-audio-converter.git
   cd braille-to-audio-converter

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
3. **Run the Application**
   ```bash
   python main.py

