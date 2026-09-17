from object1.main import detect_objects, answer_question
from text_reading_module.text_reader import read_text
from voice_assistant.voice import speak, extract_object_names

image_path = "person4/object1/test_images/WhatsApp Image 2026-09-14 at 12.12.05 PM copy.jpeg"

detected_objects = detect_objects(image_path)

full_text = read_text(image_path)
print("OCR TEXT:", repr(full_text))

print("Detected Objects:")
for obj in detected_objects:
    print(obj)

# Object names for voice
object_names = extract_object_names(detected_objects)

if object_names:
    objects_sentence = "I can see " + ", ".join(object_names) + "."
else:
    objects_sentence = "I cannot detect any objects."

question = input("Ask your question: ")

result = answer_question(detected_objects, question)

print("\nAnswer:")
print(result["answer"])

# Speak everything together in ONE TTS call
speech = (
    "Vision Assist AI is working. "
    f"The text says: {full_text}. "
    f"{objects_sentence} "
    f"{result['answer']}"
)

speak(speech)