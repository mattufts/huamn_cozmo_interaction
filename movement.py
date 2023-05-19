import cozmo
import asyncio
import maze_env
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image

# Define the maze environment
env = maze_env.MazeEnv()

# Define the robot's movement parameters
angle = 0
distance = 100
speed = 50
expression = None #cozmo's current facial expression
front = None #what is in front of cozmo
duration = 2000 #how long to display the image

async def turn_angle(robot: cozmo.robot.Robot, angle: float):
    await robot.turn_in_place(degrees(angle)).wait_for_completed()

async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
    await robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

async def act(robot: cozmo.robot.Robot):
    # Turn Cozmo by a specific angle (in degrees)
    angle_to_turn = angle  # Set the angle you want to turn (in degrees)
    await turn_angle(robot, angle_to_turn)
    # Move Cozmo forward by a specific distance (in millimeters)
    distance_to_move = distance  # Set the distance you want to move (in millimeters)
    speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
    await move_forward(robot, distance_to_move, speed_to_move)

async def cozmo_show_img(robot: cozmo.robot.Robot):
    # change the expression based on what is front
    img = None
    if front == "wall":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/Alert_icon.png" 
    if front == "nothing":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/check_mark.png"
    if front == "goal":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/finish_flag.png"
    if front == "hit":
        img = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Icon Images/injured.png"
    
    if img is not None:
        image = Image.open(img)
        resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
        robot.display_oled_face_image(face_image, duration)
async def cozmo_show_animation(robot: cozmo.robot.Robot):
    img = []
    if front == "wall":
        path = "/home/jstaley/hang_yu/huamn_cozmo_interaction/Emotion_Eyes/Blinking/eyes_blink"
        for i in range(1, 7):
            img.append(path + str(i) + ".png")
    if front == "nothing":
        pass
    if len(img) > 0:
        for i in range(0, len(img)):
            image = Image.open(img[i])
            resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
            face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
            robot.display_oled_face_image(face_image, duration/2)
            await asyncio.sleep(0.2)


# # Define the robot's OLED face images
# face_images = {
#     "happy": Image.open("Alert_icon.png"),
#     "sad": Image.open("check_mark.png"),
#     "neutral": Image.open("finish_flag.png")
# }

# # Define the robot's blinking animation
# async def blink(robot: cozmo.robot.Robot):
#     robot.set_all_backpack_lights(cozmo.lights.blue_light.flash())
#     await asyncio.sleep(0.2)
#     robot.set_all_backpack_lights(cozmo.lights.blue_light)
#     await asyncio.sleep(0.2)
#     robot.set_all_backpack_lights(cozmo.lights.off)

# # Define the robot's movement functions
# async def turn_angle(robot: cozmo.robot.Robot, angle: float):
#     await robot.turn_in_place(degrees(angle)).wait_for_completed()

# async def move_forward(robot: cozmo.robot.Robot, distance: float, speed: float):
#     await robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

# # Define the robot's program
# async def cozmo_program(robot: cozmo.robot.Robot):
#     # Display the neutral face image
#     robot.display_oled_face_image(face_images["neutral"], 5000)

#     # Turn Cozmo by a specific angle (in degrees)
#     angle_to_turn = angle  # Set the angle you want to turn (in degrees)
#     await turn_angle(robot, angle_to_turn)

#     # Move Cozmo forward by a specific distance (in millimeters)
#     distance_to_move = distance  # Set the distance you want to move (in millimeters)
#     speed_to_move = speed  # Set the speed you want to move (in millimeters per second)
#     await move_forward(robot, distance_to_move, speed_to_move)

#     # Blink while Cozmo is moving
#     await blink(robot)

#     # Display the happy face image
#     robot.display_oled_face_image(face_images["happy"], 5000)

# # Run the maze program
# async def run_maze():
#     with cozmo.robot.Robot() as robot:
#         # Reset the maze environment
#         state = env.reset()
#         done = False

#         while not done:
#             # Get the robot's movement parameters and action from user input
#             angle, distance, speed_, action = get_voice_command.get_command_from_keyboard()

#             # Step the environment based on the action
#             state, reward, hit_wall, front, done, _ = env.step(action)

#             # Run the Cozmo program
#             await cozmo_program(robot)

#             # Display the sad face image if Cozmo hits a wall
#             if hit_wall:
#                 robot.display_oled_face_image(face_images["sad"], 5000)
#             else:
#                 robot.display_oled_face_image(face_images["neutral"], 5000)

#             # Print the state of the environment
#             print(state, reward, hit_wall, front, done)

# # Run the maze program
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run_maze())