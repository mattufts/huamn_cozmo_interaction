#Main Execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen

#The five scripts that this imports are:
    #maze_env.py
    #get_voice_command.py
    #PycozmoFSM.py
    #Call_Animation

import maze_env
import threading
#import get_voice_command
import PycozmoFSM_Animation as cozmo_controller
from PycozmoFSM_Animation import display_images   #newly added 
import pycozmo
import time

#initialize threading event
animation_event = threading.Event()

def set_ads(angle, distance, speed):  
    cozmo_controller.Angle = angle
    cozmo_controller.Distance = distance
    cozmo_controller.Speed = speed

env = maze_env.MazeEnv()
state = env.reset()
done = False



def continuous_blinking(cli):
    blinking_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
    while True:  # Loop to continuously display blinking animation
        if animation_event.is_set():
            #wait until the event is cleared to resume blinking
            animation_event.wait()
        display_images(cli, blinking_path)


def handle_interaction (cli, interaction_type):   
    #set the event to pause blinking
    animation_event.set()
    animation_paths = {
    "happy": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Happy",
    "sad": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Hurt",
    "angry": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Angry",
    "surprised": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Surprised",
    "neutral": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking",
    "left": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Left",
    "right": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Right",
    "finished": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Successful",
    }
    base_path = animation_paths.get(interaction_type)
    if base_path:
        display_images(cli, base_path, repeat_duration = 4)
   #clear the event to resume blinking
        animation_event.clear()

#Defining the Keyboard Actions for Cozmo
def get_keyboard_command():
    command = input("Enter command (F = forward, L = left, R = right, Q = quit): ")
    if command == 'F':
        return 'forward'
    elif command == 'L':
        return 'left'
    elif command == 'R':
        return 'right'
    elif command == 'Q':
        return 'quit'
    else:
        return 'invalid'

#Keyboard Controls For Cozmo   
def run_with_cozmo(cli):
    #run the blinking animation
    blinking_thread = threading.Thread(target=continuous_blinking, args=(cli,))
    blinking_thread.start()
    env = maze_env.MazeEnv()
    state = env.reset()
    done = False
    blinking_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
    print('Program is running')
    
    while not done:
        command = get_keyboard_command()
        if command == 'quit':
            break
        elif command == 'invalid':
            print("Invalid command. Try again.")
            continue
         # Set the angle, distance, and speed based on the command
        if command == 'left':
            set_ads(90, 0, 0)  # Example: turn 90 degrees left
            cozmo_controller.turn_angle(cli, 90)
            front = 'left'
        elif command == 'right':
            set_ads(-90, 0, 0)# Example: turn 90 degrees right
            cozmo_controller.turn_angle(cli, -90)
            front = 'right'
        elif command == 'forward':
            set_ads(0, 80, 50)
            cozmo_controller.move_forward(cli, 80, 50)# Example: move forward 80 units at speed 50
            front = 'forward'
        else: 
            #default to blinking
            display_images(cli, blinking_path)
            continue
        handle_interaction(cli, front) 

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle)
        cli.wait_for_robot()
        run_with_cozmo(cli)

if __name__ == '__main__':
    main()

#VoiceCommandScript
#Removed temporarily 1/27/2024