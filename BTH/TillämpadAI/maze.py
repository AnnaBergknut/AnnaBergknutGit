from collections import deque

def visualize_maze(maze):
    for row in maze:
        row_str = ""
        for cell in row:
            if cell == 0:
                row_str += '█'  # Wall █
            elif cell == 2:
                row_str += 'o'  # Start
            elif cell == 3:
                row_str += 'x'  # End
            elif cell == 4:
                row_str += '.'  # visited
            else:
                row_str += ' '  # Empty cell
        print(row_str)   

def bfs(maze, start, end, moves):
    # Create a queue for BFS
    queue = deque([(start[0], start[1])])
    path = {}  # Dictionary to store the path
    # Get maze dimensions
    num_rows = 15
    num_cols = 41
    visited = [[False] * num_cols for _ in range(num_rows)]

    while queue:
        row, col = queue.popleft()
        visited[row][col] = True

        # Check if we reached the goal (end)
        if (row, col) == end:
            print(path)
            return reconstruct_path(path, start, end)

        # Explore adjacent cells
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc               # Move two steps in the given direction
            mid_row, mid_col = row + dr // 2, col + dc // 2     # Calculate the position of the cell in between

            # Check if the new cell is not visited and if the mid call is not 0 to stop it from jumping walls
            if maze[mid_row][mid_col] != 0 and not visited[new_row][new_col]:
                queue.append((new_row, new_col))
                # visited[new_row][new_col] = True
                maze[new_row][new_col] = 4  # Mark the cell as visited
                path[(new_row, new_col)] = (row, col)  # Store the path

def dfs(maze, start, end, moves):
    # Create a stack for DFS
    stack = [(start[0], start[1])]
    path = {}  # Dictionary to store the path
    # Get maze dimensions
    num_rows = 15
    num_cols = 41
    visited = [[False] * num_cols for _ in range(num_rows)]
    
    while stack:
        row, col = stack.pop()
        visited[row][col] = True
        
        # Check if we reached the goal (end)
        if (row, col) == end:
            print(path)
            return reconstruct_path(path, start, end)

        # Explore adjacent cells
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc               # Move two steps in the given direction
            mid_row, mid_col = row + dr // 2, col + dc // 2     # Calculate the position of the cell in between

            # Check if the new cell is not visited and if the mid call is not 0 to stop it from jumping walls
            if maze[mid_row][mid_col] != 0 and not visited[new_row][new_col]:
                stack.append((new_row, new_col))
                # visited[new_row][new_col] = True
                maze[new_row][new_col] = 4  # Mark the cell as visited
                path[(new_row, new_col)] = (row, col)  # Store the path

def reconstruct_path(path, start, end):
    current = end
    path_list = []

    while current != start:
        path_list.append(current)
        current = path[current]

    path_list.append(start)
    path_list.reverse()
    return path_list

def resetMaze():
    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,2,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0],
            [0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0],
            [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0],
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0],
            [0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0],
            [0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0],
            [0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0],
            [0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,3,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    return maze

def main():
    maze = resetMaze()
    visualize_maze(maze)
    
    # Define possible moves (down, up, right, left)
    moves = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    start_pos = (1, 1)
    end_pos = (13, 37)

    while True:
        algorithm = input("\nEnter input (bfs, dfs or exit): ").strip().lower()
        if algorithm == "bfs":
            print("\nFinding a path using BFS:")
            bfs_path = bfs(maze, start_pos, end_pos, moves)
            visualize_maze(maze)
            print("BFS Path:", bfs_path)
            maze = resetMaze()
        elif algorithm == "dfs":
            print("\nFinding a path using DFS:")
            dfs_path = dfs(maze, start_pos, end_pos, moves)
            visualize_maze(maze)
            print("DFS Path:", dfs_path)
            maze = resetMaze()
        elif algorithm == "exit":
            return False
        else:
            print("Invalid input. Please enter bfs, dfs or exit.")

if __name__ == "__main__":
    main()