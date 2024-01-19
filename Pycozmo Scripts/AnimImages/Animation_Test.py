import time
import os
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController

def display_images(cli, base_path, num_images=14, fps=20):
    frame_duration = 2.0 / fps  # Duration of each frame in seconds

    # Display each image in sequence
    for i in range(1, num_images + 1):
        image_path = os.path.join(base_path, f"PNG_{i:04d}.png")
        display_resized_image(cli, image_path, frame_duration)

    # Repeat the last two images for an extra 4 seconds
    extra_time = 4.0
    repeat_frames = int(extra_time / frame_duration)
    for _ in range(repeat_frames):
        for i in range(13, 15):
            image_path = os.path.join(base_path, f"PNG_{i:04d}.png")
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
        base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Angry"  # Update with the path to your images
        display_images(cli, base_path)

if __name__ == '__main__':
    main()