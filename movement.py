import maze_env
import get_voice_command
import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.anim import Triggers

# Set global variables
angle = 0
distance = 100
speed = 50

def cozmo_program(robot: cozmo.robot.Robot):
    print("Connected to Cozmo!")

async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()

async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

async def blink_eyes(robot: cozmo.robot.Robot):
    await robot.set_all_backpack_lights(cozmo.lights.blue_light.flash())
    await robot.play_anim_trigger(Triggers.BlockReact).wait_for_completed()
    await robot.set_all_backpack_lights(cozmo.lights.off_light)

async def cozmo_program(robot: cozmo.robot.Robot):
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)

    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    
    for i in range(int(distance_to_move/10)):
        await move_forward(robot, 10, speed_to_move)
        await blink_eyes(robot)

# Initialize environment and robot
env = maze_env.MazeEnv()
state = env.reset()
done = False

# Run the program
while not done:
    # Get command from keyboard
    angle, distance, speed_, action = get_voice_command.get_command_from_keyboard()

    # Move the robot according to the command
    state, reward, hit_wall, front, done, _ = env.step(action)
    cozmo.run_program(cozmo_program)

    # Print environment information
    print(state, reward, hit_wall, front, done)
