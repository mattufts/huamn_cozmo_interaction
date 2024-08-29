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
import copy
#import get_voice_command
import PycozmoFSM_controller as cozmo_controller
#import path_planner as path_planner
#from path_planner import find_shortest_path, determine_next_action, mark_forward
import pycozmo
import os
import PIL
from PIL import Image, ImageOps
import time
import Call_Animation
from gtts import gTTS
import os

text_to_say = "Hello, this is a test of Google Text-to-Speech in Python."
language = 'en'

speech = gTTS(text=text_to_say, lang=language, slow=False)

speech.save("output.mp3")

os.system("start output.mp3") 

#initialize threading event


def set_ads(angle, distance, speed):  
    cozmo_controller.Angle = angle
    cozmo_controller.Distance = distance
    cozmo_controller.Speed = speed

env = maze_env.MazeEnv()
state = env.reset()
done = False
display_flag = True

def show_neutral_image(cli):
    global display_flag
    #blinking_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
    #blinking_path = "Pycozmo Scripts/AnimImages/Blinking"
    neutral_image_path = "/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/blank.png"
    print("display_flag: ",display_flag)
    while True:
        # if animation_event.is_set():
        #     animation_event.wait()
      if display_flag:
            # Open the image using PIL
            image = Image.open(neutral_image_path)
            # Invert the image colors
            inverted_image = ImageOps.invert(image.convert('RGB'))
            
            # Depending on how Call_Animation.display_resized_image works, you might need to save the inverted image and pass the filepath
            # Or modify the display function to accept an image object directly
            inverted_image_path = '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/blank.png'
            inverted_image.save(inverted_image_path)
            
            # Display the inverted image
            Call_Animation.display_resized_image(cli, inverted_image_path)
            
            # Wait for a second before the next loop iteration
            time.sleep(1)


def handle_interaction (cli, interaction_type):
    #signal the start of an interaction animation_event

    # animation_paths = {
    #     "happy": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Happy",
    #     "sad": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Hurt",
    #     "angry": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Angry",
    #     "surprised": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Surprised",
    #     "neutral": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking",
    #     "left": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Left",
    #     "right": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Right",
    #     "finished": "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Successful",
    #                 }


        #     "angry" : "human_cozmo_interaction/Icon Images/stopping.png",
        # "happy" : "human_cozmo_interaction/Icon Images/check_mark.png",
        # "sad" : "human_cozmo_interaction/Icon Images/injured.png",
        # "surprised" : "human_cozmo_interaction/Icon Images/Alert_icon.png",
        # "neutral" : "human_cozmo_interaction/Icon Images/blank.png",
        # "left" : "human_cozmo_interaction/Icon Images/Notice_Left.png",
        # "right" : "human_cozmo_interaction/Icon Images/Notice_Right.png",
        # "finished" : "human_cozmo_interaction/Icon Images/finsih_flag"
    state_to_image = {
        # "angry" : "IconImages/stopping.png",
        # "happy" : "IconImages/check_mark.png",
        # "sad" : "IconImages/injured.png",
        # "surprised" : "IconImages/Alert_icon.png",
        # 'neutral' : "IconImages/blank.png",
        # "left" : "IconImages/notice_right.png",
        # "right" : "IconImages/Notice_Left.png",
        # "finished" : "IconImages/finish_flag.png"

        "angry": '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/stopping.png',
        "happy" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/check_mark.png',
        "sad" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/injured.png',
        "surprised" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/Alert_icon.png',
        "neutral" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/blank.png',
        "left" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/Notice_Left.png',
        "right" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/Notice_Right.png',
        "finished" : '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/IconImages/finish_flag.png'
    }
    Call_Animation.display_resized_image(cli, state_to_image[interaction_type])

    
        
#Defining the Keyboard Actions for Cozmo
def get_keyboard_command():
    command = input("Enter command (F = forward, L = left, R = right, S = stop, Q = quit): ")
    print(command)
    
    if 'F' in command:
        return 'forward'
    elif 'L' in command:
        return 'left'
    elif 'R' in command:
        return 'right'
    elif 'S' in command:
        return 'stop'
    elif 'Q' in command:
        return 'quit'
    
    return command
def clean_command(command):
    if 'F' in command:
        return 'forward'
    elif 'L' in command:
        return 'left'
    elif 'R' in command:
        return 'right'
    elif 'S' in command:
        return 'stop'
    elif 'Q' in command:
        return 'quit'
    return command
    
def convert_command_to_action(command):
    if command ==   'forward':
        return 2  #  2 is the action for moving forward in MazeEnv
    elif command == 'left':
        return 0  # 0 is the action for turning left
    elif command == 'right':
        return 1  #  1 is the action for turning right
    elif command == 'stop': 
        return 3
    return command

import threading
import keyboard
mode = 'automatic'
def keyboard_listener():
    global mode
    global env
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed('p'):
            if mode == 'automatic':
                mode = 'manual'
                print("Swiched to Manual Mode")
            else:
                mode = 'automatic'
                print("Swiched to Automatic Mode")
        if keyboard.is_pressed('m') and mode == 'manual':
            path_planner.mark_forward(env.nav_maze, env.current_pos, env.current_dir)
        if keyboard.is_pressed('c') and mode == 'manual':
            path_planner.mark_forward(env.nav_maze, env.current_pos, env.current_dir, 0)

def get_input(input_list):
    input_list[0] = input("Please type your command: ")
import path_planner
# Run Cozmo with updated behaviors
def run_with_cozmo(cli):
    import time
    action_list = ['left', 'right', 'forward', 'stop']
    global env, state, done, mode, display_flag
    env = maze_env.MazeEnv()
    state = env.reset()
    done = False
    front = 'nothing'
    print('Program is running')

    icon_display_time = 5
    user_id = "IVY_TONG" # change it everytime when you have a new participant



    respond_time = []
    # Start the keyboard listener
    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()
    while not done:
        cli.set_all_backpack_lights(pycozmo.lights.red_light) # three lines of them
        print("you can press p to swich now, current mode: ", mode)
        time.sleep(2) #increased
        
######################## choose action ############################
        print(mode)
        hit_wall = False
        #time.sleep(4)
        if mode == 'manual':
            cli.set_all_backpack_lights(pycozmo.lights.blue_light)
            # a backup solution for waiting for user input for 5 seconds
            # wait for user input for 5 seconds, if no inputs, skip the loop
            # Set up a thread to wait for input
            user_input = [None]
            start_time = time.time()
            print("\n\n\n\n Please input your command via keyboard.\n\n\n\n")
            while time.time() - start_time < 5:
                if keyboard.is_pressed('f'):
                    user_input[0] = 'forward'
                    break
                if keyboard.is_pressed('l'):
                    user_input[0] = 'left'
                    break
                if keyboard.is_pressed('r'):
                    user_input[0] = 'right'
                    break
                if keyboard.is_pressed('s'):
                    user_input[0] = 'stop'
                    break
                if keyboard.is_pressed('q'):
                    user_input[0] = 'quit'
                    break
                if keyboard.is_pressed('p'):
                    mode = 'automatic'
                    print("Swiched to Automatic Mode")
                    break
            respond_time.append(time.time() - start_time)

                  
            # Wait for 5 seconds
            if user_input[0] is None:
                current_pos = copy.deepcopy( env.current_pos)
                goal_pos = copy.deepcopy(env.goal_pos)
                #print(goal_pos)
                next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
        
                action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))
                command = action_list[action]
            else:
                command = user_input[0]
               # command = clean_command(command)
           # command = get_keyboard_command()
        else:
            current_pos = copy.deepcopy( env.current_pos)
            goal_pos = copy.deepcopy(env.goal_pos)
            #print(goal_pos)
            next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
     
            action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))
            command = action_list[action]
            print("command: ", command)

        
        action = convert_command_to_action(command)
        print(action)


        if command == 'quit':
            break
        elif command == 'invalid':
            print("Invalid command. Try again.")
            continue
        
 
        if command == 'left':
            cozmo_controller.turn_angle(cli, -75)

        if command == 'right':
            cozmo_controller.turn_angle(cli, 75)

        if command == 'forward' and front == "nothing":
            cozmo_controller.move_forward(cli, 80, 50)# Example: move forward 80 units at speed 50
        
        if command == 'forward' and front != "nothing":
            #if front == "wall":
                #env.health = -20
            if front == "fire":
                env.health = (env.health)-30
            hit_wall = True
            
            cozmo_controller.move_forward(cli, 20, 10)
            cozmo_controller.move_forward(cli, -20, -10)
            #cozmo_controller.front = front
            #handle_interaction(cli, 'sad')

        if action is not None:
            state, _, _, front , done = env.step(action)

        

        if hit_wall:
            # Cozmo hits a wall, play "Hurt" animation
            display_flag = False
            handle_interaction(cli, "sad")
            time.sleep(icon_display_time)
            display_flag = True
        
        if env.health <= 0:
            display_flag = False
            handle_interaction(cli, "angry")
            time.sleep(icon_display_time)
            display_flag = True
            break
        
        current_pos = copy.deepcopy( env.current_pos)
        goal_pos = copy.deepcopy(env.goal_pos)
        next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
        next_action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))

        # display animation based on the next action
        if next_action == 0:
            display_flag = False
            handle_interaction(cli,"left")
            time.sleep(icon_display_time)
            display_flag = True
        if next_action == 1:
            display_flag = False
            handle_interaction(cli,"right")
            time.sleep(icon_display_time)
            display_flag = True
        if next_action == 2:
            display_flag = False
            handle_interaction(cli, "happy")
            time.sleep(icon_display_time)
            display_flag = True






    file_name = "respond_time" + user_id + ".txt"
    if os.path.exists(file_name):
        print("File already exists. file name has been changed")
        file_name = "respond_time" + user_id + str(time.time()) + ".txt"
    with open(file_name, "w") as f:
        for time in respond_time:
            f.write(str(time) + "\n")
        f.write(str(done))
    print("The file has been saved as: ", file_name)
            
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
        #neutral_thread=os.path.join(os.path.dirname(__file__), "emoticons", "blank.png")
        #blinking_thread.start()
        neutral_thread = threading.Thread(target=show_neutral_image, args=(cli,))
        neutral_thread.start()
        
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

