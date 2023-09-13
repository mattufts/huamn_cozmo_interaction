#This script needs to incorporate the pycozmo library
#and is a rework of the AsyncFSM.py script 
 
import sys
import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

angle = 0
distance = 80
speed = 50
expression = None
front = None  # represents the global variable for identifying front of Cozmo
duration = 2000  # duration is how long the animation stays on cozmo's face

async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()

async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed), should_play_anim=False, in_parallel=True).wait_for_completed()

async def act(robot: cozmo.robot.Robot):
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)
    # Call the cozmo_show_img function to display the image
    await cozmo_show_img(robot)
    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    print("Turning Angle: ", angle_to_turn)
    await move_forward(robot, distance_to_move, speed_to_move)

# This function displays an image on Cozmo's face based on the environment
async def cozmo_show_img(robot: cozmo.robot.Robot):
    # Set the default image to neutral
    default_image = "neutral.png"

    # Change the expression based on what is in front
    img = None
    if front == "wall":
        img = "angry.png"  # Set the appropriate image for this state
    elif front == "nothing":
        img = "neutral.png"
    elif front == "goal":
        img = "happy.png"  # Set the appropriate image for this state
    elif front == "hit":
        img = "angry.png"  # Set the appropriate image for this state
    elif front == "left":
        img = "neutral.png"
    elif front == "right":
        img = "neutral.png"

    # Use the default image if no other image is determined
    if img is None:
        img = default_image

    image = Image.open(img)
    resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
    face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
    robot.display_oled_face_image(face_image, duration)

     # Set the idle animation during image display
    robot.set_idle_animation(Triggers.Neutral)

async def main():
    # Create a Cozmo robot object
    robot = await cozmo.robot.Robot.wait_for_robot()

    # Call the act function
    await act(robot)

if __name__ == '__main__':
    # Run the main function within a new event loop
    asyncio.run(main())

import sys
import os
import pycozmo
import time
from pycozmo import util   
from pycozmo.util import Angle, Distance, Speed, Pose, Angle, Vector3, Pose, Quaternion
from pycozmo import protocol_encoder

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

# Define global variables
Angle = 0
Distance = 80
Speed = 50

front = None
duration = 2000
default_image = "blank.png"
cli = pycozmo.Client()

# FSM state functions
def act(robot: pycozmo.client):
    angle_to_turn = Angle
    turn_angle(robot, angle_to_turn)
    distance_to_move = Distance
    speed_to_move = Speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    show_image(robot, default_image)
    
def explore_state(robot: pycozmo.client):
    print("Exploring...")
    angle_to_turn = Angle
    turn_angle(angle_to_turn)
    distance_to_move = Distance
    speed_to_move = Speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    return interact_state

def interact_state(robot: pycozmo.client):
    #print("Interacting...")
    #time.sleep(3)
    return explore_state

# Helper functions
def turn_angle(Angle: float):
    protocol_encoder.TurnInPlace(Angle)

def move_forward(robot: pycozmo.client, Distance: float, Speed: float):
    cli.drive_wheels (lwheel_speed=50.0, rwheel_speed=50.0, duration=2.0)
    print ("Driving Straight")
    #robot.drive_straight(distance_mm=Distance, speed_mmps=Speed, should_play_anim=False).wait_for_completed()

def show_image(robot: pycozmo.client, image_path: str):
    #image = Image.open()
    target_size = (128, 32)
    image = Image.open(os.path.join(os.path.dirname(__file__), "assets", image_path))
    resized_image = image.resize(target_size, Image.ANTIALIAS)
    image =  resized_image.convert('1')
    cli.display_image(image)

# Define the FSM execution function
def run_fsm(robot: pycozmo.client):
    current_state = explore_state
    show_image(robot, default_image)
    while True:
        current_state = current_state(robot)

# Define the main function
# The main function should connect to cozmo immediately and start the FSM
def main():
    with pycozmo.connect() as cli:
        # # Connect to the Cozmo robot
        #cli.start()
        cli.connect()
        run_fsm(pycozmo.robot) 
        cli.wait_for_robot()
    #cli.disconnect()
    #cli.stop()

if __name__ == '__main__':
    main()