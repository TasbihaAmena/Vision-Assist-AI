import pyttsx3
from collections import Counter


# ==================================================
# TEXT TO SPEECH
# ==================================================

def speak(text):

    if text is None:
        return

    text = str(text).strip()

    if text == "":
        return

    print("Assistant:", text)

    speech_engine = None

    try:

        # Create a fresh engine for EVERY speech
        speech_engine = pyttsx3.init()

        speech_engine.setProperty(
            "rate",
            150
        )

        speech_engine.setProperty(
            "volume",
            1.0
        )

        # Select available voice
        voices = speech_engine.getProperty("voices")

        if voices:
            speech_engine.setProperty(
                "voice",
                voices[0].id
            )

        # Speak
        speech_engine.say(text)

        speech_engine.runAndWait()

        # Stop engine completely
        speech_engine.stop()

        # Give Windows TTS a moment to release
        del speech_engine

    except Exception as error:

        print("Speech error:", error)

        try:

            if speech_engine is not None:
                speech_engine.stop()

        except:
            pass


# ==================================================
# EXTRACT OBJECT NAMES
# ==================================================

def extract_object_names(objects):

    object_names = []

    if not objects:
        return object_names

    for obj in objects:

        if isinstance(obj, dict):

            name = obj.get("name")

            if name:
                object_names.append(
                    str(name).strip()
                )

        elif isinstance(obj, str):

            object_names.append(
                obj.strip()
            )

    return object_names


# ==================================================
# SPEAK OBJECTS
# ==================================================

def speak_objects(objects):

    object_names = extract_object_names(objects)

    if not object_names:

        speak(
            "I cannot detect any objects."
        )

        return

    object_counts = Counter(
        object_names
    )

    spoken_objects = []

    for name, count in object_counts.items():

        if count == 1:

            spoken_objects.append(name)

        else:

            if name == "cell phone":

                spoken_objects.append(
                    f"{count} cell phones"
                )

            elif name == "potted plant":

                spoken_objects.append(
                    f"{count} potted plants"
                )

            elif name == "person":

                spoken_objects.append(
                    f"{count} people"
                )

            elif name == "book":

                spoken_objects.append(
                    f"{count} books"
                )

            else:

                spoken_objects.append(
                    f"{count} {name}s"
                )

    if len(spoken_objects) == 1:

        message = (
            f"I can see {spoken_objects[0]}."
        )

    elif len(spoken_objects) == 2:

        message = (
            f"I can see {spoken_objects[0]} "
            f"and {spoken_objects[1]}."
        )

    else:

        object_text = ", ".join(
            spoken_objects[:-1]
        )

        message = (
            f"I can see {object_text}, "
            f"and {spoken_objects[-1]}."
        )

    speak(message)


# ==================================================
# SPEAK OCR TEXT
# ==================================================

def speak_text(text):

    if text is None or str(text).strip() == "":

        speak(
            "I could not read any text."
        )

        return

    speak(
        f"The text says: {text}"
    )


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    speak("Vision Assist AI is working.")

    speak("I can see a person and a laptop.")

    speak("The objects near the laptop are a book and a bottle.")

    speak("The second speech test is working.")

    speak("The third speech test is working.")