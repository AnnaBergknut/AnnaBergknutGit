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
                row_str += '.'  # Visited
            else:
                row_str += ' '  # Empty cell
        print(row_str)

def backtrack_bfs(maze, start, end):
    # Create a queue for BFS
    queue = deque([(start[0], start[1], [])])

    while queue:
        row, col, path = queue.popleft()
        
        # Check if we reached the goal (end)
        if (row, col) == end:
            return path + [(row, col)]

        # Explore adjacent cells
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            new_row, new_col = row + dr, col + dc
            mid_row, mid_col = row + dr // 2, col + dc // 2

            # Check if the new cell is not visited and if the mid cell is not 0
            if maze[mid_row][mid_col] != 0 and maze[new_row][new_col] == 1:
                maze[new_row][new_col] = 4  # Mark the cell as visited
                new_path = path + [(row, col)]
                queue.append((new_row, new_col, new_path))

def backtrack_dfs(maze, start, end):
    # Create a stack for DFS
    stack = [(start[0], start[1], [])]

    while stack:
        row, col, path = stack.pop()
        
        # Check if we reached the goal (end)
        if (row, col) == end:
            return path + [(row, col)]

        # Explore adjacent cells
        for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            new_row, new_col = row + dr, col + dc
            mid_row, mid_col = row + dr // 2, col + dc // 2

            # Check if the new cell is not visited and if the mid cell is not 0
            if maze[mid_row][mid_col] != 0 and maze[new_row][new_col] == 1:
                maze[new_row][new_col] = 4  # Mark the cell as visited
                new_path = path + [(row, col)]
                stack.append((new_row, new_col, new_path))

def main():
    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

    # Get maze dimensions
    num_rows = len(maze)
    num_cols = len(maze[0])

    # Mark start and end positions
    start_pos = (1, 1)
    end_pos = (13, 37)

    maze[start_pos[0]][start_pos[1]] = 2
    maze[end_pos[0]][end_pos[1]] = 3

    visualize_maze(maze)

    while True:
        algorithm = input("\nEnter the algorithm to use (BFS or DFS): ").strip().lower()

        if algorithm == "bfs":
            print("\nFinding the shortest path using BFS:")
            bfs_path = backtrack_bfs(maze, start_pos, end_pos)
            visualize_maze(maze)
            print("BFS Path:", bfs_path)
            break
        elif algorithm == "dfs":
            print("\nFinding the shortest path using DFS:")
            dfs_path = backtrack_dfs(maze, start_pos, end_pos)
            visualize_maze(maze)
            print("DFS Path:", dfs_path)
            break
        else:
            print("Invalid input. Please enter 'BFS' or 'DFS'.")

if __name__ == "__main__":
    main()