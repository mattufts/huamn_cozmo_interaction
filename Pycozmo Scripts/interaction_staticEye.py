#main execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen

#The scripts that MainDemo imports are:
    #maze_env.py
    #PycozmoFSM_Animation.py
    #path_planner for navigation
#script that was worked on 3/5/2024
import os
import time
import threading
import copy
import pycozmo
import path_planner
import random
import string
import keyboard
import maze_env
import PycozmoFSM_controller as cozmo_controller
from Call_Animation import display_resized_image, execute_interaction_animation
from PIL import Image, ImageOps

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

#Construct the paths to the necessary directories
neutral_image_path = os.path.join(script_dir, "..", "Emotion_Eyes", "Emoticons", "neutral.png")
data_path = os.path.join(script_dir, "data")
emotion_image_dir = os.path.join(script_dir, "..", "Emotion_Eyes", "Emoticons")

state_to_image = {
    'up': os.path.join(emotion_image_dir, 'up.png'),    
    'left': os.path.join(emotion_image_dir, 'glancing_left-01.png'),
    'right': os.path.join(emotion_image_dir, 'glacing_right-01.png'),
    'happy': os.path.join(emotion_image_dir, 'happy.png'),
    'sad': os.path.join(emotion_image_dir, 'injured_sad-01.png'),
    'neutral': os.path.join(emotion_image_dir, 'neutral.png'),
    'crash': os.path.join(emotion_image_dir, 'crash.png'),
    'finished': os.path.join(emotion_image_dir, 'wink.png')
}

# state_to_image = {
#     'up': os.path.join(emotion_image_dir, 'notice_up.jpg'),    
#     'left': os.path.join(emotion_image_dir, 'notice_left.png'),
#     'right': os.path.join(emotion_image_dir, 'notice_right.png'),
#     'happy': os.path.join(emotion_image_dir, 'check_mark.png'),
#     'sad': os.path.join(emotion_image_dir, 'injured.png'),
#     'neutral': os.path.join(emotion_image_dir, 'neutral.png'),
#     'crash': os.path.join(emotion_image_dir, 'stopping.png'),
#     'finished': os.path.join(emotion_image_dir, 'finish_flag.png')
#     }


print("Current working directory:", os.getcwd())
print("Emotion image directory:", emotion_image_dir)


# You can print these to verify the paths
print("Neutral image path:", neutral_image_path)
print("Data path:", data_path)

# Initialize threading event
#animation_event = threading.Event()

env = maze_env.MazeEnv()
state = env.reset()
done = False
display_flag = True
mode = 'manual'
#************************************Display Image ***************************************

def show_neutral_image(cli):
    global display_flag
    print("display_flag: ", display_flag)
    while True:
        if display_flag:
            display_resized_image(cli, neutral_image_path)
            time.sleep(3)


def handle_interaction(cli, interaction_type):
    global state_to_image
    
    if interaction_type in state_to_image:
        image_path = state_to_image[interaction_type]
        if os.path.exists(image_path):
            display_resized_image(cli, image_path)
        else:
            print(f"Image file not found: {image_path}")
    else:
        print(f"Interaction type '{interaction_type}' not recognized.")

#************************************Keyboard Commands**************************************** 

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
    if command == 'forward':
        return 2  #  2 is the action for moving forward in MazeEnv
    elif command == 'left':
        return 0  # 0 is the action for turning left
    elif command == 'right':
        return 1  #  1 is the action for turning right
    elif command == 'stop': 
        return 3
    return command

def keyboard_listener():
    global mode
    global env
    while True:
        #time.sleep(0.1)
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
#********************************End of Keyboard Functions****************************************


#************************************Procedure Code****************************************
def run_with_cozmo(cli):
    import time
    action_list = ['left', 'right', 'forward', 'stop']
    global env, state, done, mode, display_flag
    env = maze_env.MazeEnv()
    state = env.reset()
    done = False
    front = 'nothing'
    action = None  # Initialize action to ensure it's always defined
    print('Program is running')


########ENTER USERNAME HERE########
    # random generated a 10 character user_id without using time
    user_id = "Participant_10:52 " # change it everytime when you have a new participant
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print("User ID: ", user_id)   
    start_time = time.time()

    info_file = os.path.join(data_path, user_id + "_info.txt")
    with open(info_file, "w") as f:
        f.write(user_id + "\n")
        f.write(str(start_time) + "\n")
        f.write("Static Eyes\n")
        f.write("MAZE NAME: A")           ###REMEMBER TO CHANGE THIS
        f.close()

    traj_file = os.path.join(data_path, user_id + "_traj.txt")
    with open(traj_file, "w") as f:
        f.close()

    current_step = 0
    hit_wall_cnt = 0
    hit_fire_cnt = 0
    consistent_cnt = 0
    inconsistent_cnt = 0
    auto_cnt = 0
    cmd_cnt = 0

    respond_time = []
    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()
    while not done:
        current_step += 1
        with open(traj_file, "a") as f:
            f.write("*****************************************************\n")
            f.write("current_step: " + str(current_step) + "\n")
            f.write("current_pos:" + str(env.current_pos) + "\n")
            f.write("current_dir:" + str(env.current_dir) + "\n")
            f.write("current_health:" + str(env.health) + "\n")
            f.close()
        cli.set_all_backpack_lights(pycozmo.lights.red_light)
        print(f"You can press 'p' to switch modes. Current mode: {mode}")

        ######################## choose action ############################
        print(mode)
        hit_wall = False

        print(f"Current Position: {env.current_pos}, Goal Position: {env.goal_pos}")  # Add this line here


        # Determine the next action
        if (env.current_pos == env.goal_pos).all():
            # Hardcode the display of the 'finished_flag.png' icon
            finished_image_path = os.path.join(emotion_image_dir, 'wink.png')
        
            # Check if the image exists before displaying
            if os.path.exists(finished_image_path):
                display_flag = False
                time.sleep(1)  # Add a slight delay before displaying the final image
                
                # Display the final image using the display_resized_image function
                display_resized_image(cli, finished_image_path)
                
                time.sleep(5)  # Keep the image displayed for 5 seconds
                display_flag = True
            else:
                print(f"Finished image not found: {finished_image_path}")

            # Print congratulatory message
            print("You have completed the course! Congratulations!")

            # Record data to the info_file
            with open(info_file, "a") as f:
                f.write("hit_wall_cnt: " + str(hit_wall_cnt) + "\n")
                f.write("hit_fire_cnt: " + str(hit_fire_cnt) + "\n")
                f.write("consistent_cnt: " + str(consistent_cnt) + "\n")
                f.write("inconsistent_cnt: " + str(inconsistent_cnt) + "\n")
                f.write("auto_cnt: " + str(auto_cnt) + "\n")
                f.write("total_steps: " + str(current_step) + "\n")
                f.write("human_commands: " + str(cmd_cnt) + "\n")
                f.write("end_health: " + str(env.health) + "\n")
                f.write("end_time: " + str(time.time()) + "\n")
                f.close()

            done = True

            # Prompt the user to manually hit "Q" to end the session
            while True:
                end_command = input("Press 'Q' to quit: ").strip().upper()
                if end_command == 'Q':
                    print("Session ended.")
                    break
            break

        # showing an instruction before the user input
        current_pos = copy.deepcopy(env.current_pos)
        goal_pos = copy.deepcopy(env.goal_pos)
        next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
        next_action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))


        # display animation based on the next action
        if next_action == 0:
            display_flag = False
            time.sleep(1)
            handle_interaction(cli,"left")
            time.sleep(3) 
            display_flag = True
        if next_action == 1:
            display_flag = False
            time.sleep(1)
            handle_interaction(cli,"right")
            time.sleep(3) 
            display_flag = True
        if next_action == 2:
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "up")
            time.sleep(3) 
            display_flag = True



        if mode == 'manual':
            cli.set_all_backpack_lights(pycozmo.lights.blue_light)
            # a backup solution for waiting for user input for 5 seconds
            # wait for user input for 5 seconds, if no inputs, skip the loop
            # Set up a thread to wait for input
            # Get command from user input
            user_input = [None]
            start_time = time.time()
            print("\n\n\n\n Please input your command via keyboard.\n\n\n\n")
            while time.time() - start_time < 10:  # 10 seconds to respond
                if keyboard.is_pressed('f') or keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    user_input[0] = 'forward'
                    break
                if keyboard.is_pressed('l') or keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                    user_input[0] = 'left'
                    break
                if keyboard.is_pressed('r') or keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                    user_input[0] = 'right'
                    break
                 # if keyboard.is_pressed('s'):
                #     user_input[0] = 'stop'
                #     break

                if keyboard.is_pressed('q'):
                    user_input[0] = 'quit'
                    break
                if keyboard.is_pressed('p'):
                    auto_cnt += 1 
                    break
            respond_time.append(time.time() - start_time)


                  
            # Wait for 20 seconds
            if user_input[0] is None:                   #This script here replicates the movement that the robot is going to to take its predetermined path after waiting
                current_pos = copy.deepcopy( env.current_pos)
                goal_pos = copy.deepcopy(env.goal_pos)
                #print(goal_pos)
                next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
        
                action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))
                command = action_list[action]
            else:
                for _ in range(3):
                    cli.set_all_backpack_lights(pycozmo.lights.green_light)
                    time.sleep(0.5)
                    cli.set_all_backpack_lights(pycozmo.lights.white_light)
                    time.sleep(0.5)
                cli.set_all_backpack_lights(pycozmo.lights.red_light)
                command = user_input[0]
                cmd_cnt += 1
           # command = clean_command(command)
           # command = get_keyboard_command()
        else:
            current_pos = copy.deepcopy( env.current_pos)
            goal_pos = copy.deepcopy(env.goal_pos)
            #print(goal_pos)
            next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)
     
            action = path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))
            command = action_list[action]   #enumerators would automatically adjust for this
            print("command: ", command)

        
        action = convert_command_to_action(command)
        print(action)

        current_pos = copy.deepcopy( env.current_pos)
        goal_pos = copy.deepcopy(env.goal_pos)
            #print(goal_pos)
        next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)


# Assuming command comes from user input and action is determined by path planner
        if mode == 'manual' and user_input[0] is not None and action == path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir)):
            # Show an alignment face, currently using happy face
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "happy")
            time.sleep(3) 
            display_flag = True
            time.sleep(1)
            consistent_cnt += 1
        else:
            inconsistent_cnt += 1

        with open(traj_file, "a") as f:
            f.write("current_time: " + str(time.time()) + "\n")
            f.write("respond_time: " + str(respond_time[-1]) + "\n")
            f.write("action: " + str(action) + "\n")
            f.write("command: " + str(command) + "\n")
            f.write("indicated next action: " + str(path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir))) + "\n")
            
            if mode == 'manual' and action == path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir)):
                f.write("consistent: " + "Yes" + "\n")
            else:
                f.write("consistent: " + "No" + "\n")
                inconsistent_cnt += 1
            f.close()


        if command == 'quit':
            with open(info_file, "a") as f:
                f.write("hit_wall_cnt: "+ str(hit_wall_cnt) +"\n")
                f.write("hit_fire_cnt: "+ str(hit_fire_cnt) +"\n")
                f.write("consistent_cnt: "+ str(consistent_cnt) +"\n")
                f.write("inconsistent_cnt: "+ str(inconsistent_cnt)+ "\n")
                f.write("auto_cnt: "+ str(auto_cnt)+ "\n")
                f.write("total_steps: "+ str(current_step)+ "\n")
                f.write("human_commands: "+ str(cmd_cnt)+ "\n")
                f.write("end_health: "+ str(env.health)+ "\n")
                f.write("end_time: "+ str( time.time())+ "\n")
                f.close()
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
             #env.health = 0
            #wall = wall+1
            cozmo_controller.move_forward(cli, 20, 10)
            if front == "fire":
                env.health -= 20
                display_flag = False
                time.sleep(1)
                handle_interaction(cli, "sad")
                time.sleep(3) 
                display_flag = True
                hit_fire_cnt += 1
                with open(traj_file, "a") as f:
                    f.write("hit fire: " + "Yes"+ "\n")
                    f.write("hit wall: " + "No"+ "\n")
                    f.close()
            else:
                env.health -= 10
                hit_wall_cnt += 1
                display_flag = False
                time.sleep(1)
                handle_interaction(cli, "crash")
                time.sleep(3) 
                display_flag = True
                with open(traj_file, "a") as f:
                    f.write("hit fire: "+ "No"+ "\n")
                    f.write("hit wall: "+ "Yes"+ "\n")
                    f.close()
            hit_wall = True   
            #time.sleep(1)


            cozmo_controller.move_forward(cli, -20, -10)
            #cozmo_controller.front = front
            #handle_interaction(cli, 'sad')
        else:
          # normal forward movement
            
            with open(traj_file, "a") as f:
                f.write("hit fire: "+ "No" + "\n")
                f.write("hit wall: "+ "No" + "\n")
                f.close()

    
        if action is not None:
           state, _, _, front , done = env.step(action)
        

        if hit_wall:
            pass
        
        
       
        if env.health <= 0:
            with open(info_file, "a") as f:
                f.write("Status: Robot failed (health = 0).\n")
                f.close()
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "sad")
            time.sleep(3) 
            display_flag = True
            break
        
        elif current_step >=25:
            with open(info_file, "a") as f:
                f.write("Status: Robot failed (health = 0).\n")
                f.close()
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "sad")
            time.sleep(3) 
            display_flag = True
            break

    with open(info_file, "a") as f:
        f.write(f"Hit Wall Count: {hit_wall_cnt}\n")
        f.write(f"Hit Fire Count: {hit_fire_cnt}\n")
        f.write(f"Consistent Count: {consistent_cnt}\n")
        f.write(f"Inconsistent Count: {inconsistent_cnt}\n")
        f.write(f"Auto Mode Count: {auto_cnt}\n")
        f.write(f"Total Steps: {current_step}\n")
        f.write(f"Human Commands: {cmd_cnt}\n")
        f.write(f"End Health: {env.health}\n")
        f.write(f"End Time: {time.time()}\n")
        f.close()
#************************************End of Procedure Code****************************************


#**************************These are helper functions****************************************************
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
#****************************End of helper functions******************************************************


#************************************End of Procedure Code****************************************

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
    
        run_with_cozmo(cli)


if __name__ == '__main__':
    main()