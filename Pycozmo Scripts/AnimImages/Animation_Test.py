# import time
# import os
# from PIL import Image, ImageOps
# import pycozmo
# from pycozmo.anim_controller import AnimationController

# def display_resized_image(cli, image_path, duration):
#     target_size = (128, 32)

#     if os.path.exists(image_path):
#         image_open = Image.open(image_path)
#         image_resized = image_open.resize(target_size)
#         image_rgb = image_resized.convert('RGB')
#         image_inverted = ImageOps.invert(image_rgb)
#         img = image_inverted.convert('1')

#         cli.display_image(img)
#         time.sleep(duration)
#     else:
#         print(f"Image file not found: {image_path}")

# def display_images(cli, base_path, fps=20):
#     frame_duration = 1.0 / fps

#     image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])

#     while True:
#         for file_name in image_files:
#             image_path = os.path.join(base_path, file_name)
#             display_resized_image(cli, image_path, frame_duration)

# def main():
#     with pycozmo.connect() as cli:
#         cli.set_head_angle((pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0)
#         time.sleep(2)

#         anim_controller = AnimationController(cli)
#         anim_controller.enable_animations(False)

#         base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
#         display_images(cli, base_path)

# if __name__ == '__main__':
#     main()

# import time
# import os
# from PIL import Image, ImageOps
# import pycozmo

# def display_resized_image(cli, image_path, duration):
#     target_size = (128, 32)

#     if os.path.exists(image_path):
#         # Open, resize, and convert the image
#         image_open = Image.open(image_path)
#         image_resized = image_open.resize(target_size)
#         image_rgb = image_resized.convert('RGB')
#         image_inverted = ImageOps.invert(image_rgb)
#         img = image_inverted.convert('1')

#         # Display the image on Cozmo's screen for the specified duration
#         cli.display_image(img)
#         time.sleep(0.01)
#     else:
#         print(f"Image file not found: {image_path}")

# def display_animation(cli, base_path, fps=20):
#     frame_duration = 1.0 / fps  # Duration of each frame in seconds

#     # List and sort all PNG files in the directory
#     image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])

#     # Continuously cycle through the images to create an animation
#     while True:
#         for file_name in image_files:
#             image_path = os.path.join(base_path, file_name)
#             display_resized_image(cli, image_path, frame_duration)

# def main():
#     with pycozmo.connect() as cli:
#         cli.set_head_angle((pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0)
#         time.sleep(2)

#         base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
#         display_animation(cli, base_path)

# if __name__ == '__main__':
#     main()

# #working animation script verison 1
# import time
# import os
# from PIL import Image, ImageOps
# import pycozmo
# from pycozmo.anim_controller import AnimationController

# def preload_images(base_path):
#     images = []
#     image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])
#     for file_name in image_files:
#         image_path = os.path.join(base_path, file_name)
#         if os.path.exists(image_path):
#             image_open = Image.open(image_path)
#             image_resized = image_open.resize((128, 32))
#             image_rgb = image_resized.convert('RGB')
#             image_inverted = ImageOps.invert(image_rgb)
#             img = image_inverted.convert('1')
#             images.append(img)
#         else:
#             print(f"Image file not found: {image_path}")
#     return images
# def display_animation(cli, images, desired_fps=24, reset_fps=45):
#     desired_frame_duration = 1.0 / desired_fps
#     reset_frame_duration = 1.0 / reset_fps
#     slowdown_interval = 20  # Number of frames to display rapidly before slowing down

#     counter = 0
#     while True:
#         for img in images:
#             cli.display_image(img)
#             if counter < slowdown_interval:
#                 time.sleep(reset_frame_duration)  # Fast frame rate
#             else:
#                 time.sleep(desired_frame_duration)  # Slow down intermittently
#             counter = (counter + 1) % (slowdown_interval + 5)  # Reset counter periodically


# def main():
#     with pycozmo.connect() as cli:
#         cli.set_head_angle((pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0)
#         time.sleep(2)

#         base_path = "/Users/matt/Documents/GitHub/human_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
#         images = preload_images(base_path)
#         display_animation(cli, images)
        
# if __name__ == '__main__':
#     main()


#Working animation script verison 2
import os
import time
from PIL import Image, ImageOps
import pycozmo
from pycozmo.anim_controller import AnimationController

def preload_images(base_path):
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
            
            # If the resized image height is greater than 32, crop it to fit
            if new_height > 32:
                top = (new_height - 32) // 2
                bottom = top + 32
                image_resized = image_resized.crop((0, top, 128, bottom))
            else:
                # If the resized height is less than or equal to 32, add padding
                image_resized = ImageOps.pad(image_resized, (128, 32), color=(0, 0, 0))

            image_rgb = image_resized.convert('RGB')
            image_inverted = ImageOps.invert(image_rgb)
            img = image_inverted.convert('1')
            images.append(img)
        else:
            print(f"Image file not found: {image_path}")
    return images

def display_animation(cli, anim_controller, images, fps=40):  # Ensure this is defined before calling in main()
    frame_duration = 1.0 / fps
    while True:
        for img in images:
            cli.display_image(img)
            time.sleep(frame_duration)
            anim_controller.enable_animations(False)  # Frequent resets to assert control


# def preload_images(base_path):
#     images = []
#     image_files = sorted([f for f in os.listdir(base_path) if f.endswith('.png')])
#     for file_name in image_files:
#         image_path = os.path.join(base_path, file_name)
#         if os.path.exists(image_path):
#             image_open = Image.open(image_path)
#             #image_resized = image_open.resize((128, 32))
#             image_rgb = image_open.convert('RGB')
#             image_inverted = ImageOps.invert(image_rgb)
#             img = image_inverted.convert('1')
#             images.append(img)
#         else:
#             print(f"Image file not found: {image_path}")
#     return images

# def display_animation(cli, anim_controller, images, fps=40): #FPS is set intentionally high for animation blending
#     frame_duration = 1.0 / fps
#     while True:
#         for img in images:
#             cli.display_image(img)
#             time.sleep(frame_duration)
#             anim_controller.enable_animations(False)  # Frequent resets to assert control
def main():
    with pycozmo.connect() as cli:
        cli.set_head_angle((pycozmo.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0)
        time.sleep(2)

        anim_controller = AnimationController(cli)
        anim_controller.enable_animations(False)

        base_path = '/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/AnimImages/icon_stop'
        images = preload_images(base_path)
        display_animation(cli, anim_controller, images)

if __name__ == '__main__':
    main()
