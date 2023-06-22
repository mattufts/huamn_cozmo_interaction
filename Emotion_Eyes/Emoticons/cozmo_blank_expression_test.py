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
    image_settings = [("happy-01.png", Image.BICUBIC),
                      ("low_battery-01.png", Image.NEAREST)]
    face_image = [ ]
    for image_name, resampling in image_settings:
        # Load the image and resize it
        image = Image.open(image_name)
        resized_image = image.resize(cozmo.oled_face.dimensions(), resampling)
        image = image.resize(cozmo.oled_face.dimensions(), resampling)
        face_image.append(cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True))
        face_image.append (face_image)
    
    num_loops = 10
    duration_s = 4.0
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