#This is the new Cozmo Controller script that will be used for the maze
#It defines the robot's actions and robots expressions
#It also defines the FSM states and the FSM execution function
#This script is imported by the main script
#This script is based on the pycozmo_controller.py script

#For use with STATIC IMAGES
 
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

#Define image library that maps states to image file names
state_to_image = {  
    "wall": "sudden_hit-01.png",
    "nothing": "neutral.png",
    "goal": "happy-01.png",
    "hit": "sudden_hit-01.png",
    "left": "glancing_left-01.png",
    "right": "glancing_right-01.png"
}



# FSM state functions
def act(robot: pycozmo.client, image_path):
    global Angle, Distance, Speed
    angle_to_turn = Angle
    turn_angle(robot, angle_to_turn)
    
    show_image(robot, image_path)
    
    distance_to_move = Distance
    speed_to_move = Speed

    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    

def explore_state(robot: pycozmo.client, image_path):
    print("Exploring....")
    act(robot, image_path)
    return "interact"

def interact_state(robot: pycozmo.client, image_path):
    print ("Interacting....")
    act(robot, image_path)
    return "explore"

# Helper functions
def turn_angle(robot: pycozmo.Client, angle: float):
    # You'll need to determine the appropriate wheel speeds and duration
    # based on the desired angle and Cozmo's turning characteristics
    speed = 30  # Example speed value
    duration = abs(angle) / speed  # Example calculation for duration
    if angle > 0:
        robot.drive_wheels(lwheel_speed=speed, rwheel_speed=-speed, duration=duration)
    elif angle < 0:
        robot.drive_wheels(lwheel_speed=-speed, rwheel_speed=speed, duration=duration)

def move_forward(robot: pycozmo.Client, distance: float, speed: float):
    duration = distance / speed
    robot.drive_wheels(lwheel_speed=speed, rwheel_speed=speed, duration=duration)
    print ("Driving Straight")

def show_image(cli, image_path):
    # Set the target size for the image
    target_size = (128, 32)

    # Check if the specified image path exists
    if not os.path.exists(image_path):
        print("Image file not found: {image_path}")
        return

    # Open, resize, and convert the image
    image_open = Image.open(image_path)
    image_resized = image_open.resize(target_size)
    img = image_resized.convert('1')

    # Display the image on Cozmo's screen
    start_time = time.time()
    cli.anim_controller.enable_animations(True)
    while True:
        if time.time() - start_time > 10.0:
            break
        cli.display_image(img)

# def display_image



# Define the FSM execution function
def run_fsm(robot: pycozmo.client, image_path):
    current_state = "explore"
    #show_image(robot, default_image)
    while True:
        if current_state == "explore":
            current_state = explore_state(robot, image_path)
        elif current_state == "interact": 
            current_state = interact_state(robot, image_path)
        else:
            print("Unknown state:", current_state)
            break

# The main function should connect to cozmo immediately and start the FSM
def main():
    with pycozmo.connect() as cli:
        # # Connect to the Cozmo robot
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle)
        #turn off "alive" animations for cozmo
        time.sleep(1)
        run_fsm(cli, image_path)

if __name__ == '__main__':
    main()

#resolving cozmo's face
#instead of making a square maze, can we make a curved like maze so that the robot has branching?
#Can the robot approximately follow a curved image
#Can we have an option that allows us to only look at the robot?

#Robot can have two choices 
#Real world investigation for the maze anid