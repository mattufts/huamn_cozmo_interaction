#FSM script to handle animation, movement and reactions

import sys
import os
import pycozmo
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
    "wall": "AnimImages/Hurt",
    "nothing": "AnimImages/Blinking",
    "goal": "AnimImages/Happy",
    "hit": "AnimImages/Hurt",
    "left": "AnimImages/Left",
    "right": "AnimImages/Right"
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

def display_images(cli, base_path, fps=30, repeat_duration=3):
    frame_duration = 1.0 / fps  # Duration of each frame in seconds

    # List and count PNG files in the directory
    image_files = [f for f in os.listdir(base_path) if f.endswith('.png')]
    num_images = len(image_files)
    
    #calculate total loops needed based on repeat_duration
    total_frames = repeat_duration * fps
    total_loops = int(total_frames / len(image_files))
    
    # Display each image in sequence
    for _ in range (total_loops):
        for file_name in sorted(image_files):
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)

    # Repeat the last two images for an extra duration
    extra_time = 4.0
    repeat_frames = int(extra_time / frame_duration)
    last_two_images = sorted(image_files)[-2:]  # Get last two images
    for _ in range(repeat_frames):
        for file_name in last_two_images:
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)
            
def display_resized_image(cli, image_path, duration):
    target_size = (128, 32)

    if os.path.exists(image_path):
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        cli.display_image(img)
        time.sleep(duration)
    else:
        print(f"Image file not found: {image_path}")

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