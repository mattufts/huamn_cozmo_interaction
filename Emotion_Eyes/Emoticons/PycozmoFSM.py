Initialize global variables (angle, distance, speed, front, duration, default_image)

Define function act(robot):
    angle_to_turn = angle
    turn_angle(robot, angle_to_turn)
    distance_to_move = distance
    speed_to_move = speed
    Print "Turning Angle:", angle_to_turn
    move_forward(robot, distance_to_move, speed_to_move)
    show_image(robot, default_image)

Define function explore_state(robot):
    Print "Exploring..."
    angle_to_turn = angle
    turn_angle(robot, angle_to_turn)
    distance_to_move = distance
    speed_to_move = speed
    Print "Turning Angle:", angle_to_turn
    move_forward(robot, distance_to_move, speed_to_move)
    Return interact_state

Define function interact_state(robot):
    Print "Interacting..."
    Wait for 3 seconds
    Return explore_state

Define function turn_angle(robot, angle):
    Turn the robot in place by angle degrees
    Wait for the turn to complete

Define function move_forward(robot, distance, speed):
    Drive the robot straight by distance millimeters at speed millimeters per second
    Wait for the movement to complete

Define function show_image(robot, image_path):
    Load the image from image_path
    Resize the image to fit the OLED display
    Convert the image to screen data
    Display the image on the robot's face for a duration

Define function run_fsm(robot):
    Set current_state to explore_state
    Show default_image on the robot's face
    Repeat forever:
        Call current_state(robot) and set current_state to the returned value

Define function main():
    Connect to the Cozmo robot
    Get the robot object from the connection
    Call run_fsm(robot)

If the script is executed directly:
    Call main()


import pycozmo
import time
from PIL import Image

# Define global variables
angle = 0
distance = 80
speed = 50
front = None
duration = 2000
default_image = "blank.png"

# FSM state functions
def act(robot: pycozmo.robot.Robot):
    angle_to_turn = angle
    turn_angle(robot, angle_to_turn)
    distance_to_move = distance
    speed_to_move = speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    show_image(robot, default_image)
    
def explore_state(robot: pycozmo.robot.Robot):
    print("Exploring...")
    angle_to_turn = angle
    turn_angle(robot, angle_to_turn)
    distance_to_move = distance
    speed_to_move = speed
    print("Turning Angle: ", angle_to_turn)
    move_forward(robot, distance_to_move, speed_to_move)
    return interact_state

def interact_state(robot: pycozmo.robot.Robot):
    print("Interacting...")
    time.sleep(3)
    return explore_state

# Helper functions
def turn_angle(robot: pycozmo.robot.Robot, angle: float):
    robot.turn_in_place(degrees=angle).wait_for_completed()

def move_forward(robot: pycozmo.robot.Robot, distance: float, speed: float):
    robot.drive_straight(distance_mm=distance, speed_mmps=speed, should_play_anim=False).wait_for_completed()

def show_image(robot: pycozmo.robot.Robot, image_path: str):
    image = Image.open(image_path)
    resized_image = image.resize(pycozmo.oled_face.dimensions(), Image.BICUBIC)
    face_image = pycozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
    robot.display_oled_face_image(face_image, duration)

# Define the FSM execution function
def run_fsm(robot: pycozmo.robot.Robot):
    current_state = explore_state
    show_image(robot, default_image)
    while True:
        current_state = current_state(robot)

# Define the main function
def main():
    with pycozmo.connect() as cli:
        robot = cli.robot
        run_fsm(robot)

if __name__ == '__main__':
    main()
