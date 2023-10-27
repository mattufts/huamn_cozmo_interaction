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


# FSM state functions
def act(robot: pycozmo.client, image_path):
    
    angle_to_turn = Angle
    turn_angle(robot, angle_to_turn, image_path)
    
    show_image(robot, image_path)
    
    distance_to_move = Distance
    speed_to_move = Speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    
    
def explore_state(robot: pycozmo.client, image_path):
    print("Exploring...")
    angle_to_turn = Angle
    turn_angle(angle_to_turn)
    show_image(robot, image_path)
    distance_to_move = Distance
    speed_to_move = Speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    return "interact"

def interact_state(robot: pycozmo.client, image_path):
    print("Interacting...")
    show_image(robot, image_path)
    time.sleep(3)
    return "explore"

# Helper functions
def turn_angle(Angle: float):
    protocol_encoder.TurnInPlace(Angle)

def move_forward(robot: pycozmo.Client, Distance: float, Speed: float):
    robot.drive_wheels(lwheel_speed=50.0, rwheel_speed=50.0, duration=5.0)
    print ("Driving Straight")
    
def show_image(cli, image_path):
    # Set the default image to neutral
    target_size = (128, 32)
    default_image = "blank.png"
    # Change the expression based on what is in front
    img = None
    if front == "wall":
        img = "Angry_Stop-01.png"
        #img = "pycozmo.png"
    elif front == "nothing":
        img = "neutral.png"
        #img = "pycozmo.png"
    elif front == "goal":
        #img = "happy-01.png"
        img = "pycozmo.png"
    elif front == "hit":
        img = "sudden_hit-01.png"
        #img = "pycozmo.png"
    elif front == "left":
        img = "glancing_left-01.png"
        #img = "pycozmo.png"
    elif front == "right":
        img = "glancing_right-01.png"
        #img = "pycozmo.png"
    
    # Use the default image if no other image is determined
    if img is None:
        img = default_image
    
    #image = Image.open(os.path.join(os.path.dirname(__file__), img)) # Open the image file
    image_open = Image.open(image_path)
    image_resized = image_open.resize(target_size)
    img = image_resized.convert('1') 

    start_time = time.time()
    cli.anim_controller.enable_animations(True)
    while True:
        if time.time() - start_time > 10.0:
            break
        cli.display_image(img)
        



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
        
        image_path = os.path.join(os.path.dirname(__file__), "emoticons", "neutral.png")
        run_fsm(cli, image_path)
        
        cli.wait_for_robot()
        cli.disconnect()
        cli.stop()

if __name__ == '__main__':
    main()
    
#resolving cozmo's face
#instead of making a square maze, can we make a curved like maze so that the robot has branching?
#Can the robot approximately follow a curved image
#Can we have an option that allows us to only look at the robot?

#Next step is to design the maze
#IRB Training and Consent Form
#Design the maze
#dynamic multi choice environment 
    #make sure that pycozmo maze can still work with separate agents and functionalize everything
    
#Robot can have two choices 
#Real world investigation for the maze and