#This script is imported by PycozmoFSM_Animation (for upper use with the MainDemo_Animation program)
#The program defines how the robot is able to handle displaying animation 

#Run Animation Repeatedly
import time
import os
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the AnimImages directory
base_path = os.path.join(script_dir, "AnimImages", "icon_default")


def display_blink_eyes(cli, base_path=None, fps=24, duration=1):
    if base_path is None:
        base_path = os.path.join(script_dir, "AnimImages", "icon_default")
    frame_duration = 1.0 / fps  # Duration of each frame in seconds 
    total_loops = 1 
    # List and count PNG files in the directory
    image_files = [f for f in os.listdir(base_path) if f.endswith('.png')]
    num_images = len(image_files)
    
    # Display each image in sequence
    for _ in range(total_loops):
        for file_name in sorted(image_files):
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)


def display_images(cli, base_path, fps=30, repeat_duration=3):
    frame_duration = 1.0 / fps  # Duration of each frame in seconds

    # List and count PNG files in the directory
    image_files = [f for f in os.listdir(base_path) if f.endswith('.png')]
    num_images = len(image_files)
    
    #calculate total loops needed based on repeat_duration
    #total_frames = repeat_duration * fps
    total_loops = 1
    
    # Display each image in sequence
    for _ in range (total_loops):
        for file_name in sorted(image_files):
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)

    # Repeat the last two images for an extra duration
    repeat_frames = 1
    last_two_images = sorted(image_files)[-2:]  # Get last two images
    for _ in range(repeat_frames):
        for file_name in last_two_images:
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)

def display_resized_image(cli, image_path, duration = 1):
    target_size = (128, 32)

    if os.path.exists(image_path):
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        cli.display_image(img)
        #time.sleep(duration)
    else:
        print(f"Image file not found: {image_path}")

# Call_Animation.py
def execute_interaction_animation(cli, interaction_type):
    animation_paths = {
        "up": "icon_up",  # directional animations
        "left": "icon_left",
        "right": "icon_right",

        "sad": "icon_injured",  # reactionary animations
        "crash": "icon_stopped",
        "finished": "icon_finished",

        "happy": "icon_checkmark",  # alignment animations

        "neutral": "icon_default"  # default animation
    }

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construct the path to the AnimImages directory
    base_path = os.path.join(script_dir, "AnimImages")
    
    # Determine the full path for the specified interaction type
    animation_folder = animation_paths.get(interaction_type, "icon_default")
    full_path = os.path.join(base_path, animation_folder)
    
    if os.path.exists(full_path):
        # Call the function that handles the display of images
        display_images(cli, full_path, repeat_duration=4)
    else:
        print(f"Animation path does not exist: {full_path}")

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle)
        time.sleep(2)
        anim_controller = AnimationController(cli)
        anim_controller.enable_animations(False)
        
        # Use the absolute path here
        base_path = os.path.join(script_dir, "AnimImages", "icon_default")
        display_images(cli, base_path, fps=30, repeat_duration=3)

if __name__ == '__main__':
    main()



