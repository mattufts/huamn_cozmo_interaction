import os

blinking_path = "/home/tadashi_e/Documents/GithubRepos/huamn_cozmo_interaction/Pycozmo Scripts/AnimImages/Blinking"
try:
    print("Files in Blinking directory:", os.listdir(blinking_path))
except FileNotFoundError as e:
    print(f"Error: {e}")
