import numpy as np
from Prisoner import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # Initialize a 2D array of random colors (Red: 0, Blue:1)
        self.grid = np.random.randint(low=0, high=2, size=(self.height, self.width))
        # use this to correspond the ints with an actual policy
        
        
    def update(self, success_array):
        # Flatten the success array for easier manipulation
        success_array = np.array(success_array).flatten()
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                # Current color of the square
                current_color = self.grid[row, col]  # fix 1: using tuple to access array element
 
                # Get neighbors and their indices
                neighbors, neighbor_indices = self.get_neighbors(row, col)

                # Find the indices of the most successful neighbors
                most_success_indices = np.where(success_array[neighbor_indices] == success_array[neighbor_indices].max())[0]
                most_success_colors = self.grid[neighbor_indices[most_success_indices] // self.width,
                                      neighbor_indices[most_success_indices] % self.width]
  
                opposite_colors = most_success_colors != current_color
                 
                if np.count_nonzero(opposite_colors) == 1:
                    # Change color if there is exactly one opposite color and no tie
                    self.grid[row, col] = most_success_colors[np.argwhere(opposite_colors)][0]

    def get_neighbors(self, row, col):  # fix 2: corrected neighbor indices calculation
        neighbors = []
        neighbor_indices = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                r = row + dx  
                c = col + dy
                if 0 <= r < self.height and 0 <= c < self.width: 
                    if dx != 0 or dy != 0:       
                        neighbors.append(self.grid[r][c])
                        neighbor_indices.append(r * self.width + c)                   
        return np.array(neighbors), np.array(neighbor_indices)          

    def get_random_success_array(self):
        return np.random.randint(low=0, high=100, size=(self.height, self.width)).flatten()
    
    def get_prisonors_success_array(self):
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                # Current color of the square
                current_color = self.grid[row, col]  # fix 1: using tuple to access array element
    
    def preRound(self):
        for row in range(self.height):
            for col in range(self.width):
                current_color = self.grid[row, col]
                

    def plot(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self.grid, cmap='RdBu')
        ax.set_xticks(np.arange(self.width))
        ax.set_yticks(np.arange(self.height))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.colorbar(im)
        return im

    
def run_evolution(field, num_iterations):
    success_array = field.get_random_success_array() 
    im = field.plot()
    plt.title("Iteration: 0")
    for i in range(num_iterations):
        field.update(success_array)
        success_array = field.get_random_success_array()  # Replace with actual success calculation
        im.set_array(field.grid)
        plt.title(f"Iteration: {i+1}")
        plt.pause(0.5)
    
#Set the height and width of the grid
height = 10 
width = 10
num_iterations = 20
#Create an instance of the field
field = Field(height, width)
run_evolution(field, num_iterations)
plt.show()