#This is a copy of the Maze Environment Script
#DO NOT CHANGE THIS SCRIPT
#This creates a maze environment that can be used to test the Pycozmo Controller


import numpy as np
import numpy as np
import random

# maze should know everything including hazard and hazard should be 2
maze =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0],     #Challenge Maze 1
       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 2, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0], 
       [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
       [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
        ]

nav_maze=[
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  #vanilla maze, maze without environmental hazards.
       [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
       [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
        ]

# maze =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0],     #Challenge Maze 2
#        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#        [0, 1, 1, 2, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0], 
#        [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
#        [0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
#         ]
# # this is a maze exclude hazard
# nav_maze=[
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#        [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
#        [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
#         ]

# maze =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0],     #Challenge Maze 3
#        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#        [0, 1, 1, 2, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0], 
#        [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
#        [0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
#         ]
# # this is a maze exclude hazard
# nav_maze=[
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#        [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], 
#        [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
#        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
#         ]
# Define the maze dimensions
# def gen_maze():
#     global maze
#     width = 10
#     height = 10

#     # Define the maze as a 2D array of zeros
#     maze = [[0 for y in range(height)] for x in range(width)]

#     # Add walls to the maze
#     for x in range(width):
#         maze[x][0] = 1
#         maze[x][height-1] = 1
#     for y in range(height):
#         maze[0][y] = 1
#         maze[width-1][y] = 1

#     # Add random obstacles to the maze
#     for i in range(20):  # Add 20 obstacles
#         x = random.randint(1, width-2)  # Choose a random x-coordinate
#         y = random.randint(1, height-2)  # Choose a random y-coordinate
#         maze[x][y] = 1  # Place an obstacle at the chosen location

#     # Print the maze
#     for y in range(height):
#         for x in range(width):
#             print(maze[x][y], end="")
#         print()
class MazeEnv:
    def __init__(self):
        #gen_maze()
        self.maze = np.array(maze)  # 2D array representing the maze
        self.nav_maze = np.array(nav_maze)
        self.height, self.width = self.maze.shape
        self.start_pos = np.array([1, 1])  # starting position is at 1, 1 of the grid
        #self.goal_pos = np.array([self.height - 1, self.width - 1])  # goal position
        self.current_pos = self.start_pos  # current position
        self.current_dir = np.array([0, 1])  # current direction (facing right)
        self.goal_pos = np.array([4,12]) # end point
        self.done = False  # episode termination flag
        self.battery = 100 # battery level, not sure how to use it right now 
        self.health = 100
    def reset(self):
        self.current_pos = self.start_pos
        self.current_dir = np.array([0, 1])  # facing right, maybe all directions should be relative
        self.health = 100
        self.done = False
        return self._get_state()
    
    def what_is_front(self):
        new_pos = self.current_pos + self.current_dir
        if not ((new_pos >= [0, 0]).all() and (new_pos < [self.height, self.width]).all()):
            return "out_of_bounds"
        # if (self.current_pos == self.goal_pos).all():
        #     return "goal"
        if self.maze[tuple(new_pos)] == 0: 
            return "nothing"
        if self.maze[tuple(new_pos)] == 1: 
            return "wall"
        if self.maze[tuple(new_pos)] == 2: 
            return "fire"
        
    def step(self, action):
        # action is an integer: 0 = turn left, 1 = turn right, 2 = go forward
        reward = 0
        self.battery -= 10 # reduce battery level
        hit_wall = False
        if action == 0:  # t0rn left
            if (self.current_dir == np.array([0, 1])).all():
                self.current_dir = np.array([-1, 0])
            elif (self.current_dir == np.array([-1, 0])).all():
                self.current_dir = np.array([0, -1])
            elif (self.current_dir == np.array([0, -1])).all():
                self.current_dir = np.array([1, 0])
            else:  # current_dir == np.array([1, 0])
                self.current_dir = np.array([0, 1])
        elif action == 1:  # turn right
            if (self.current_dir == np.array([0, 1])).all():
                self.current_dir = np.array([1, 0])
            elif (self.current_dir == np.array([1, 0])).all():
                self.current_dir = np.array([0, -1])
            elif (self.current_dir == np.array([0, -1])).all():
                self.current_dir = np.array([-1, 0])
            else:  # current_dir == np.array([-1, 0])
                self.current_dir = np.array([0, 1])
        elif action == 2:  # go forward
            new_pos = self.current_pos + self.current_dir
            if (new_pos >= [1, 1]).all() and (new_pos < [self.height-1, self.width-1]).all():  # within bounds
                if self.maze[tuple(new_pos)] == 0:  # not a wall
                    self.current_pos = new_pos
                    if (self.current_pos == self.goal_pos).all():  # reached goal
                        reward = 1
                        self.done = True
                    else:
                        reward = 0
                else:  # hit a wall
                    reward = -1
                    hit_wall = True
            else:  # out of bounds
                reward = -1
                hit_wall = True
        else:
            print("stop being pressed")
        if self.health < 0:
            self.done = 'dead'
            print ("you have burned in the fire :(")

            
        return self._get_state(), reward, hit_wall, self.what_is_front(), self.done
    
    def _get_state(self):
        return np.concatenate([self.current_pos, self.current_dir])



