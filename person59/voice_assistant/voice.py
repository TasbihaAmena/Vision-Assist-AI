
import pyttsx3
from collections import Counter


# ==================================================
# 1. INITIALIZE TEXT-TO-SPEECH ENGINE
# ==================================================

engine = pyttsx3.init()

# Speech speed
# Lower value = slower speech
# Higher value = faster speech
engine.setProperty("rate", 150)

# Volume range: 0.0 to 1.0
engine.setProperty("volume", 1.0)

# Select the first available voice
voices = engine.getProperty("voices")

if len(voices) > 0:
    engine.setProperty("voice", voices[0].id)


# ==================================================
# 2. BASIC SPEAK FUNCTION
# ==================================================


def speak(text):
    if text is None:
        return

    text = str(text).strip()
    if text == "":
        return

    print("Assistant:", text)

    try:
        speech_engine = pyttsx3.init()
        speech_engine.setProperty("rate", 150)
        speech_engine.setProperty("volume", 1.0)

        speech_engine.say(text)
        speech_engine.runAndWait()
        speech_engine.stop()

    except Exception as error:
        print("Speech error:", error)
# ==================================================
# 3. EXTRACT OBJECT NAMES
# ==================================================

def extract_object_names(objects):
    """
    Extracts object names from Person 1's output.

    Person 1 may send data like:

    [
        {
            "name": "person",
            "center_x": 447,
            "center_y": 342,
            "confidence": 0.52
        },
        {
            "name": "cell phone",
            "center_x": 410,
            "center_y": 259,
            "confidence": 0.76
        }
    ]

    This function returns:

    ["person", "cell phone"]
    """

    object_names = []

    if not objects:
        return object_names

    for obj in objects:

        # If Person 1 sends a dictionary
        if isinstance(obj, dict):
            name = obj.get("name")

            if name:
                object_names.append(str(name).strip())

        # If Person 1 sends only object names as strings
        elif isinstance(obj, str):
            object_names.append(obj.strip())

    return object_names


# ==================================================
# 4. SPEAK OBJECTS DETECTED BY PERSON 1
# ==================================================

def speak_objects(objects):
    """
    Speaks the objects detected by Person 1.

    It accepts either:

    1. A list of dictionaries
    2. A list of object-name strings
    """

    object_names = extract_object_names(objects)

    if not object_names:
        speak("I cannot detect any objects.")
        return

    # Count repeated objects
    # Example:
    # ["person", "cell phone", "cell phone", "book", "book"]
    # becomes:
    # person = 1
    # cell phone = 2
    # book = 2

    object_counts = Counter(object_names)

    spoken_objects = []

    for name, count in object_counts.items():

        if count == 1:
            spoken_objects.append(name)

        else:
            # Special plural handling
            if name == "cell phone":
                spoken_objects.append(f"{count} cell phones")

            elif name == "potted plant":
                spoken_objects.append(f"{count} potted plants")

            elif name == "person":
                spoken_objects.append(f"{count} people")

            elif name == "book":
                spoken_objects.append(f"{count} books")

            else:
                spoken_objects.append(f"{count} {name}s")

    # Create a natural sentence
    if len(spoken_objects) == 1:

        message = f"I can see {spoken_objects[0]}."

    elif len(spoken_objects) == 2:

        message = (
            f"I can see {spoken_objects[0]} "
            f"and {spoken_objects[1]}."
        )

    else:

        object_text = ", ".join(spoken_objects[:-1])

        message = (
            f"I can see {object_text}, "
            f"and {spoken_objects[-1]}."
        )

    speak(message)


# ==================================================
# 5. SPEAK TEXT RECEIVED FROM PERSON 2
# ==================================================

def speak_text(text):
    """
    Speaks the text extracted by Person 2's OCR module.

    Example:
        speak_text("Welcome to Vision Assist AI.")
    """

    if text is None or str(text).strip() == "":
        speak("I could not read any text.")
        return

    speak(f"The text says: {text}")


# ==================================================
# 6. TEST THE COMPLETE VOICE MODULE
# ==================================================

if __name__ == "__main__":

    speak("Vision Assist AI is working. I can see a person, a bottle, and a laptop, chair, potted plant, cell phones and 4 books.The text says: small steps big dreams, learn build grow, you can do it, future ai ml engineer, better days ahead")