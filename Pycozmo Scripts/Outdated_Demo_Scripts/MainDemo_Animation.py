#main execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen

#The scripts that MainDemo imports are:
    #maze_env.py
    #PycozmoFSM_Animation.py
    #path_planner for navigation
#script that was worked on 3/5/2024

import maze_env
import threading
#import get_voice_command
import PycozmoFSM_Animation as cozmo_controller
from PycozmoFSM_Animation import display_animation, display_images
from Call_Animation import execute_interaction_animation
#import path_planner as path_planner
#from path_planner import find_shortest_path, determine_next_action, mark_forward
import pycozmo
import os
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
display_flag = True

def continuous_blinking(cli):
    global display_flag
    blinking_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
    while True:
        if animation_event.is_set():
            animation_event.wait()
        if display_flag:
            #display_animation(cli, blinking_path)
            display_images(cli, blinking_path, repeat_duration=0.3, extra_time=1)
            #should be the duration of the animation + extra time
            #<--- play with this time and adjust
            time.sleep(2.5)
        print (display_flag)

def handle_interaction (cli, interaction_type):
    #signal the start of an interaction animation_event
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
    #Request the Call_animaiton script to execute the animation for the interaction
    execute_interaction_animation(cli, interaction_type)
        #if the above doesn't work try to use this script:
        #base_path = animation_paths.get(interaction_type)
        #if base_path:
            #display_images(cli, base_path=
    #clear the event after the animation request to resume default behavior    
    animation_event.clear()
    base_path = animation_paths.get(interaction_type)
    
        
#Defining the Keyboard Actions for Cozmo
def get_keyboard_command():
    command = input("Enter command (F = forward, L = left, R = right, S = stop, Q = quit): ")
    if command == 'F':
        return 'forward'
    elif command == 'L':
        return 'left'
    elif command == 'R':
        return 'right'
    elif command == 'S':
        return 'stop'
    elif command == 'Q':
        return 'quit'
    else:
        return 'invalid'
    
def convert_command_to_action(command):
    if command ==   'forward':
        return 2  #  2 is the action for moving forward in MazeEnv
    elif command == 'left':
        return 0  # 0 is the action for turning left
    elif command == 'right':
        return 1  #  1 is the action for turning right
    elif command == 'stop': 
        return 3
    return None

# Run Cozmo with updated behaviors
def run_with_cozmo(cli):
    global env, state, done
    env = maze_env.MazeEnv()
    state = env.reset()
    done = False
    print('Program is running')

    while not done:
        command = get_keyboard_command()
        # Convert command to action for the maze environment
        action = convert_command_to_action(command)
         # Check if action is valid before proceeding
        if action is not None:
            state, hit_wall, front, done, _ = env.step(action)
        if command == 'quit':
            break
        elif command == 'invalid':
            print("Invalid command. Try again.")
            continue
        
        state, hit_wall, front, done, _ = env.step(action)
 
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
        elif command == 'stop':
            set_ads(0, 0, 0)
            cozmo_controller.move_forward(cli,00, 00)
            front = 'stop'
        else: 
            #default to blinking
            continuous_blinking(cli)
            continue

        if hit_wall:
            # Cozmo hits a wall, play "Hurt" animation
            set_ads(0, 10, 10) #angle distance and speed
            cozmo_controller.act(cli)
            handle_interaction(cli, "sad")
            set_ads(0, -10, 10)
            cozmo_controller.act(cli)
            cozmo_controller.front = "hit"

        elif done:
            # Cozmo reaches the end of the maze, play "Happy" animation
            handle_interaction(cli, "happy")
        elif action == 2 and can_move_left_or_right():
            # Cozmo is moving forward and there is a path to the left or right
            if is_path_left():
                handle_interaction(cli, "left")
            if is_path_right():
                handle_interaction(cli, "right")

        else:
            handle_interaction(cli, front)
            
def can_move_left_or_right():
    # Get Cozmo's left and right directions based on current direction
    left_dir, right_dir = get_left_right_dirs(env.current_dir)

    # Check if left or right cell is open
    return is_cell_open(env.current_pos + left_dir) or is_cell_open(env.current_pos + right_dir)

def is_path_left():
    # Get Cozmo's left direction based on current direction
    left_dir = get_left_right_dirs(env.current_dir)[0]
    
    # Check if left cell is open
    return is_cell_open(env.current_pos + left_dir)

def is_path_right():
    # Get Cozmo's right direction based on current direction
    right_dir = get_left_right_dirs(env.current_dir)[1]
    
    # Check if right cell is open
    return is_cell_open(env.current_pos + right_dir)

def get_left_right_dirs(current_dir):
    # Define direction vectors
    dir_map = {(0, 1): ((-1, 0), (1, 0)),  # Facing up
               (1, 0): ((0, 1), (0, -1)),  # Facing right
               (0, -1): ((1, 0), (-1, 0)), # Facing down
               (-1, 0): ((0, -1), (0, 1))} # Facing left
    return dir_map[tuple(current_dir)]

def is_cell_open(pos):
    # Check if the cell at pos is within bounds and open
    x, y = pos
    return 0 <= x < env.width and 0 <= y < env.height and env.maze[x][y] == 0

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        cli.set_head_angle(head_angle)
        cli.wait_for_robot()
        # Start the blinking thread
        blinking_thread = threading.Thread(target=continuous_blinking, args=(cli,), daemon=True)
        blinking_thread.start()
        
        front = 'stop'
    
        run_with_cozmo(cli)

if __name__ == '__main__':
    main()
#VoiceCommandScript
#Removed temporarily 1/27/2024

#below is the original MainDemo script
# import maze_env
# #import get_voice_command
# import PycozmoFSM_controller as cozmo_controller
# import pycozmo
# import os

# def set_ads(angle, distance, speed):  
#     cozmo_controller.Angle = angle
#     cozmo_controller.Distance = distance
#     cozmo_controller.Speed = speed

# env = maze_env.MazeEnv()
# state = env.reset()
# done = False

# #Defining the Keyboard Actions for Cozmo
# def get_keyboard_command():
#     command = input("Enter command (F = forward, L = left, R = right, Q = quit): ")
#     if command == 'F':
#         return 'forward'
#     elif command == 'L':
#         return 'left'
#     elif command == 'R':
#         return 'right'
#     elif command == 'Q':
#         return 'quit'
#     else:
#         return 'invalid'

# def show_neutral_image(cli):
#     #neutral_image_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/emoticons/neutral.png"
#     #for raspberry
#     neutral_image_path = "/home/matt_e/Documents/Github_Projects/HumanCozmoInteraction/huamn_cozmo_interaction/Pycozmo Scripts/emoticons/neutral.png"
#     cozmo_controller.show_image(cli, neutral_image_path)

# #Keyboard Controls For Cozmo   
# def run_with_cozmo(cli):
#     env = maze_env.MazeEnv()
#     state = env.reset()
#     done = False
#     print('Program is running')
#     while not done:
#         command = get_keyboard_command()
#         if command == 'quit':
#             break
#         elif command == 'invalid':
#             print("Invalid command. Try again.")
#             continue
#          # Set the angle, distance, and speed based on the command
#         if command == 'left':
#             set_ads(90, 0, 0)  # Example: turn 90 degrees left
#             cozmo_controller.turn_angle(cli, 90)
#             front = 'left'
#         elif command == 'right':
#             set_ads(-90, 0, 0)# Example: turn 90 degrees right
#             cozmo_controller.turn_angle(cli, -90)
#             front = 'right'
#         elif command == 'forward':
#             set_ads(0, 80, 50)
#             cozmo_controller.move_forward(cli, 80, 50)# Example: move forward 80 units at speed 50
#             front = 'forward'
#         if command in {'left', 'right', 'forward'}:
#             cozmo_controller.update_state_and_image(cli, command)
#         else: 
#             #default to blinking
#             show_neutral_image(cli)
#             continue
#         cozmo_controller.update_state_and_image(cli, front) 

# def main():
#     with pycozmo.connect(enable_procedural_face=False) as cli:
#         head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
#         cli.set_head_angle(head_angle) 
#         cli.wait_for_robot()
#         run_with_cozmo(cli)

# if __name__ == '__main__':
#     main

