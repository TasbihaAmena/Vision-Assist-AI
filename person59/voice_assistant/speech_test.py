import speech_recognition as sr

# Create the recognizer object
recognizer = sr.Recognizer()

print("Speech recognition test started.")
print("Please speak after the microphone starts listening.")


# Open the microphone
with sr.Microphone() as source:

    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening now. Please speak...")

    try:
        # Listen to the user's voice
        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

        print("Processing your voice...")

        # Convert speech into text
        text = recognizer.recognize_google(audio)

        print("You said:", text)

    except sr.WaitTimeoutError:
        print("No speech detected. Please try again.")

    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")

    except sr.RequestError:
        print("Speech recognition service is unavailable.")

print("Speech recognition test completed.")