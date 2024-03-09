#This script is imported by PycozmoFSM_Animation (for upper use with the MainDemo_Animation program)
#The program defines how the robot is able to handle displaying animation 

#Run Animation Repeatedly
import time
import os
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController


def display_images(cli, base_path, fps=30, repeat_duration=3, extra_time=4):
    frame_duration = 1.0 / fps  # Duration of each frame in seconds

    # List and count PNG files in the directory
    image_files = [f for f in os.listdir(base_path) if f.endswith('.png')]
    num_images = len(image_files)
    
    #calculate total loops needed based on repeat_duration
    total_frames = repeat_duration * fps
    total_loops = int(total_frames / len(image_files))
    
    # Display each image in sequence
    for _ in range (total_loops):
        for file_name in sorted(image_files):
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)

    # Repeat the last two images for an extra duration
    repeat_frames = int(extra_time / frame_duration)
    last_two_images = sorted(image_files)[-2:]  # Get last two images
    for _ in range(repeat_frames):
        for file_name in last_two_images:
            image_path = os.path.join(base_path, file_name)
            display_resized_image(cli, image_path, frame_duration)

def display_resized_image(cli, image_path, duration):
    target_size = (128, 32)

    if os.path.exists(image_path):
        image_open = Image.open(image_path)
        image_resized = image_open.resize(target_size)
        image_rgb = image_resized.convert('RGB')
        image_inverted = ImageOps.invert(image_rgb)
        img = image_inverted.convert('1')

        cli.display_image(img)
        time.sleep(duration)
    else:
        print(f"Image file not found: {image_path}")

# Call_Animation.py
def execute_interaction_animation(cli, interaction_type):
    animation_paths = {
        "happy": "Happy",
        "sad": "Hurt",
        "angry": "Angry",
        "surprised": "Surprised",
        "neutral": "Blinking",
        "left": "Left",
        "right": "Right",
        "finished": "Successful"
    }
    # Get the relative base path for animations
    #base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/"
    base_path = "Pycozmo Scripts/AnimImages"
    
    # Determine the full path for the specified interaction type
    animation_folder = animation_paths.get(interaction_type, "Blinking")
    full_path = os.path.join(base_path, animation_folder)
    
    if full_path:
        # Call the function that handles the display of images
        display_images(cli, full_path, repeat_duration=4)

def main():
    with pycozmo.connect(enable_procedural_face=False) as cli:
        head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
        cli.set_head_angle(head_angle)
        time.sleep(2)
        anim_controller = AnimationController(cli)
        anim_controller.enable_animations(False)
        #base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"  # Update with the path to your images
        #base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"  # For use with iMac Pro
        base_path = "Pycozmo Scripts/AnimImages/Blinking"
        display_images(cli, base_path, fps=30, repeat_duration=3)

if __name__ == '__main__':
    main()



#Run animation once
# import time
# import os
# from PIL import Image, ImageOps
# import pycozmo
# from pycozmo.anim_controller import AnimationController

# def display_images(cli, base_path, num_images=14, fps=30, repeat_duration= 3):
#     frame_duration = 1.0 / fps  # Duration of each frame in seconds
#     num_loops = repeat_duration * fps
#     # Display each image in sequence
#     for i in range(1, num_images + 1):
#         image_path = os.path.join(base_path, f"PNG_{i:04d}.png")
#         display_resized_image(cli, image_path, frame_duration)

#     # Repeat the last two images for an extra 4 seconds
#     extra_time = 4.0
#     repeat_frames = int(extra_time / frame_duration)
#     for _ in range(repeat_frames):
#         for i in range(13, 15):
#             image_path = os.path.join(base_path, f"PNG_{i:04d}.png")
#             display_resized_image(cli, image_path, frame_duration)
            
# def display_resized_image(cli, image_path, duration):
#     target_size = (128, 32)

#     if os.path.exists(image_path):
#         # Open, resize, and convert the imageßß
#         image_open = Image.open(image_path)
#         image_resized = image_open.resize(target_size)
#         image_rgb = image_resized.convert('RGB')
#         image_inverted = ImageOps.invert(image_rgb)
#         img = image_inverted.convert('1')
        

#         # Display the image on Cozmo's screen for the specified duration
#         cli.display_image(img)
#         time.sleep(duration)
#     else:
#         print(f"Image file not found: {image_path}")

# # Example usage
# def main():
#     with pycozmo.connect(enable_procedural_face=False) as cli:
#         head_angle = (pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians)/2.0
#         cli.set_head_angle(head_angle)
#         time.sleep(2)
#         anim_controller = AnimationController(cli)
#         anim_controller.enable_animations(False)
#         base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Happy"  # Update with the path to your images
#         for _ in range(3):
#             display_images(cli, base_path, num_images=14, fps=30, repeat_duration=3)

# if __name__ == '__main__':
#     main()
