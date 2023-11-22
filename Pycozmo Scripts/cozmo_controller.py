
#This is a copy of older script that was designed for Cozmo SDK
#It is copied here as reference but serves no purpose

#It has since been adapted into PycozmoFSM_controller
import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image
angle = 0
distance = 100
speed = 50
expression = None
front = None
duration = 2000

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
    await move_forward(robot, distance_to_move, speed_to_move)

async def cozmo_show_img(robot: cozmo.robot.Robot):
    # change the expression based on what is front
    img = None
    if front == "wall":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/Alert_icon.png" 
    if front == "nothing":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/check_mark.png"
    if front == "goal":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/finish_flag.png"
    if front == "hit":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/injured.png"
    
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

