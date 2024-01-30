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
import os

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
    blinking_thread.start()
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
    
def convert_command_to_action(command):
    if command ==  'F':
        return 2  # Assuming 2 represents forward in your maze environment
    elif command == 'L':
        return 0  # Assuming 0 represents a left turn
    elif command == 'R':
        return 1  # Assuming 1 represents a right turn
    # Add more conditions if needed
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
        if command == 'quit':
            break
        elif command == 'invalid':
            print("Invalid command. Try again.")
            continue
        
        # Convert command to action for the maze environment
        action = convert_command_to_action(command)
        
        # Update Cozmo's state in the maze
        state, reward, hit_wall, front, done, _ = env.step(action)

        if hit_wall:
            # Cozmo hits a wall, play "Hurt" animation
            handle_interaction(cli, "sad")
        elif done:
            # Cozmo reaches the end of the maze, play "Happy" animation
            handle_interaction(cli, "happy")
        elif action == 2 and can_move_left_or_right():
            # Cozmo is moving forward and there is a path to the left or right
            if is_path_left():
                handle_interaction(cli, "left")
            elif is_path_right():
                handle_interaction(cli, "right")
            else:
                handle_interaction(cli, front)
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
        run_with_cozmo(cli)


if __name__ == '__main__':
    main()

#VoiceCommandScript
#Removed temporarily 1/27/2024