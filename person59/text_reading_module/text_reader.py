import truststore
truststore.inject_into_ssl()
import re
import os
import easyocr
import cv2
from PIL import Image


# ==============================
# OCR READER
# ==============================

reader = easyocr.Reader(['en'], gpu=False)


def clean_text(text):
    """Clean OCR detected text."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def read_text(image_path):
    """Read all readable text from an image."""

    if not os.path.exists(image_path):
        print("ERROR: Image file not found.")
        return ""

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Could not open image.")
        return ""

    # OCR detection
    results = reader.readtext(image, detail=1, paragraph=False)

    detected_lines = []

    for result in results:
        text = result[1]

        if text and text.strip():
            detected_lines.append(clean_text(text))

    # Combine all detected text
    full_text = " ".join(detected_lines)

    return full_text


# ==============================
# IMPORTANT WORD DETECTION
# ==============================

def detect_important_words(full_text):

    important_words = [
        "Python",
        "Machine Learning",
        "Data Science",
        "AI",
        "ML",
        "Future",
        "Engineer",
        "Learn",
        "Build",
        "Grow",
        "Dreams",
        "Big Dreams"
    ]

    detected_words = []

    text_lower = full_text.lower()

    for word in important_words:

        word_lower = word.lower()

        if word_lower in text_lower:
            detected_words.append(word)

    return detected_words


# ==============================
# MAIN TESTING
# ==============================

if __name__ == "__main__":

    image_path = "text_image.jpg"

    print("\n===================================")
    print("       OCR TEXT READING MODULE")
    print("===================================\n")

    full_text = read_text(image_path)

    # Check whether readable text exists
    if not full_text:

        print("NO READABLE TEXT FOUND.")
        print("Please use an image containing clear text.")

    else:

        print("===== ALL DETECTED TEXT =====")
        print(full_text)

        print("\n===== CLEAN TEXT =====")
        cleaned_text = clean_text(full_text)
        print(cleaned_text)

        print("\n===== IMPORTANT WORDS DETECTED =====")

        detected_words = detect_important_words(cleaned_text)

        if detected_words:

            for word in detected_words:
                print("Detected:", word)

        else:

            print("No important words detected.")

        print("\n===================================")
        print("OCR TEXT READING COMPLETED")
        print("===================================")     # ==============================
# TEXT TO SPEECH
# ==============================

import pyttsx3


def speak_text(text):
    """Convert detected text into speech."""

    if not text:
        print("No text available for speech.")
        return

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    print("\n===== TEXT TO SPEECH =====")
    print("Speaking detected text...")

    engine.say(text)
    engine.runAndWait()

    print("TEXT TO SPEECH COMPLETED")


# ==============================
# RUN TEXT TO SPEECH
# ==============================

try:
    speak_text(full_text)
except Exception as e:
    print("Text-to-Speech Error:", e)