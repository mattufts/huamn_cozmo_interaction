import random
import queue
import maze_env
import keyboard
import threading



def find_shortest_path(maze, start, end):
    width, height = len(maze), len(maze[0])
    visited = [[False for _ in range(height)] for _ in range(width)]
    move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, left, down, up
    q = queue.Queue()
    q.put((start, [start]))  # (current position, path taken to reach here)
    while not q.empty():
        current_pos, path = q.get()
        x, y = current_pos
        if current_pos[0] == end[0] and current_pos[1] == end[1]:
            # Return the next move to make from the start
            return path[1] if len(path) > 1 else start

        for move in move_directions:
            next_x, next_y = x + move[0], y + move[1]

            if 0 < next_x < width and 0 < next_y < height and maze[next_x][next_y] == 0 and not visited[next_x][next_y]:
                visited[next_x][next_y] = True
                new_path = list(path)
                new_path.append((next_x, next_y))
                q.put(((next_x, next_y), new_path))

    return None  # Return None if no path is found
def determine_next_action(start_point, next_move, current_direction):
    if next_move is None:
        print("Warning: next_move is None. Defaulting to no movement.")
        return None  # or return some default action

    move_direction = (next_move[0] - start_point[0], next_move[1] - start_point[1])
    # Mapping from current direction to the next required action
    direction_to_action = {
        (0, 1): {"left": 0, "right": 1, "forward": 2},  # Facing right
        (1, 0): {"left": 1, "right": 0, "forward": 2},  # Facing down
        (0, -1): {"left": 1, "right": 0, "forward": 2}, # Facing left
        (-1, 0): {"left": 0, "right": 1, "forward": 2}, # Facing up
    }
    # 0 left 1 right, 2 forward
    # Calculate the required move direction to get to the next move
    move_direction = (next_move[0] - start_point[0], next_move[1] - start_point[1])
    
    # Determine the action based on the current direction and the move direction
    print(move_direction, current_direction)
    if move_direction == current_direction:
        return direction_to_action[tuple(current_direction)]["forward"]
    else:
        if current_direction == (0, 1) and move_direction == (1, 0):
            return 1
        if current_direction == (0, 1) and move_direction == (-1, 0):
            return 0
        
        if current_direction == (0, -1) and move_direction == (1, 0):
            return 0
        if current_direction == (0, -1) and move_direction == (-1, 0):
            return 1
        

        if current_direction == (1, 0) and move_direction == (0, 1):
            return 0
        if current_direction == (1, 0) and move_direction == (0, -1):
            return 1
        

        if current_direction == (-1, 0) and move_direction == (0, 1):
            return 1
        if current_direction == (-1, 0) and move_direction == (0, -1):
            return 0

        if random.choice([0, 1]):
            return 0
        else:
            return 1
    
def mark_forward(maze, current_position, current_direction, marker = 2):

    # Calculate the position directly in front
    forward_position = (current_position[0] + current_direction[0], current_position[1] + current_direction[1])
    
    # Check if the forward position is within the maze boundaries
    if 0 <= forward_position[0] < len(maze) and 0 <= forward_position[1] < len(maze[0]):
        # Mark the forward position as a wall
        if maze[forward_position[0]][forward_position[1]] == 1 and marker == 0:
            pass
        else:
            maze[forward_position[0]][forward_position[1]] = marker
    else:
        print("Forward position is outside the maze boundaries.")

def toggle_mode():
    global Mode
    if Mode == "Auto":
        Mode = "Manual"
    else:
        Mode = "Auto"
    print(f"Mode changed to {Mode}")

def listen_for_mode_toggle():
    keyboard.add_hotkey('s', toggle_mode)
    keyboard.wait()

# # Example usage:
# maze = maze_env.MazeEnv() # Generates the maze and stores it in the global 'maze' variable
# path_maze = maze .maze.copy()
# start_point = (3, 1)  # Assuming top-left corner is the start (not a wall)
# end_point = (8, 7)  # Assuming bottom-right corner is the goal (modify as needed)
# Mode = "Auto"
# listener_thread = threading.Thread(target=listen_for_mode_toggle, daemon=True)
# listener_thread.start()

# while True:
#     if Mode == "Auto":
#         print("Auto mode")
#     else:
#         print("Manual mode")
#     if Mode == "Auto":
#         next_move = find_shortest_path(path_maze, start_point, end_point)
#         print("Next move:", next_move)
#         action = determine_next_action(start_point, next_move, tuple(maze.current_dir))
#         print("Next action:", action)
#         mark_forward(path_maze, start_point, maze.current_dir)
#         print(path_maze)
#         import time
#         time.sleep(1
#         #smaze.step(action)
#     else:
#         print("Manual mode")
#         action = input("Enter action: ")
#         #maze.step(int(action))
#         break
