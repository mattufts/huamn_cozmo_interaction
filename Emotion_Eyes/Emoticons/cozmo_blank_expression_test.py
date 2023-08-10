#Script that tests out blank images and paused movement with the cozmo robot

import sys
import time

try: 
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")
    
import cozmo
#import asyncio 

async def cozmo_show_img(robot: cozmo.robot.Robot):
    # Use a blank image
    image_settings = [("blank.png", Image.BICUBIC),
                      ("blank.png", Image.NEAREST)]
    face_image = [ ]
    for image_name, resampling in image_settings:
        # Load the image and resize it
        image = Image.open(image_name)
        resized_image = image.resize(cozmo.oled_face.dimensions(), resampling)
        image = image.resize(cozmo.oled_face.dimensions(), resampling)
        face_image.append(cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True))
        face_image.append (face_image)
    
    num_loops = 10
    duration_s = 1000
    # Load the image and resize it
    print("Press CTRL-C to quit (or wait %s seconds to complete)" % int(num_loops*duration_s) )
    
    for _ in range(num_loops):
        for image in face_image:
            robot.display_oled_face_image(image, duration_s * 1000.0)
            time.sleep(duration_s)


    # resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)

    # # Convert the image to the format used by the oled screen
    # face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)

    # # Display the blank image on Cozmo's face
    # robot.display_oled_face_image(face_image, duration=200)
    
cozmo.run_program(cozmo_show_img)


# import asyncio
# import cozmo
# from cozmo.util import degrees, distance_mm, speed_mmps
# from PIL import Image

# async def move_forward_with_image(robot: cozmo.robot.Robot, distance: float, speed: float, image_path: str):
#     # Load the image and resize it
#     image = Image.open(image_path)
#     resized_image = image.resize(robot.oled_face.dimensions(), Image.BICUBIC)
    
#     # Convert the image to the format used by the OLED screen
#     face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
    
#     # Display the image while moving
#     robot.display_oled_face_image(face_image)
#     await robot.drive_straight(distance_mm(distance), speed_mmps(speed), should_play_anim=False).wait_for_completed()
    
#     # Turn off the screen after motion is complete
#     robot.display_oled_face_image(cozmo.oled_face.convert_image_to_screen_data(Image.new('1', (64, 128), 0)), duration_ms=0)

# async def cozmo_program(robot: cozmo.robot.Robot):
#     distance_to_move = 100  # Set the distance you want to move (in millimeters)
#     speed_to_move = 50  # Set the speed you want to move (in millimeters per second)
#     image_path = "path_to_your_image.png"  # Specify the path to the image you want to display
    
#     # Move forward with the specified image displayed on Cozmo's face screen
#     await move_forward_with_image(robot, distance_to_move, speed_to_move, image_path)

# cozmo.run_program(cozmo_program)
