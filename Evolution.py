import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from Prisoner import *

class Field:
    def __init__(self, height, width, p, policies):
        self.height = height
        self.width = width
        self.policies = policies
        # Initialize a 2D array of random colors (Red: 0, Blue:1)
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), p=p)
        # use this to correspond the ints with an actual policy

        self.population = [None]*(width*height)

        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col

                self.population[index] = policies[self.grid[row][col]]
        
    def pre_round(self):
        for i, thing in enumerate(self.population):
            if(thing == Master.name and random.uniform(0, 1) < 0.7):
                self.population[i] = Slave.name
            elif(thing == Helper.name and random.uniform(0, 1) < 0.5):
                self.population[i] = Reciever.name
            elif(thing == Reciever.name and random.uniform(0, 1) < 0.5):
                self.population[i] = Helper.name
            
        
        print(self.population)
        
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
                current_colors = most_success_colors == current_color
                 
                if np.count_nonzero(current_colors) == 0:
                    # Change color if there is at least one opposite color highest value
                    self.grid[row, col] = most_success_colors[np.argwhere(opposite_colors)][0]
                
                self.population[index] = self.policies[self.grid[row][col]]

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
    

    def zero_wins(self):
        flattened = self.grid.flatten()

        for i, item in enumerate(flattened):
            if item == 0:
                flattened[i] = 1
            else:
                flattened[i] = 0
            
        
        return flattened
    
    def prisoners_game(self):
        flattened = self.grid.flatten()

        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col

                neighbors, neighbor_indices = self.get_neighbors(row, col)
                cur = self.population[index]
                score = 0

                for neighbour in neighbor_indices:
                    score += score_matrix[(cur, self.population[neighbour])]
                
                flattened[index] = score / len(neighbors)
        
        return flattened
    
    def get_prisonors_success_array(self):
        for row in range(self.height):
            for col in range(self.width):
                index = row * self.width + col
                # Current color of the square
                current_color = self.grid[row, col]  # fix 1: using tuple to access array element
    

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
    im = field.plot()
    plt.title("Iteration: 0")
    for i in range(num_iterations):
        field.pre_round()
        dummy = field.get_random_success_array()
        success_array = field.prisoners_game() 
        field.update(success_array)
        im.set_array(field.grid)
        plt.title(f"Iteration: {i+1}")
        plt.pause(0.5)

        first = field.grid[0][0]
        count = sum(sum(field.grid == first))
        if count == field.grid.flatten().size:
            break


score_matrix = {
    ('Master', 'Master'): 296,
    ('Master', 'Slave'): 477,
    ('Master', 'Helper'): 106,
    ('Master', 'Reciever'): 111,
    ('Master', 'Tit-For-Tat'): 106,
    ('Master', 'Always Defect'): 99,
    ('Slave', 'Master'): 17,
    ('Slave', 'Slave'): 200,
    ('Slave', 'Helper'): 106,
    ('Slave', 'Reciever'): 111,
    ('Slave', 'Tit-For-Tat'): 106,
    ('Slave', 'Always Defect'): 99,
    ('Helper', 'Master'): 101,
    ('Helper', 'Slave'): 101,
    ('Helper', 'Helper'): 300,
    ('Helper', 'Reciever'): 6,
    ('Helper', 'Tit-For-Tat'): 300,
    ('Helper', 'Always Defect'): 98,
    ('Reciever', 'Master'): 101,
    ('Reciever', 'Slave'): 101,
    ('Reciever', 'Helper'): 496,
    ('Reciever', 'Reciever'): 298,
    ('Reciever', 'Tit-For-Tat'): 299,
    ('Reciever', 'Always Defect'): 98,
    ('Tit-For-Tat', 'Master'): 101,
    ('Tit-For-Tat', 'Slave'): 101,
    ('Tit-For-Tat', 'Helper'): 300,
    ('Tit-For-Tat', 'Reciever'): 299,
    ('Tit-For-Tat', 'Tit-For-Tat'): 300,
    ('Tit-For-Tat', 'Always Defect'): 99,
    ('Always Defect', 'Master'): 104,
    ('Always Defect', 'Slave'): 104,
    ('Always Defect', 'Helper'): 108,
    ('Always Defect', 'Reciever'): 108,
    ('Always Defect', 'Tit-For-Tat'): 104,
    ('Always Defect', 'Always Defect'): 100
}
#Set the height and width of the grid
height = 100
width = 100
num_iterations = 100

# which index is what policy
policies = [Helper.name, Master.name]

#Create an instance of the field
field = Field(height, width, [0.5, 0.5], policies)
run_evolution(field, num_iterations)
plt.show()