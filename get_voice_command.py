import re
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source,  timeout=10, phrase_time_limit=5)
        print("record over")
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Sorry, could not recognize your speech.")
        return None

def extract_values(text):
    angle_pattern = re.compile(r"(?P<angle>-?\d+(\.\d+)?)(?:\s?degrees? |°)")
    distance_pattern = re.compile(r"(?P<distance>-?\d+(\.\d+)?)(?:\s?millimeters?| mm)")
    speed_pattern = re.compile(r"(?P<speed>-?\d+(\.\d+)?)(?:\s? for a second)")

    angle_match = angle_pattern.search(text)
    distance_match = distance_pattern.search(text)
    speed_match = speed_pattern.search(text)

    angle = float(angle_match.group("angle")) if angle_match else 0
    distance = float(distance_match.group("distance")) if distance_match else 0
    speed = float(speed_match.group("speed")) if speed_match else 50

    return angle, distance, speed
def get_command():
    text = recognize_speech()
    if text:
        angle, distance, speed = extract_values(text)
        print(f"Angle: {angle} degrees")
        print(f"Distance: {distance} millimeters")
        print(f"Speed: {speed} millimeters per second")
        return angle, distance, speed
    else:
        print("Could not extract values from speech.")
        return 0, 0, 0
def get_command_from_keyboard():
    action = input("Enter your command: ")
    if action == 1:
        angle = 0
        distance = 50
        speed = 50
    elif action == 2:
        angle = 90
        distance = 0
        speed = 0
    elif action == 3:
        angle = -90
        distance = 0
        speed = 0
    return angle, distance, speed, action
# if __name__ == "__main__":
#     text = recognize_speech()
#     if text:
#         angle, distance, speed = extract_values(text)
#         print(f"Angle: {angle} degrees")
#         print(f"Distance: {distance} millimeters")
#         print(f"Speed: {speed} millimeters per second")
#     else:
#         print("Could not extract values from speech.")
