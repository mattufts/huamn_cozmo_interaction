#This script needs to incorporate the 

import sys
import os
import pycozmo
import time
from pycozmo import util   
from pycozmo.util import Angle, Distance, Speed, Pose, Angle, Vector3, Pose, Quaternion
from pycozmo import protocol_encoder
from pycozmo.protocol_encoder import TurnInPlace

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


# Initialize global variables (angle, distance, speed, front, duration, default_image)

# Define function act(robot):
#     angle_to_turn = angle
#     turn_angle(robot, angle_to_turn)
#     distance_to_move = distance
#     speed_to_move = speed
#     Print "Turning Angle:", angle_to_turn
#     move_forward(robot, distance_to_move, speed_to_move)
#     show_image(robot, default_image)

# Define function explore_state(robot):
#     Print "Exploring..."
#     angle_to_turn = angle
#     turn_angle(robot, angle_to_turn)
#     distance_to_move = distance
#     speed_to_move = speed
#     Print "Turning Angle:", angle_to_turn
#     move_forward(robot, distance_to_move, speed_to_move)
#     Return interact_state

# Define function interact_state(robot):
#     Print "Interacting..."
#     Wait for 3 seconds
#     Return explore_state

# Define function turn_angle(robot, angle):
#     Turn the robot in place by angle degrees
#     Wait for the turn to complete

# Define function move_forward(robot, distance, speed):
#     Drive the robot straight by distance millimeters at speed millimeters per second
#     Wait for the movement to complete

# Define function show_image(robot, image_path):
#     Load the image from image_path
#     Resize the image to fit the OLED display
#     Convert the image to screen data
#     Display the image on the robot's face for a duration

# Define function run_fsm(robot):
#     Set current_state to explore_state
#     Show default_image on the robot's face
#     Repeat forever:
#         Call current_state(robot) and set current_state to the returned value

# Define function main():
#     Connect to the Cozmo robot
#     Get the robot object from the connection
#     Call run_fsm(robot)

# If the script is executed directly:
#     Call main()