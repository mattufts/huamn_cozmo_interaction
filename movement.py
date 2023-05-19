import cozmo
import get_voice_command
import asyncio
import maze_env
import maze
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image

# Define the maze environment
env = maze_env.MazeEnv()

# Define the robot's movement parameters
angle = 0
distance = 95
speed = 50

def move_forward():
    # Use Cozmo SDK to make the robot move forward
    robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()


def turn_left():
    # Use Cozmo SDK to make the robot turn left
    set_ads(-90, 0, 0)

def turn_right():
    # Use Cozmo SDK to make the robot turn right
    set_ads(90, 0, 0)

# env = maze_env.MazeEnv()
# #cozmo = cozmo_bot.Cozmo() # initialization
# state = env.reset()
# done = False

# while not done:
#     angle, distance, speed, action = get_voice_command.get_command_from_keyboard()
#     print(action, type(action))
#     state, reward, hit_wall, front, done, _ = env.step(action)

#     if hit_wall:
#         # If hit wall, show temptation
#         cozmo_controller.angle = 0
#         cozmo_controller.distance = 10
#         cozmo_controller.speed = 10
#         cozmo.run_program(cozmo_controller.act)
#         cozmo_controller.distance = -10
#         cozmo.run_program(cozmo_controller.act)
#         cozmo_controller.front = "hit"
#         cozmo.run_program(cozmo_controller.cozmo_show_img)
#     else:
#         # Check if current location in the maze is a '0' or '1'
#         current_position = env.get_current_position()
#         if env.maze[current_position[0]][current_position[1]] == '0':
#             # Move forward if current position is '0'
#             move_forward()
#         elif env.maze[current_position[0]][current_position[1]] == '1':
#             # Stop abruptly if current position is '1'
#             # Use Cozmo SDK to stop the robot
#             pass

#     cozmo_controller.front = front
#     cozmo.run_program(cozmo_controller.cozmo_show_animation)

#     print(state, reward, hit_wall, front, done)
#     print(env.maze)