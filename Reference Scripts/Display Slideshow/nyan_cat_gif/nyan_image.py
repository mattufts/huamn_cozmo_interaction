#!/usr/bin/env python3


"""
    Display animation on Cozmo's face (oled screen)
"""


import sys
import time

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import cozmo


def get_in_position(robot: cozmo.robot.Robot):
    """If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face"""
    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel=True).wait_for_completed()


def cozmo_program(robot: cozmo.robot.Robot):
    get_in_position(robot)

    image_settings = []
    face_images = []

    for i in range(0, 7):
        if i < 10:
            num = '0000' + str(i)
        else:
            num = '000' + str(i)
        image_settings.append(('/Users/matt/Cozmo SDK/face_animation/nyan_cat_gif/nyan_' + num + '.png', Image.BICUBIC))

    for image_name, resampling_mode in image_settings:
        image = Image.open(image_name)

        resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)

        face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image)
        face_images.append(face_image)

    num_loops = 200
    duration_s = .04

    print("Press CTRL-C to quit (or wait %s seconds to complete)" % int(num_loops*duration_s*len(face_images)))

    for _ in range(num_loops):
        for i in range(0, len(face_images)):
            robot.display_oled_face_image(face_images[i], duration_s * 1000.0)
            time.sleep(duration_s)
        for i in reversed(range(0, len(face_images))):
            robot.display_oled_face_image(face_images[i], duration_s * 1000.0)
            time.sleep(duration_s)

cozmo.robot.Robot.drive_off_charger_on_connect = False

cozmo.run_program(cozmo_program)