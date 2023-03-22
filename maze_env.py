import numpy as np
import numpy as np
maze = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
]
class MazeEnv:
    def __init__(self):
        self.maze = np.array(maze)  # 2D array representing the maze
        self.height, self.width = self.maze.shape
        self.start_pos = np.array([0, 0])  # starting position
        self.goal_pos = np.array([self.height - 1, self.width - 1])  # goal position
        self.current_pos = self.start_pos  # current position
        self.current_dir = np.array([0, 1])  # current direction (facing right)
        self.done = False  # episode termination flag
        self.battery = 100 # battery level, not sure how to use it right now 
    def reset(self):
        self.current_pos = self.start_pos
        self.current_dir = np.array([0, 1])  # facing right, maybe all directions should be relative
        self.done = False
        return self._get_state()
    def what_is_front(self):
        new_pos = self.current_pos + self.current_dir
        if not ((new_pos >= [0, 0]).all() and (new_pos < [self.height, self.width]).all()):
            return "out_of_bounds"
        if (self.current_pos == self.goal_pos).all():
            return "goal"
        if self.maze[tuple(new_pos)] == 0: 
            return "nothing"
        if self.maze[tuple(new_pos)] == 1: 
            return "wall"
        
    def step(self, action):
        # action is an integer: 0 = adjust up, 1 = adjust down, 2 = adjust left, 3 = adjust right, 4 = go forward
        reward = 0
        self.battery -= 10 # reduce battery level
        hit_wall = False
        if action == 0:  # adjust up
            self.current_dir = np.array([-1, 0])
        elif action == 1:  # adjust down
            self.current_dir = np.array([1, 0])
        elif action == 2:  # adjust left
            self.current_dir = np.array([0, -1])
        elif action == 3:  # adjust right
            self.current_dir = np.array([0, 1])
        elif action == 4:  # go forward
            new_pos = self.current_pos + self.current_dir
            if (new_pos >= [0, 0]).all() and (new_pos < [self.height, self.width]).all():  # within bounds
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
            raise ValueError("Invalid action!")
        
        return self._get_state(), reward, hit_wall, self.what_is_front(), self.done, {}
    
    def _get_state(self):
        return np.concatenate([self.current_pos, self.current_dir])



