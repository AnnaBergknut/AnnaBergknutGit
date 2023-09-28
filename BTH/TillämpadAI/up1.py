# def create_maze(width, height):
#     maze = [['|' if i == 0 or i == width - 1 or j == 0 or j == height - 1 else ' ' for i in range(width)] for j in range(height)]
    
#     # Example: Removing a wall between cell (1, 1) and cell (1, 2)
#     maze[1][1] = ' '
#     maze[1][2] = ' '
    
#     return maze

# def display_maze(maze):
#     for row in maze:
#         print("".join(row))

# def main():
#     maze_width = 20
#     maze_height = 7
#     maze = create_maze(maze_width, maze_height)

#     display_maze(maze)

# if __name__ == "__main__":
#     main()

#--------------------------------------------------------------------------------

# import random

# # Maze dimensions (odd values for simplicity)
# maze_width = 21
# maze_height = 7

# # Create a maze grid with cells
# def create_maze(width, height):
#     maze = [['#'] * width for _ in range(height)]
#     return maze

# # Display the maze
# def display_maze(maze):
#     for row in maze:
#         print("".join(row))

# # Generate a maze using randomized Prim's algorithm
# def generate_maze(maze):
#     # Initialize with walls
#     for row in range(1, len(maze) - 1, 2):
#         for col in range(1, len(maze[0]) - 1, 2):
#             maze[row][col] = ' '

#     # Initialize the frontier
#     frontier = [(i, j) for i in range(1, len(maze) - 1, 2) for j in range(1, len(maze[0]) - 1, 2)]
#     random.shuffle(frontier)

#     # While there are frontier cells
#     while frontier:
#         cell = frontier.pop()
#         row, col = cell
#         maze[row][col] = ' '

#         # Randomly choose a neighboring wall cell
#         neighbors = []

#         if row - 2 >= 0:
#             neighbors.append((row - 2, col))
#         if row + 2 < len(maze):
#             neighbors.append((row + 2, col))
#         if col - 2 >= 0:
#             neighbors.append((row, col - 2))
#         if col + 2 < len(maze[0]):
#             neighbors.append((row, col + 2))

#         random.shuffle(neighbors)

#         for neighbor in neighbors:
#             n_row, n_col = neighbor
#             if maze[n_row][n_col] == ' ':
#                 continue

#             wall_row = (row + n_row) // 2
#             wall_col = (col + n_col) // 2

#             maze[wall_row][wall_col] = ' '
#             frontier.append(cell)
#             break

# def main():
#     maze = create_maze(maze_width, maze_height)
#     generate_maze(maze)

#     display_maze(maze)

# if __name__ == "__main__":
#     main()
 
# ------------------------------------------------------------------------------
 
# 



def create_maze(width, height):
    maze = [['|' if i % 2 == 0 or j % 2 == 0 else ' ' for i in range(width)] for j in range(height)]

    # Remove the wall between cell (1, 1) and cell (1, 2)
    maze[1][1] = ' '
    maze[1][2] = ' '

    return maze

def display_maze(maze):
    for row in maze:
        print("".join(row))

def main():
    maze_width = 20
    maze_height = 7
    maze = create_maze(maze_width, maze_height)

    display_maze(maze)

if __name__ == "__main__":
    main()