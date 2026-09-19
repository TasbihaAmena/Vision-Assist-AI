from ultralytics import YOLO
import math

model = YOLO("yolo11n.pt")


def detect_objects(image):

    results = model(image, verbose=False, conf=0.30)
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
            "center_y": center_y,
            "bbox":(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )
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
            if obj["name"] != reference_object:
                if obj["center_x"] < reference["center_x"]:
                    answer_objects.append(obj["name"])

    elif "right" in question:

        relation = "right"

        for obj in detected_objects:
            if obj["name"] != reference_object:
                if obj["center_x"] > reference["center_x"]:
                    answer_objects.append(obj["name"])

    elif "near" in question or "paas" in question:

        relation = "near"

        for obj in detected_objects:
            if obj["name"] != reference_object:

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