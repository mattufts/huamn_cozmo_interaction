import maze_env
import get_voice_command

 ########################cozmo program########################
import cozmo
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps

angle = 0
distance = 100
speed = 50
expression = None


async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()

async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

async def cozmo_program(robot: cozmo.robot.Robot):
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)

    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    await move_forward(robot, distance_to_move, speed_to_move)

async def cozmo_expression(robot: cozmo.robot.Robot):
    # change the expression based on what is front
    pass
# async def cozmo_program(robot: cozmo.robot.Robot):
#     global angle, distance, speed

#     print("Connected to Cozmo!")

#     while True:
#         angle_, distance_, speed_ = get_voice_command.get_command()
#         #print(angle, distance, speed)

#         if angle_ != 0:
#             angle = angle_
#             await turn_angle(robot, angle_)
#         if speed_ != 50 and speed_ != 0:
#             speed = speed_
#             await move_forward(robot, distance, speed)
#         if angle_ == 0 and speed_ == 0 and distance_ == 0:
#             await move_forward(robot, 8*speed, speed)
#         await asyncio.sleep(1) 

########################end cozmo program########################

env = maze_env.MazeEnv()
#cozmo = cozmo_bot.Cozmo() # initilization
state = env.reset()
done = False

while not done:
    angle, distance, speed_, action = get_voice_command.get_command_from_keyboard()
    state, reward, hit_wall, front, done, _ =env.step(action)
    cozmo.run_program(cozmo_program)
    cozmo.run_program(cozmo_expression)
    print(state, reward, hit_wall, front, done)