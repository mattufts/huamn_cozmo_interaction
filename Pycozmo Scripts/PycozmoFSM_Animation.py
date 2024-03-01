#FSM script to handle animation, movement and reactions
#This is the new Cozmo Controller script that will be used for the maze
#It defines the robot's actions and robots expressions
#It also defines the FSM states and the FSM execution function

#This script is imported by MainDemo_Animation script

#The scripts that this imports are:
    #Call_Animation

import sys
import os
import pycozmo
import Call_Animation as Call_Animation
from Call_Animation import display_images
import time
from pycozmo.util import Angle, Distance, Speed
from PIL import Image, ImageOps

# Define global variables
Angle = 0
Distance = 80
Speed = 50
front = None

# State-to-animation mapping (Updated to use animation folders)
state_to_animation = {
    "wall": "Hurt",
    "nothing": "Blinking",
    "goal": "Happy",
    "hit": "Hurt",
    "left": "Left",
    "right": "Right",
    "alert": "Surprse",
    "finish": "Successful"
}

# FSM state functions
def act(robot: pycozmo.client, state):
    global Angle, Distance, Speed
    angle_to_turn = Angle
    turn_angle(robot, angle_to_turn)
    
    display_animation(robot, state)
    
    distance_to_move = Distance
    speed_to_move = Speed
    move_forward(robot, distance_to_move, speed_to_move)

def explore_state(robot: pycozmo.client, state):
    print("Exploring....")
    act(robot, state)
    return "interact"

def interact_state(robot: pycozmo.client, state):
    print("Interacting....")
    act(robot, state)
    return "explore"

# Helper functions for Cozmo's movements
def turn_angle(robot: pycozmo.Client, angle: float):
    # based on the desired angle and Cozmo's turning characteristics
    speed = 30  # Example speed value
    duration = abs(angle) / speed  # Example calculation for duration
    if angle > 0:
        robot.drive_wheels(lwheel_speed=speed, rwheel_speed=-speed, duration=duration)
    elif angle < 0:
        robot.drive_wheels(lwheel_speed=-speed, rwheel_speed=speed, duration=duration)

def move_forward(robot: pycozmo.Client, distance: float, speed: float):
    if speed > 0:
        duration = distance / speed
        robot.drive_wheels(lwheel_speed=speed, rwheel_speed=speed, duration=duration)
        print ("Driving Straight")

def display_animation(cli, state):
    #base_path = "/path/to/your/animations"
    base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages" #for iMac Pro
    #base_path = "/" #For Raspberry pi images
    animation_folder = state_to_animation.get(state, "Blinking")
    animation_path = os.path.join(base_path, animation_folder)
    display_images(cli, animation_path)

# Define the FSM execution function
def run_fsm(robot: pycozmo.client):
    current_state = "explore"
    while True:
        if current_state == "explore":
            current_state = explore_state(robot, current_state)
        elif current_state == "interact":
            current_state = interact_state(robot, current_state)
        else:
            print("Unknown state:", current_state)
            break

# The main function to connect to Cozmo and start the FSM
def main():
    with pycozmo.connect() as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        cli.set_head_angle(head_angle)
        time.sleep(1)
        run_fsm(cli)

if __name__ == '__main__':
    main()