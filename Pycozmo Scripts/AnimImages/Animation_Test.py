import time
import os
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController

def display_resized_image(cli, image_path, duration):
    target_size = (128, 32)

    if os.path.exists(image_path):
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        # Display the image on Cozmo's screen for the specified duration
        cli.display_image(img)
        time.sleep(duration)
    else:
        print(f"Image file not found: {image_path}")

def display_images(cli, base_path, fps=20):
    frame_duration = 1.0 / fps  # Duration of each frame in seconds

    # List and sort all PNG files in the directory
    image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])

    while True:  # Loop to continuously cycle through the images
        # Display each image in sequence
        for file_name in image_files:
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)import time
                    anim_controller.enable_animations(False)    

        # Optionally, repeat the last two images for an extra duration
        extra_time = 4.0  # Total extra time to display the last two images
        if len(image_files) >= 2:
            repeat_frames = int(extra_time / frame_duration)
        for _ in range(repeat_frames):
            for i in range(-2, 0):
                image_path = os.path.join(base_path, image_files[i])
                display_resized_image(cli, image_path, frame_duration)

def display_resized_image(cli, image_path, duration):
    target_size = (128, 32)

    if os.path.exists(image_path):
        # Open, resize, and convert the image
        # Open, resize, and convert the imageßß
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        # Display the image on Cozmo's screen for the specified duration
        cli.display_image(img)
        time.sleep(duration)
    else:
        print(f"Image file not found: {image_path}")

# Example usage
def main():
    with pycozmo.connect() as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle)
        
        anim_controller = AnimationController(cli)
        anim_controller.enable_animations(False)
        
        base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"  # Update with the path to your images
        display_images(cli, base_path)
        while True:  # Infinite loop to continuously play the animation
            display_images(cli, base_path)
             # Periodically reaffirm control over animations if necessary
            anim_controller.enable_animations(False)

if __name__ == '__main__':
    main()