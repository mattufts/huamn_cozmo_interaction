#This is a copy of the Maze Environment Script
#DO NOT CHANGE THIS SCRIPT
#This creates a maze environment that can be used to test the Pycozmo Controller

#Note: Check maze_env_ORIG.py for more information on the maze
#This is adapted for the actual study


import numpy as np

#maze should know everything including hazard and hazard should be 2
# # ############## Maze Option A ###################
# maze =      [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option A
#              [0, 0, 0, 0, 0, 0, 0, 1, 0],  # 1st row
#              [0, 1, 1, 2, 0, 1, 0, 0, 0],  # 2nd row
#              [0, 0, 0, 0, 0, 2, 1, 0, 0],  # 3rd row
#              [0, 0, 1, 0, 0, 2, 0, 0, 0],  # 4th row
#              [0, 0, 1, 1, 0, 0, 0, 1, 0],  # 5th row
#              [0, 0, 1, 0, 0, 0, 0, 0, 0],  # 6th row
#              [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#  ]       #  1, 2, 3, 4, 5, 6, 7  #     columns 

# nav_maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option A
#             [0, 0, 0, 0, 0, 0, 0, 1, 0],  # 1st row
#             [0, 1, 1, 0, 0, 1, 0, 0, 0],  # 2nd row
#             [0, 0, 0, 0, 0, 0, 1, 0, 0],  # 3rd row
#             [0, 0, 1, 0, 0, 0, 0, 0, 0],  # 4th row
#             [0, 0, 1, 1, 0, 0, 0, 1, 0],  # 5th row
#             [0, 0, 1, 0, 0, 0, 0, 0, 0],  # 6th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#   ]          #  1, 2, 3, 4, 5, 6, 7  #     columns 

# # # ################# Maze Option B ###################
maze =      [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option B, includes hazards
             [0, 1, 0, 0, 0, 0, 0, 0, 0],  # 1st row
             [0, 0, 0, 1, 0, 2, 1, 1, 0],  # 2nd row
             [0, 0, 1, 2, 0, 0, 0, 0, 0],  # 3rd row
             [0, 0, 0, 2, 0, 0, 1, 0, 0],  # 4th row
             [0, 1, 0, 0, 0, 1, 1, 0, 0],  # 5th row
             [0, 0, 0, 0, 0, 0, 1, 0, 0],  # 6th row
             [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
 ]            #  1, 2, 3, 4, 5, 6, 7  #     columns 


################# Maze Option B ###################
nav_maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option B
            [0, 1, 0, 0, 0, 0, 0, 0, 0],  # 1st row
            [0, 0, 0, 1, 0, 0, 1, 1, 0],  # 2nd row
            [0, 0, 1, 0, 0, 0, 0, 0, 0],  # 3rd row
            [0, 0, 0, 0, 0, 0, 1, 0, 0],  # 4th row
            [0, 1, 0, 0, 0, 1, 1, 0, 0],  # 5th row
            [0, 0, 0, 0, 0, 0, 1, 0, 0],  # 6th row   
            [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
 ]           #  1, 2, 3, 4, 5, 6, 7  #     columns 


################## Maze Template ###################
# maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option Template
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1st row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2nd row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3rd row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#  ]       #  1, 2, 3, 4, 5, 6, 7  8  #     columns 


# nav_maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Nav_Maze1, Template
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1st row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2nd row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3rd row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#  ]           #  1, 2, 3, 4, 5, 6, 7  #    columns

##################################################
class MazeEnv:
    def __init__(self):

        self.maze = np.array(maze)  # 2D array representing the maze
        self.nav_maze = np.array(nav_maze)
        self.height, self.width = self.maze.shape


# # # # # ################### Maze A start position ###################
#         self.start_pos = np.array([1,1])  # starting position is at 1, 1 of the grid   MAZE A
# ################### Maze A goal position ###################
#         self.current_dir = np.array([0, 1])  # current direction (facing right)
#         self.goal_pos = np.array([4,6]) # end point

# ################# Maze B start position ###################
        self.start_pos = np.array([1,7])  # starting position is at 1wwwwwwwwwwwwwd dddddddddddddddddddddddddd, 1 of the grid   MAZE B 
################## Maze B goal position ###################
        self.current_dir = np.array([0, -1])  # current direction (facing left)       
        self.goal_pos = np.array([4,2]) # end point

        self.done = False  # episode termination flag
        self.battery = 100 # battery level, not sure how to use it right now 
        self.health = 100
    def reset(self):
        self.current_pos = np.array(self.start_pos)  # starting position is at 1, 1 of the grid
        self.current_dir = np.array(self.current_dir)  # facing right, maybe all directions should be relative
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
        #print("hahahahahahhahahhahahahahhaha")
        reward = 0
        self.battery -= 10 # reduce battery level
        hit_wall = False
        if action == 0:  # turn left
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
                   # print("maze new pose:", self.maze[tuple(new_pos)])
                    self.current_pos = new_pos
                    print(f"Updated Position: {self.current_pos}")  # Debug: Print the updated position
                    if (self.current_pos == self.goal_pos).all():  # reached goal
                        reward = 1
                        #self.done = True
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


################## Maze Template ###################
# maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Maze Option Template
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1st row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2nd row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3rd row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6th row
#         [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#  ]          1, 2, 3, 4, 5, 6, 7   columns 


# nav_maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # Top border        Nav_Maze1, Template
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1st row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2nd row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3rd row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6th row
#             [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Bottom border
#  ]          1, 2, 3, 4, 5, 6, 7   columns

#Orientation of Robot
# 0, 1 = Facing Right
# 1, 0 = Facing Down
# 0, -1 = Facing Left
# -1, 0 = Facing Up