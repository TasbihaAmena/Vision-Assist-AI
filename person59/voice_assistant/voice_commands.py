import speech_recognition as sr
from voice import speak


# Create speech recognizer
recognizer = sr .Recognizer()
def listen_command():
    with sr.Microphone() as source:

        print("Please wait. Adjusting microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        speak("Please say your command now.")

        print("Listening... Speak now.")

        try:
            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

            print("Processing your voice...")

            command = recognizer.recognize_google(audio)

            command = command.lower()

            print("You said:", command)

            return command

        except sr.WaitTimeoutError:
            print("No voice detected within the time limit.")
            speak("I did not hear anything. Please try again.")
            return ""

        except sr.UnknownValueError:
            print("I heard something, but I could not understand it.")
            speak("Sorry, I could not understand your voice.")
            return ""

        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            speak("Speech recognition service is unavailable.")
            return ""

        except Exception as error:
            print("Microphone error:", error)
            speak("There is a problem with the microphone.")
            return ""

def process_command(command):
    """
    Process the recognized voice command.
    """

    if not command:
        return True

    if "help" in command:
        speak(
            "You can say what can you see, read the text, "
            "help, or exit."
        )

    elif "what can you see" in command or "detect objects" in command:
        speak("I will check the objects around you.")

        # Later, connect Person 1's object detection function here.
        # Example:
        # detected_objects = detect_objects()
        # speak_objects(detected_objects)

    elif "read the text" in command or "read text" in command:
        speak("I will read the text.")

        # Later, connect Person 2's OCR function here.
        # Example:
        # detected_text = extract_text()
        # speak_text(detected_text)

    elif "stop" in command or "exit" in command or "quit" in command:
        speak("Voice assistant stopped.")
        return False

    else:
        speak("Sorry, I do not know that command.")

    return True


if __name__ == "__main__":

    speak("Vision Assist AI voice command system is ready.")

    running = True

    while running:
        user_command = listen_command()
        running = process_command(user_command)