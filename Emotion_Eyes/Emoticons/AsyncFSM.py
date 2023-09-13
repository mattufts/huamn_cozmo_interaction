#This script is designed to work as a cozmo controller with Asyncio
#Script is based off of and replaces cozmo_controller_emoticons while also incorporating async functions
#It does not run on its own, but is used in conjunction with maze.py
import cozmo
import asyncio
import time
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image
# Define global variables
angle = 0
distance = 80
speed = 50
front = None  # represents the global variable for identifying front of Cozmo
duration = 2000  # duration is how long the animation stays on Cozmo's face
default_image = "blank.png"
# FSM state functions
async def act(robot: cozmo.robot.Robot):
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)
    # Call the cozmo_show_img function to display the image
    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    print("Turning Angle: ", angle_to_turn)
    await move_forward(robot, distance_to_move, speed_to_move)
async def explore_state(robot: cozmo.robot.Robot):
    print("Exploring...")
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    turn_angle(robot, angle_to_turn)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    print("Turning Angle: ", angle_to_turn)
    await move_forward(robot, distance_to_move, speed_to_move)
    return "interact"
async def interact_state(robot: cozmo.robot.Robot):
    print("Interacting...")
    #await cozmo_show_img(robot)
    # Perform interaction behavior here
    await asyncio.sleep(3)
    return "explore"
# Helper functions
async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()
async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed), should_play_anim=False, in_parallel=True).wait_for_completed()
async def cozmo_show_img(robot: cozmo.robot.Robot):
    global default_image
    # Set the default image to neutral
    img = default_image
    image = Image.open(img)
    resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
    face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
    
    while True:
        robot.display_oled_face_image(face_image, 1000)
        await asyncio.sleep(0.1)
# Define the FSM execution function
async def run_fsm(robot: cozmo.robot.Robot):
    current_state = "explore"  # Initial state
    await cozmo_show_img(robot)
    while True:
        if current_state == "explore":
            current_state = await explore_state(robot)
        elif current_state == "interact":
            current_state = await interact_state(robot)
        else:
            print("Unknown state:", current_state)
            break
# Define the main function
async def main():
    # Create a Cozmo robot object
    robot = await cozmo.robot.Robot.wait_for(robot)
    # Call the run_fsm function
    await run_fsm(robot)
if __name__ == '__main__':
    #asyncio.run(main())
    cozmo.run_program(run_fsm)