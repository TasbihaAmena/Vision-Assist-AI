import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

from object1.main import detect_objects, answer_question
from voice_assistant.voice import speak, extract_object_names


# =========================================================
# DRAW OBJECT DETECTIONS
# =========================================================

def draw_detections(frame, detected_objects):

    for obj in detected_objects:

        name = obj["name"]
        center_x = obj["center_x"]
        center_y = obj["center_y"]

        if "bbox" in obj:

            x1, y1, x2, y2 = obj["bbox"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                name,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                name,
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )


# =========================================================
# SPEAK ANSWER SAFELY
# =========================================================

def speak_answer(answer):

    try:

        speak(answer)

    except Exception as e:

        print("Voice output error:", e)


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(detected_objects):

    object_names = extract_object_names(detected_objects)

    if object_names:

        print("\nDetected:", ", ".join(object_names))

    else:

        print("\nNo objects detected.")

    question = input(
        "\nAsk your question: "
    ).strip()

    if not question:

        print("\nNo question entered.")
        return

    result = answer_question(
        detected_objects,
        question
    )

    answer = result["answer"]

    print("\nAnswer:")
    print(answer)

    # Speak every answer
    speak_answer(answer)


# =========================================================
# OPEN CAMERA
# =========================================================

def open_camera():

    # Try DirectShow first with MJPG
    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if cap.isOpened():

        # Request MJPG format
        cap.set(
            cv2.CAP_PROP_FOURCC,
            cv2.VideoWriter_fourcc(*"MJPG")
        )

    # If DirectShow fails, try normal camera
    if not cap.isOpened():

        cap.release()

        cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        return None

    # Camera resolution
    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    # Try to keep normal colour capture
    cap.set(
        cv2.CAP_PROP_CONVERT_RGB,
        1
    )

    return cap


# =========================================================
# LIVE CAMERA
# =========================================================

def live_camera():

    cap = open_camera()

    if cap is None:

        print("\nError: Could not open camera.")
        return

    print("\n================================")
    print("LIVE CAMERA")
    print("================================")
    print("S = Scan current frame")
    print("Q = Quit camera")
    print("================================")

    window_name = "VISION ASSIST AI - LIVE CAMERA"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        window_name,
        1100,
        700
    )

    while True:

        ret, frame = cap.read()

        if not ret:

            print("Could not read camera frame.")
            break

        # Make sure frame is in normal BGR colour format
        if len(frame.shape) == 2:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_GRAY2BGR
            )

        elif frame.shape[2] == 4:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGRA2BGR
            )

        # Object detection
        detected_objects = detect_objects(frame)

        # Copy for display
        display_frame = frame.copy()

        # Draw boxes
        draw_detections(
            display_frame,
            detected_objects
        )

        # Instructions
        cv2.putText(
            display_frame,
            "S = SCAN    Q = QUIT",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        # Show camera
        cv2.imshow(
            window_name,
            display_frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Scan current frame
        if key == ord("s"):

            print("\n--------------------------------")
            print("Frame scanned.")
            print("--------------------------------")

            ask_question(
                detected_objects
            )

            print("\nCamera resumed.")
            print("Press S to scan again or Q to quit.")

        # Quit
        elif key == ord("q"):

            break

    cap.release()

    cv2.destroyAllWindows()

    print("\nLive Camera Stopped.")


# =========================================================
# SELECT IMAGE
# =========================================================

def select_image():

    root = tk.Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(

        title="Select an Image",

        filetypes=[
            (
                "Image Files",
                "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG"
            ),
            (
                "All Files",
                "*.*"
            )
        ]
    )

    root.destroy()

    if not image_path:

        print("\nNo image selected.")
        return

    print("\nImage selected.")

    try:

        image = cv2.imdecode(
            np.fromfile(
                image_path,
                dtype=np.uint8
            ),
            cv2.IMREAD_COLOR
        )

    except Exception as e:

        print("\nError reading image:")
        print(e)
        return

    if image is None:

        print("\nCould not open selected image.")
        return

    # Object detection
    detected_objects = detect_objects(image)

    # Draw detections
    display_image = image.copy()

    draw_detections(
        display_image,
        detected_objects
    )

    window_name = "VISION ASSIST AI - SELECTED IMAGE"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        window_name,
        1100,
        700
    )

    cv2.imshow(
        window_name,
        display_image
    )

    print("\nImage detection complete.")
    print("Press any key on the image window to continue.")

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    # Ask question
    ask_question(
        detected_objects
    )


# =========================================================
# MAIN MENU
# =========================================================

def main():

    while True:

        print("\n")
        print("========================================")
        print("          VISION ASSIST AI")
        print("========================================")
        print("1. Live Camera")
        print("2. Select Image")
        print("3. Exit")
        print("========================================")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            live_camera()

        elif choice == "2":

            select_image()

        elif choice == "3":

            print("\nVision Assist AI Closed.")
            break

        else:

            print(
                "\nInvalid choice. "
                "Please enter 1, 2 or 3."
            )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    main()