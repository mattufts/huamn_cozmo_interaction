
#main execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen


#The scripts that MainDemo imports are:
    #maze_env.py
    #PycozmoFSM_Animation.py
    #path_planner for navigation
#script that was worked on 3/5/2024
        #script has been updated and approved for final study 8/30/2024

#main execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen


import os
import time
import threading
import copy
import pycozmo
import path_planner
import keyboard
import random
import string
import maze_env
import PycozmoFSM_Animation as cozmo_controller
from Call_Animation import display_blink_eyes, execute_interaction_animation

# Change working directory to ensure paths are correctly resolved
os.chdir("/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts")

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the Blinking directory and other necessary directories
blinking_path = os.path.join(script_dir, "AnimImages", "Blinking")
data_path = os.path.join(script_dir, "data")

# You can print these to verify the paths
print("Blinking path:", blinking_path)
print("Data path:", data_path)

# Initialize threading event
animation_event = threading.Event()

env = maze_env.MazeEnv()
state = env.reset()
done = False
display_flag = True
wall = 0
mode = 'manual'


#************************************Global Variables****************************************
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the Blinking directory
blinking_path = os.path.join(script_dir, "AnimImages", "Blinking")

# You can print this to verify the patha
print("Blinking path:", blinking_path)

# Now, use blinking_path wherever it is needed in your script


#initialize threading event
animation_event = threading.Event()


env = maze_env.MazeEnv()
state = env.reset()
done = False
display_flag = True
wall = 0
mode = 'manual'

#************************************End of Global Variables****************************************


#************************************Display Animation****************************************


# Display blinking eyes continuously, this is for the neutral state

def continuous_blinking(cli):
    global display_flag
    blinking_path = os.path.join(script_dir, "AnimImages", "Blinking")
    print("display_flag: ", display_flag)
    while True:
        if display_flag:
            display_blink_eyes(cli, base_path=blinking_path, fps=24, duration=1)
        # Adding a sleep to reduce CPU usage and prevent overwhelming Cozmo
        time.sleep(1.5)



def handle_interaction (cli, interaction_type, repeat_count=1):
#signal the start of an interaction animation_event
    animation_event.set()
    for _ in range(repeat_count):
        # Request the Call_Animation script to execute the animation for the interaction
        execute_interaction_animation(cli, interaction_type)
        time.sleep(1)  # Add a delay between repetitions if needed

    # Clear the event after the animation request to resume default behavior    
    animation_event.clear()
#************************************End of Display Animation functions****************************************


    

#************************************Get Commands from Keyboard**************************************** 

#Defining the Keyboard Actions for Cozmo  #This can be done in a swtich statement 
def get_keyboard_command():
    command = input("Enter command (F = forward, L = left, R = right, S = stop, Q = quit): ")
    print(command)
    
    if 'F' in command:  #these could be done in a switch statement
                        #convert everything to a lowercase
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
    
def convert_command_to_action(command):   #using enumerators could simplify this script 
                                          #this would make sure that variables are defined and prevent incorrect keys
    if command ==   'forward':
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
        #if keyboard.is_pressed('p'):    #change to on release 
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

#************************************End of Keyboard funtions****************************************





#************************************Procedure Code****************************************
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


########ENTER USERNAME HERE########
    user_id = "Participant_6:54" # change it everytime when you have a new participant
    # random generated a 10 character user_id without using time
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    print("User ID: ", user_id)
    start_time = time.time()

    #write basic info to a file in data folder
    info_file = "data/" + user_id + "_info.txt"
    with open(info_file, "w") as f:
        f.write(user_id + "\n")
        f.write(str(start_time) + "\n")
        f.write("Animate Eyes\n")
        f.write("MAZE NAME: A\n")
        f.close()
    #initialize the traj file
    traj_file = "data/" + user_id + "_traj.txt"
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
    # Start the keyboard listener
    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()
    while not done:
        current_step += 1
        with open(traj_file, "a") as f:
            f.write("*****************************************************\n")
            f.write("current_step: " + str(  current_step) + "\n")
            f.write("current_pos:" + str( env.current_pos) +"\n")
            f.write("current_dir:"+ str( env.current_dir )+ "\n") 
            f.write("current_health:"+ str(  env.health) +"\n") 
            f.close()
        cli.set_all_backpack_lights(pycozmo.lights.red_light) # three lines of them
        print("you can press p to swich now, current mode: ", mode)
        #time.sleep(1) #increased
######################## choose action ############################
        print(mode)
        hit_wall = False
        
        print(f"Current Position: {env.current_pos}, Goal Position: {env.goal_pos}")  # Add this line here

        if (env.current_pos == env.goal_pos).all():
            # Play the "Winking" animation
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "finished", repeat_count=2)
            display_flag = True

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
                f.write("Status: Successfully completed the goal!\n")
                f.close()
            
            # Now set done to True to end the loop
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
            display_flag = True
        if next_action == 1:
            display_flag = False
            time.sleep(1)
            handle_interaction(cli,"right")
            display_flag = True
        if next_action == 2:
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "up")
            display_flag = True

        #time.sleep(4)
        if mode == 'manual':
            cli.set_all_backpack_lights(pycozmo.lights.blue_light)
            # a backup solution for waiting for user input for 5 seconds
            # wait for user input for 5 seconds, if no inputs, skip the loop
            # Set up a thread to wait for input
            user_input = [None]
            start_time = time.time()
            print("\n\n\n\n Please input your command via keyboard.\n\n\n\n")
            while time.time() - start_time < 5:  #this can be put in a variable once
                                                #put start.time under the start time
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
                    # mode = 'automatic'
                    # print("Swiched to Automatic Mode")
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
                for _ in range(2):
                    cli.set_all_backpack_lights(pycozmo.lights.green_light)
                    time.sleep(0.3)
                    cli.set_all_backpack_lights(pycozmo.lights.white_light)
                    time.sleep(0.3)
                cli.set_all_backpack_lights(pycozmo.lights.red_light)
                command = user_input[0]
                cmd_cnt += 1
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

        current_pos = copy.deepcopy(env.current_pos)
        goal_pos = copy.deepcopy(env.goal_pos)
        next_move = path_planner.find_shortest_path(env.nav_maze, current_pos, goal_pos)

        # Assuming command comes from user input and action is determined by path planner
        if mode == 'manual' and user_input[0] is not None and action == path_planner.determine_next_action(current_pos, next_move, tuple(env.current_dir)):
            # Show an alignment face, currently using happy face
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "happy")
            display_flag = True
            #time.sleep(1)
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
                f.write("hit_wall_cnt: "+ str( hit_wall_cnt )+"\n")
                f.write("hit_fire_cnt: "+ str( hit_fire_cnt)+"\n")
                f.write("consistent_cnt: "+ str( consistent_cnt)+"\n")
                f.write("inconsistent_cnt: "+ str( inconsistent_cnt)+ "\n")
                f.write("auto_cnt: "+ str( auto_cnt)+ "\n")
                f.write("total_steps: "+ str( current_step)+ "\n")
                f.write("human_commands: "+ str( cmd_cnt)+ "\n")
                f.write("end_health: "+ str( env.health)+ "\n")
                f.write("end_time: "+ str(  time.time())+ "\n")
                        # Write manual quit message to file
                f.write("Status: Manually Quit by User\n")
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
            print("front: ", front)
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
            # Cozmo hits a wall, play "Hurt" animation
            pass

        
        if env.health <= 0:
            with open(info_file, "a") as f:
                f.write("Status: Robot failed (health = 0).\n")
                f.close()
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "sad")
            display_flag = True
            break
        
        elif current_step >=25:
            with open(info_file, "a") as f:
                f.write("Status: Robot failed (too many moves).\n")
                f.close()
            display_flag = False
            time.sleep(1)
            handle_interaction(cli, "sad")
            display_flag = True
            break


    with open(info_file, "a") as f:
        f.write("hit_wall_cnt: "+ str( hit_wall_cnt )+"\n")
        f.write("hit_fire_cnt: "+ str( hit_fire_cnt)+"\n")
        f.write("consistent_cnt: "+ str( consistent_cnt)+"\n")
        f.write("inconsistent_cnt: "+ str( inconsistent_cnt)+ "\n")
        f.write("auto_cnt: "+ str( auto_cnt)+ "\n")
        f.write("total_steps: "+ str( current_step)+ "\n")
        f.write("human_commands: "+ str( cmd_cnt)+ "\n")
        f.write("end_health: "+ str( env.health)+ "\n")
        f.write("end_time: "+ str(  time.time())+ "\n")
        f.write ("total time: " + start_time- time.time() + "\n")
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

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        cli.set_head_angle(head_angle)
        cli.wait_for_robot()

        # Start the blinking thread
        blinking_thread = threading.Thread(target=continuous_blinking, args=(cli,), daemon=True)
        blinking_thread.start()

        # Start the main thread
        run_with_cozmo(cli)

if __name__ == '__main__':
    main()