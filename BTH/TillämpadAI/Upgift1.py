import matplotlib.pyplot as plt
import numpy as np
import random
from queue import Queue

def generate_maze(width, height):
    # Create a grid with walls
    maze = [['#'] * width for _ in range(height)]

    def recursive_backtracking(x, y):
        maze[y][x] = ' '  # Mark the current cell as open

        # Define the four possible directions to move (up, down, left, right)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx * 2, y + dy * 2

            # Check if the new cell is within bounds and unvisited
            if 0 <= new_x < width and 0 <= new_y < height and maze[new_y][new_x] == '#':
                maze[y + dy][x + dx] = ' '  # Remove the wall between the current and new cell
                recursive_backtracking(new_x, new_y)

    # Start generation from a random cell
    start_x, start_y = random.randrange(0, width, 2), random.randrange(0, height, 2)
    recursive_backtracking(start_x, start_y)

    return maze

def visualize_maze(maze):
    for row in maze:
        print(''.join(row))
    plt.imshow([[1 if cell == '#' else 0 for cell in row] for row in maze], cmap='gray')
    plt.xticks([])  # Remove x-axis ticks and labels
    plt.yticks([])  # Remove y-axis ticks and labels
    plt.show()

width, height = 20, 7  # Adjust the dimensions as needed
maze = generate_maze(width, height)
visualize_maze(maze)
    
def main():
    pass

if __name__ == "__main__":
    main()