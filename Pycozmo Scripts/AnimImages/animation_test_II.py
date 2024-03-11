import time
import os
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController

def display_resized_image(cli, image_path):
    target_size = (128, 32)

    if os.path.exists(image_path):
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        cli.display_image(img)
        time.sleep(0.01) #the time here dictates whether cozmo's face will blend into other animations
    else:
        print(f"Image file not found: {image_path}")

def display_images(cli, base_path, fps=12):
    #frame_duration = 1.0 / fps

    image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])

    while True:
        for file_name in image_files:
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path)

def main():
    with pycozmo.connect() as cli:
        anim_controller = AnimationController(cli)
        anim_controller.enable_animations(True)
        cli.set_head_angle((pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0)
        time.sleep(2)
     
        #base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Sad"

        #base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Left"
        base_path = '/home/matt_e/huamn_cozmo_interaction/Pycozmo Scripts/AnimImages/Sad'
        display_images(cli, base_path)


if __name__ == '__main__':
    main()
