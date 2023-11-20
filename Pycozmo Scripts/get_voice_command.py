#COPY OF get_voice_command.py found in main
#Delete this when bringing over script into main

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

# def extract_values(text):
#     angle_pattern = re.compile(r"(?P<angle>-?\d+(\.\d+)?)(?:\s?degrees? |°)")
#     distance_pattern = re.compile(r"(?P<distance>-?\d+(\.\d+)?)(?:\s?millimeters?| mm)")
#     speed_pattern = re.compile(r"(?P<speed>-?\d+(\.\d+)?)(?:\s? for a second)")

#     angle_match = angle_pattern.search(text)
#     distance_match = distance_pattern.search(text)
#     speed_match = speed_pattern.search(text)

#     angle = float(angle_match.group("angle")) if angle_match else 0
#     distance = float(distance_match.group("distance")) if distance_match else 0
#     speed = float(speed_match.group("speed")) if speed_match else 50

#     return angle, distance, speed

def extract_values(text):
    angle_pattern = re.compile(r"(?P<angle>left|right)")
    distance_pattern = re.compile(r"(?P<distance>forward|backward)")
    speed_pattern = re.compile(r"(?P<speed>faster|slower)")

    angle_match = angle_pattern.search(text)
    distance_match = distance_pattern.search(text)
    speed_match = speed_pattern.search(text)

    angle_text = angle_match.group("angle") if angle_match else "straight"
    distance_text = distance_match.group("distance") if distance_match else "no movement"
    speed_text = speed_match.group("speed") if speed_match else "medium"
    action = None
    # Convert angle to numeric value
    if angle_text == "left":
        angle = 90
        action  = 0
    elif angle_text == "right":
        angle = -90
        action  = 1
    else:
        angle = 0

    # Convert distance to numeric value
    if distance_text == "forward":
        distance = 50
        action  = 2
    elif distance_text == "backward":
        distance = -50
    else:
        distance = 0

    # Convert speed to numeric value
    if speed_text == "faster":
        speed = 2
    elif speed_text == "slower":
        speed = 0.5
    else:
        speed = 1

    return angle, distance, speed, action

def get_command():
    text = recognize_speech()
    if text:
        return extract_values(text)
    else:
        print("Could not extract values from speech. Plz retry.")
        get_command()


def get_command_from_keyboard():
    action = input("Enter your command: ")
    if action == "l" or "left":
        action = 0
    if action == "r" or "right":
        action = 1
    if action == "f" or "forward":
        action = 2
    action = float(action)
    angle = 0
    distance = 0
    speed = 0
    if action == 2:
        angle = 0
        distance = 50
        speed = 50
    elif action == 0:
        angle = 90
        distance = 0
        speed = 0
    elif action == 1:
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
