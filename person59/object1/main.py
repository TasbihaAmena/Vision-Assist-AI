from ultralytics import YOLO
import math
from pathlib import Path 

model=YOLO(Path(__file__).parent / "yolo11n.pt")


def detect_objects(image):
    results = model(image, verbose=False)
    result = results[0]

    detected_objects = []

    for box in result.boxes:
        class_id = int(box.cls[0])
        name = model.names[class_id]

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        detected_objects.append({
            "name": name,
            "center_x": center_x,
            "center_y": center_y
        })

    return detected_objects


def answer_question(detected_objects, question):
    question = question.lower()

    reference = None

    for obj in detected_objects:
        if obj["name"] in question:
            reference = obj
            break

    if reference is None:
        return {
            "reference": None,
            "relation": "unknown",
            "answer_objects": [],
            "answer": "I could not find the object you asked about."
        }

    reference_object = reference["name"]
    answer_objects = []
    relation = "unknown"

    if "left" in question:
        relation = "left"

        for obj in detected_objects:
            if obj["name"] == reference_object:
                continue

            if obj["center_x"] < reference["center_x"]:
                answer_objects.append(obj["name"])

    elif "right" in question:
        relation = "right"

        for obj in detected_objects:
            if obj["name"] == reference_object:
                continue

            if obj["center_x"] > reference["center_x"]:
                answer_objects.append(obj["name"])

    elif "near" in question or "paas" in question:
        relation = "near"

        for obj in detected_objects:
            if obj["name"] == reference_object:
                continue

            dx = obj["center_x"] - reference["center_x"]
            dy = obj["center_y"] - reference["center_y"]

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 400:
                answer_objects.append(obj["name"])

    else:
        return {
            "reference": reference_object,
            "relation": "unknown",
            "answer_objects": [],
            "answer": "Please ask about left, right, or near."
        }

    if answer_objects:
        answer = (
            f"The objects {relation} the {reference_object} are: "
            + ", ".join(answer_objects)
        )
    else:
        answer = (
            f"There are no detected objects {relation} the "
            f"{reference_object}."
        )

    return {
        "reference": reference_object,
        "relation": relation,
        "answer_objects": answer_objects,
        "answer": answer
    }


if __name__ == "__main__":

    image_path = (
        "test_images/"
        "WhatsApp Image 2026-09-14 at 12.12.05 PM copy.jpeg"
    )

    detected_objects = detect_objects(image_path)

    print("\nDetected objects:")

    for obj in detected_objects:
        print(obj)

    question = input("\nAsk a question: ")

    result = answer_question(detected_objects, question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nIntegration-ready data:")
    print(result)

    print("\nObject Detection Module Ready!")