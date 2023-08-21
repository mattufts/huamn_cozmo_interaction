
import sys
import time

try: 
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps


# def cozmo_program(robot: cozmo.robot.Robot):
#     # Drive forwards for 150 millimeters at 50 millimeters-per-second.
#     robot.drive_straight(distance_mm(10000), speed_mmps(50)).wait_for_completed()
# async def cozmo_show_img(robot: cozmo.robot.Robot):
#     # Use a blank image
#     image_settings = [("blank.png", Image.BICUBIC),
#                       ("blank.png", Image.NEAREST)]
#     face_image = [ ]
#     for image_name, resampling in image_settings:
#         # Load the image and resize it
#         image = Image.open(image_name)
#         resized_image = image.resize(cozmo.oled_face.dimensions(), resampling)
#         image = image.resize(cozmo.oled_face.dimensions(), resampling)
#         face_image.append(cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True))
#         face_image.append (face_image)
    
#     num_loops = 10
#     duration_s = 1000
#     # Load the image and resize it
#     print("Press CTRL-C to quit (or wait %s seconds to complete)" % int(num_loops*duration_s) )
    
#     for _ in range(num_loops):
#         for image in face_image:
#             robot.display_oled_face_image(image, duration_s * 1000.0)
#             time.sleep(duration_s)

async def cozmo_program(robot: cozmo.robot.Robot):
    # Create an image using PIL
    # img = Image.new('L', (128, 64), 'white')
    # draw = ImageDraw.Draw(img)
    # draw.line((0, 0) + img.size, fill=0)
    # draw.line((0, img.size[1], img.size[0], 0), fill=0)
    # # Convert the image to Cozmo's format
    # cozmo_oled_image = cozmo.oled_face.convert_image_to_screen_data(img)
    # Display the image on Cozmo's face
    image = Image.open("blank.png")
    resized_image = image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
    image = (cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True))
    #face_image.append(cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True))
    
    await robot.drive_straight(cozmo.util.distance_mm(200), cozmo.util.speed_mmps(50)).wait_for_completed()
    await robot.display_oled_face_image(image, 1000.0, in_parallel=True) 
    time.sleep(1)
    #robot.display_oled_face_image(cozmo_oled_image, 1000.0)
    # Move Cozmo forward while displaying the image
    
cozmo.run_program(cozmo_program)

