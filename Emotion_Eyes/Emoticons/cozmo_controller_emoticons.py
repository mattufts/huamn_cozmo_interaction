#Cozmo Robot Navigation Controller
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This code provides a basic framework for controlling cozmo to navigate through a maze or environment.  It
#utilizes the SDK, asyncio for asynchronous programming, and the PIL library for image manipulation.

#Key Features
#1.  Cozmo can move forward, turn left, and turn right
#2.  Moving cozmo forward by a specific distance (in mm) and speed (in mm/s)
#3.  Displaying images on cozmo's face based on the environment
#4. Displaying animations on cozmo's face based on the environment

import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image
angle = 0
distance = 80
speed = 50
expression = None 
front = None    #represents the global variable for identifying front of Cozmo
duration = 2000 #duration is how long the animation stays on cozmo's face

async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()

async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()
    
async def act(robot: cozmo.robot.Robot): 
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)
    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    print("Turning Angle: ", angle_to_turn)
    await move_forward(robot, distance_to_move, speed_to_move)

async def cozmo_show_img(robot: cozmo.robot.Robot):
    # change the expression based on what is front
    img = None
    if front == "wall":   
        img = "Emotion_Eyes/Emoticons/Angry_Stop-01.png" 
    if front == "nothing":
        img = "Emotion_Eyes/Emoticons/neutral.png"
    if front == "goal":
        img = "Emotion_Eyes/Emoticons/happy-01.png"
    if front == "hit":
        img = "Emotion_Eyes/Emoticons/injured.png"
    if front == "left":
        img: "Emotion_Eyes/Emoticons/glancing_left-01.png"
    if front == "right":
        img: "Emotion_Eyes/Emoticons/glancing_right-01.png"
    
    
    if img is not None:
        image = Image.open(img)
        resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
        robot.display_oled_face_image(face_image, duration)
async def cozmo_show_animation(robot: cozmo.robot.Robot):
    img = []
    if front == "wall":
        path = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Emotion_Eyes/Blinking/eyes_blink"
        for i in range(1, 7):
            img.append(path + str(i) + ".png")
    if front == "nothing":
        pass
    if len(img) > 0:
        for i in range(0, len(img)):
            image = Image.open(img[i])
            resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
            face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
            robot.display_oled_face_image(face_image, duration/2)
            await asyncio.sleep(0.2)

