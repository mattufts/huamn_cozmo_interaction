#Main Execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen

#The scripts that MainDemo imports are:
    #maze_env.py
    #PycozmoFSM_Animation.py
    #path_planner for navigation

import maze_env
import threading
#import get_voice_command
import PycozmoFSM_Animation as cozmo_controller
from PycozmoFSM_Animation import display_animation 
from Call_Animation import execute_interaction_animation
import pycozmo
import os

#initialize threading event
animation_event = threading.Event()

def set_ads(angle, distance, speed):  
    cozmo_controller.Angle = angle
    cozmo_controller.Distance = distance
    cozmo_controller.Speed = speed

env = maze_env.MazeEnv()
state = env.reset()
state = "STOP"
front = None
done = False

def continuous_blinking(cli):
    blinking_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
    while True:
        if animation_event.is_set():
            animation_event.wait()
        display_animation(cli, blinking_path)

def handle_interaction (cli, interaction_type):
    #signal the start of an interaction animation_event
    animation_event.set()
    #Request the Call_animaiton script to execute the animation for the interaction
    execute_interaction_animation(cli, interaction_type)
    #clear the event after the animation request to resume default behavior    
    animation_event.clear()
        
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
    if command ==   'F':
        return 2  #  2 is the action for moving forward in MazeEnv
    elif command == 'L':
        return 0  # 0 is the action for turning left
    elif command == 'R':
        return 1  #  1 is the action for turning right
    elif command == 'S': 
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
        action = None
        hit_wall = False
         # Check if action is valid before proceeding
        if command is not None:
            action = convert_command_to_action(command)
            if action is not None:
                state, hit_wall, front, done, _ = env.step(action)
            if command == 'quit':
                break
            elif command == 'invalid':
                print("Invalid command. Try again.")
                continue
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
        #if command in {'left', 'right', 'forward'}:
            #cozmo_controller.update_state_and_image(cli, command)
        else: 
            #default to blinking
            continuous_blinking(cli)
            continue
        #cozmo_controller.update_state_and_image(cli, front) 

        if hit_wall:
            # Cozmo hits a wall, play "Hurt" animation
            set_ads(0, 10, 10) #angle distance and speed
            cozmo_controller.act(cli)
            handle_interaction(cli, "wall")
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
        global state, front, done
    
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        cli.set_head_angle(head_angle)
        cli.wait_for_robot()

        # Start the blinking thread
        blinking_thread = threading.Thread(target=continuous_blinking, args=(cli,), daemon=True)
        blinking_thread.start()
        
        run_with_cozmo(cli)

if __name__ == '__main__':
    main()