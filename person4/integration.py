import cv2
import threading
import queue
import time
import speech_recognition as sr

from object1.main import detect_objects, answer_question
from voice_assistant.voice import speak


# ==============================
# VOICE COMMAND SYSTEM
# ==============================

command_queue = queue.Queue()
running = True


def listen_for_commands():
    """
    Continuously listens for voice commands.
    Commands are placed into command_queue.
    """

    recognizer = sr.Recognizer()

    try:
        microphone = sr.Microphone()
    except Exception as e:
        print("Microphone error:", e)
        return

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while running:

        try:
            with microphone as source:
                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=5
                )

            command = recognizer.recognize_google(audio)

            command = command.lower().strip()

            if command:
                command_queue.put(command)

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except sr.RequestError:
            continue

        except Exception:
            continue


# ==============================
# SPEECH
# ==============================

def say(text):
    """
    Speaks the answer.
    No terminal answer is required.
    """

    try:
        speak(text)
    except Exception as e:
        print("Voice error:", e)


# ==============================
# OBJECT SUMMARY
# ==============================

def create_scene_summary(detected_objects):

    if not detected_objects:
        return "I cannot detect any objects right now."

    counts = {}

    for obj in detected_objects:

        name = obj["name"]

        if name in counts:
            counts[name] += 1
        else:
            counts[name] = 1

    parts = []

    for name, count in counts.items():

        if count == 1:
            parts.append(f"one {name}")
        else:
            parts.append(f"{count} {name}s")

    if len(parts) == 1:
        return "I can see " + parts[0] + "."

    if len(parts) == 2:
        return "I can see " + parts[0] + " and " + parts[1] + "."

    return "I can see " + ", ".join(parts[:-1]) + ", and " + parts[-1] + "."


# ==============================
# SCENE SIGNATURE
# ==============================

def get_scene_signature(detected_objects):

    """
    Creates a simple signature so the AI
    does not speak the same detection every frame.
    """

    counts = {}

    for obj in detected_objects:

        name = obj["name"]

        if name in counts:
            counts[name] += 1
        else:
            counts[name] = 1

    return tuple(sorted(counts.items()))


# ==============================
# VOICE QUESTION PROCESSING
# ==============================

def process_voice_command(command, detected_objects):

    global running

    print("Voice command received:", command)

    # Stop commands

    if (
        "stop camera" in command
        or "close camera" in command
        or "quit camera" in command
        or command == "exit"
    ):

        say("Stopping the camera.")

        running = False

        return "STOP"

    # Scene commands

    if (
        "what do you see" in command
        or "what can you see" in command
        or "describe the scene" in command
        or "what is around me" in command
    ):

        answer = create_scene_summary(detected_objects)

        say(answer)

        return "DONE"

    # Person counting

    if (
        "how many people" in command
        or "how many persons" in command
        or "count people" in command
        or "count persons" in command
    ):

        person_count = 0

        for obj in detected_objects:

            if obj["name"] == "person":
                person_count += 1

        if person_count == 0:
            answer = "I cannot see any person."

        elif person_count == 1:
            answer = "I can see one person."

        else:
            answer = f"I can see {person_count} persons."

        say(answer)

        return "DONE"

    # Generic visual question
    # Example:
    # "What is on the left of laptop?"

    try:

        result = answer_question(
            detected_objects,
            command
        )

        answer = result["answer"]

        say(answer)

    except Exception:

        say(
            "Sorry, I could not understand that visual question."
        )

    return "DONE"


# ==============================
# CAMERA
# ==============================

def open_camera():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():

        cap.release()

        cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    return cap


# ==============================
# DRAW OBJECTS
# ==============================

def draw_detections(frame, detected_objects):

    for obj in detected_objects:

        name = obj["name"]
        confidence = obj.get("confidence", 0)

        x1, y1, x2, y2 = obj["bbox"]

        label = f"{name} {confidence:.2f}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


# ==============================
# LIVE CAMERA
# ==============================

def live_camera():

    global running

    running = True

    cap = open_camera()

    if cap is None:

        say("I could not open the camera.")

        return

    # Start voice listener

    listener_thread = threading.Thread(
        target=listen_for_commands,
        daemon=True
    )

    listener_thread.start()

    say("Camera is now active. I am looking at the scene.")

    previous_signature = None

    last_announcement_time = 0

    announcement_cooldown = 5

    while running:

        ret, frame = cap.read()

        if not ret:
            break

        # ==========================
        # YOLO DETECTION
        # ==========================

        detected_objects = detect_objects(frame)

        # ==========================
        # DRAW DETECTIONS
        # ==========================

        display_frame = frame.copy()

        draw_detections(
            display_frame,
            detected_objects
        )

        # ==========================
        # SCENE CHANGE DETECTION
        # ==========================

        current_signature = get_scene_signature(
            detected_objects
        )

        current_time = time.time()

        if (
            current_signature != previous_signature
            and current_time - last_announcement_time
            > announcement_cooldown
        ):

            scene_description = create_scene_summary(
                detected_objects
            )

            say(scene_description)

            previous_signature = current_signature

            last_announcement_time = current_time

        # ==========================
        # CAMERA WINDOW
        # ==========================

        cv2.putText(
            display_frame,
            "VOICE MODE ACTIVE",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        cv2.putText(
            display_frame,
            "Speak your question | Say STOP CAMERA to exit",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        cv2.imshow(
            "VISION ASSIST AI",
            display_frame
        )

        # ==========================
        # VOICE COMMAND PROCESSING
        # ==========================

        while not command_queue.empty():

            command = command_queue.get()

            result = process_voice_command(
                command,
                detected_objects
            )

            if result == "STOP":

                running = False

                break

        # Emergency keyboard exit only

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            running = False

            break

    cap.release()

    cv2.destroyAllWindows()

    say("Camera stopped.")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    live_camera()