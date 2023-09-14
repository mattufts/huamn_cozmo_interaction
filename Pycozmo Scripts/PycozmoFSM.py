#This script needs to incorporate the pycozmo library
#and is a rework of the AsyncFSM.py script 



import os
import time 

from PIL import Image

import pycozmo


with pycozmo.connect() as cli:

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)
    time.sleep(1)

    # Load image
    #target_size = (128, 32)
    image = Image.open(os.path.join(os.path.dirname(__file__), "pycozmo.png"))
    #resized_image = image.resize(target_size, Image.ANTIALIAS)
    image =  image.convert('1') 
    
    cli.display_image(image)
 
# import sys
# import os
# import pycozmo
# import time 

# from pycozmo.util import Angle, Distance, Speed, Pose, Angle
# from pycozmo import protocol_encoder

# try:
#     from PIL import Image
# except ImportError:
#     sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

# # Define global variables
# Angle = 0
# Distance = 80
# Speed = 50
# front = None
# duration = 2000
# default_image = "blank.png"

# cli = pycozmo.Client()

# # FSM state functions
# def act(robot: pycozmo.client):
#     angle_to_turn = Angle
#     turn_angle(robot, angle_to_turn)
#     distance_to_move = Distance
#     speed_to_move = Speed
#     print("Turning Angle: ", angle_to_turn)
#     move_forward(robot, distance_to_move, speed_to_move)
#     show_image(robot, default_image)
    
# def explore_state(robot: pycozmo.client):
#     print("Exploring...")
#     angle_to_turn = Angle
#     turn_angle(angle_to_turn)
#     distance_to_move = Distance
#     speed_to_move = Speed
#     print("Turning Angle: ", angle_to_turn)
#     move_forward(robot, distance_to_move, speed_to_move)
#     return "interact"

# def interact_state(robot: pycozmo.client):
#     print("Interacting...")
#     cli.display_image(image)
#     time.sleep(3)
#     return "explore"

# # Helper functions
# def turn_angle(Angle: float):
#     protocol_encoder.TurnInPlace(Angle)

# def move_forward(robot: pycozmo.client, Distance: float, Speed: float):
#     cli.drive_wheels (lwheel_speed=50.0, rwheel_speed=50.0, duration=2.0)
#     print ("Driving Straight")
    
# def show_image(robot: pycozmo.client, image_path: str):
#     # Set the default image to neutral
#     default_image = "blank.png"
#     # Change the expression based on what is in front
#     img = None
#     if front == "wall":
#         #img = "Angry_Stop-01.png"
#         img = 'blank.png'
#     elif front == "nothing":
#         #img = "neutral.png"
#         img = 'blank.png'
#     elif front == "goal":
#         #img = "happy-01.png"
#         img = 'blank.png'
#     elif front == "hit":
#         #img = "sudden_hit-01.png"
#         img = 'blank.png'
#     elif front == "left":
#         #img = "glancing_left-01.png"
#         img = 'blank.png'
#     elif front == "right":
#         #img = "glancing_right-01.png"
#         img = 'blank.png'
   
#     if img is None:
#         img = default_image
#     target_size = (128, 32)
#     image = Image.open(os.path.join(image_path))
#     resized_image = image.resize(target_size, Image.ANTIALIAS)
#     image =  resized_image.convert('1') 
    
#     cli.display_image(image)


# # Define the FSM execution function
# def run_fsm(robot: pycozmo.client):
#     current_state = "explore"
#     #show_image(robot, default_image)
#     while True:
#         if current_state == "explore":
#             current_state == explore_state(robot)
#         elif current_state == "interact": 
#             current_state = interact_state(robot)
#         else:
#             print("Unknown state:", current_state)
#             break

# # Define the main function
# # The main function should connect to cozmo immediately and start the FSM
# def main():
#     with pycozmo.connect() as pyc:
#         cli.start()
#         cli.connect()
#         # # Connect to the Cozmo robot
#         head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
#            #turn off "alive" animations for cozmo
#         #cli.anim_controller.enable_animations(False)
#         #cli.anim_controller.cancel_anim()
#         pyc.set_head_angle(head_angle)
#         run_fsm(pycozmo.robot) 
#         pyc.wait_for_robot()
#     pyc.disconnect()
#     pyc.stop()

# if __name__ == '__main__':
#     main()