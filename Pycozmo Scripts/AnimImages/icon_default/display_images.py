import os
import time
from PIL import Image, ImageOps
import pycozmo

def display_images(cli, image_path, repeat_duration=1):
    """
    Function to display a sequence of images on Cozmo's face.

    Args:
        cli: Cozmo client instance used to communicate with the robot.
        image_path: Path to the directory containing the images to display.
        repeat_duration: Number of times the animation should repeat.
    """
    images = []

    # List all files in the directory
    image_files = sorted([f for f in os.listdir(image_path) if f.endswith(".png")])

    if not image_files:
        print(f"No image files found in directory: {image_path}")
        return

    # Preload images and convert them for Cozmo's display
    for file_name in image_files:
        img_path = os.path.join(image_path, file_name)
        img = Image.open(img_path)

        # Scale and crop or pad the image to fit Cozmo's screen
        scale_factor = 128 / img.width
        new_height = int(img.height * scale_factor)
        img = img.resize((128, new_height))
        if new_height > 32:
            top = (new_height - 32) // 2
            bottom = top + 32
            img = img.crop((0, top, 128, bottom))
        else:
            img = ImageOps.pad(img, (128, 32), color=(0, 0, 0))

        img = img.convert('RGB')
        img = ImageOps.invert(img)
        img = img.convert('1')
        images.append(img)

    # Display the images on Cozmo's face
    frame_duration = 1.0 / 40  # 40 FPS
    for _ in range(repeat_duration):
        for img in images:
            cli.display_image(img)
            time.sleep(frame_duration)

def preload_images(base_path):
    """
    Preload all images from a specified directory for quicker access during animation display.

    Args:
        base_path: The directory path where the images are stored.

    Returns:
        A list of preprocessed images ready for display on Cozmo's screen.
    """
    images = []
    image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])

    for file_name in image_files:
        image_path = os.path.join(base_path, file_name)
        if os.path.exists(image_path):
            image_open = Image.open(image_path)

            # Calculate the scaling factor to fit the image width
            scale_factor = 128 / image_open.width
            new_height = int(image_open.height * scale_factor)

            # Resize the image with the calculated scale factor
            image_resized = image_open.resize((128, new_height))

            # Crop or pad the image to fit Cozmo's display size
            if new_height > 32:
                top = (new_height - 32) // 2
                bottom = top + 32
                image_resized = image_resized.crop((0, top, 128, bottom))
            else:
                image_resized = ImageOps.pad(image_resized, (128, 32), color=(0, 0, 0))

            image_rgb = image_resized.convert('RGB')
            image_inverted = ImageOps.invert(image_rgb)
            img = image_inverted.convert('1')
            images.append(img)
        else:
            print(f"Image file not found: {image_path}")
    return images

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        # Set the initial head angle for Cozmo
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        cli.set_head_angle(head_angle)
        cli.wait_for_robot()

        # Example usage of display_images function
        image_path = "/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/AnimImages/icon_default"
        display_images(cli, image_path, repeat_duration=4)

if __name__ == "__main__":
    main()
