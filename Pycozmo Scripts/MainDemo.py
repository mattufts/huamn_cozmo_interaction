#Main Execution Code
#This code utilizes maze environment.py and cozmo_controller.py to test the maze environment
#This shows the functionality together, but the code can be broken up into
#different sections in order to test the screen
#Code implements the pycozmo library

#The five scripts that this imports are:
    #maze_env.py
    #PycozmoFSM.py
    #Pycozmo_controller.py
    #navigation path

#other scripts that aren't incorporated here but are still considered
#get_voice_command.py

import maze_env
#import get_voice_command
import PycozmoFSM_controller as cozmo_controller
import pycozmo
import os

def set_ads(angle, distance, speed):  
    cozmo_controller.Angle = angle
    cozmo_controller.Distance = distance
    cozmo_controller.Speed = speed

env = maze_env.MazeEnv()
state = env.reset()
done = False

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

def show_neutral_image(cli):
    #neutral_image_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/emoticons/neutral.png"
    #for raspberry
    neutral_image_path = "/home/matt_e/Documents/Github_Projects/HumanCozmoInteraction/huamn_cozmo_interaction/Pycozmo Scripts/emoticons/neutral.png"
    cozmo_controller.show_image(cli, neutral_image_path)

#Keyboard Controls For Cozmo   
def run_with_cozmo(cli):
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
        if command in {'left', 'right', 'forward'}:
            cozmo_controller.update_state_and_image(cli, command)
        else: 
            #default to blinking
            show_neutral_image(cli)
            continue
        cozmo_controller.update_state_and_image(cli, front) 

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle) 
        cli.wait_for_robot()
        run_with_cozmo(cli)

if __name__ == '__main__':
    main()

#async scripts deleted 2/29/24

#VoiceCommandScript
# def run_with_cozmo(cli):
#     global state, done
#     while not done: # start loop 
#         angle, distance, speed, action = get_voice_command.get_command_from_keyboard()
#         print(action, type(action))
#         state, reward, hit_wall, front, done, _ = env.step(action) 
#         if hit_wall:
#             set_ads(0, 10, 10) #angle distance and speed
#             cozmo_controller.act(cli)
#             set_ads(0, -10, 10)
#             cozmo_controller.act(cli)
#             cozmo_controller.front = "hit"
#         else:    

#             set_ads(angle, distance, speed)
#             cozmo_controller.act(cli)
#         cozmo_controller.front = front
#         print(state, reward, hit_wall, front, done)
#         print(env.maze)

# def main():
#     with pycozmo.connect() as cli:
#         cli.wait_for_robot()
#         run_with_cozmo(cli)

# if __name__ == '__main__':
#     main()
