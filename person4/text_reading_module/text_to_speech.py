import pyttsx3

# ==============================
# TEXT TO SPEECH MODULE
# ==============================

def speak_text(text):
    if not text:
        print("No text available to speak.")
        return

    print("Speaking detected text...")

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()

    print("TEXT TO SPEECH COMPLETED")


# ==============================
# TEST
# ==============================

if __name__ == "__main__":

    test_text = "Hello. This is the AI Vision Assistant text reading module."

    print("==============================")
    print("     TEXT TO SPEECH MODULE")
    print("==============================")

    speak_text(test_text)