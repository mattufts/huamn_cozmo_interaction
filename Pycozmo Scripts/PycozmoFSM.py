#This script needs to incorporate the pycozmo library
#and is a rework of the AsyncFSM.py script 
 
import sys
import os
import pycozmo
import time 

from pycozmo.util import Angle, Distance, Speed, Pose, Angle
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
    image = Image.open(os.path.join(image_path))
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
    with pycozmo.connect() as pyc:
        cli.start()
        cli.connect()
        # # Connect to the Cozmo robot
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
           #turn off "alive" animations for cozmo
        cli.anim_controller.enable_animations(False)
        #cli.anim_controller.cancel_anim()
        pyc.set_head_angle(head_angle)
        run_fsm(pycozmo.robot) 
        pyc.wait_for_robot()
    pyc.disconnect()
    pyc.stop()

if __name__ == '__main__':
    main()