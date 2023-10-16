import random
import math
import numpy as np

def create_individual(length):
    for i in range(length):
        return [random.choice(['up', 'down', 'left', 'right'])]

def evaluate_fitness(individual, maze, start, end):
    row, col = start
    visited_positions = set()  # Create a set to track visited positions
    fitness = 0.0  # Initialize fitness score

    for action in individual:
        # Calculate the next position based on the action
        if action == 'up':
            wall_row, wall_col = row - 1, col
            if maze[wall_row][wall_col] != 0:
                new_row, new_col = row - 2, col
        elif action == 'down':
            wall_row, wall_col = row + 1, col
            if maze[wall_row][wall_col] != 0:
                new_row, new_col = row + 2, col
        elif action == 'left':
            wall_row, wall_col = row, col - 1
            if maze[wall_row][wall_col] != 0:
                new_row, new_col = row, col - 2
        elif action == 'right':
            wall_row, wall_col = row, col + 1
            if maze[wall_row][wall_col] != 0:
                new_row, new_col = row, col + 2

        # Check if the next position is a wall
        if maze[wall_row][wall_col] == 0:
            fitness -= 0.5  # Penalize for hitting a wall
        else:
            # Check if the position is already visited
            if (new_row, new_col) in visited_positions:
                fitness -= 0.1  # Penalize for revisiting a position

            # Update the visited positions
            visited_positions.add((new_row, new_col))

            # Update the current position
            row, col = new_row, new_col

        # Check if the individual has reached the end
        if (row, col) == end:
            fitness += 10.0  # Reward maximum fitness when the end is reached
            
    return fitness

def genetic_algorithm(maze, start, end, individual_length, population_size, num_generations, mutation_rate):
    for i in range(population_size):
        population = [create_individual(individual_length)]

    for generation in range(num_generations):
        # Evaluate the fitness of each individual
        fitness_scores = []
        for ind in population:
            fitness_score = [evaluate_fitness(ind, maze, start, end)]
            fitness_scores.append(fitness_score)

        # Print the best fitness score achieved in this generation
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}/{num_generations}, Best Fitness: {best_fitness}")
        
        # Find the best individual in this generation
        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]

        # Print the moves of the best individual for this generation
        print(f"Generation {generation}, Best Fitness: {best_fitness}, Best Individual's Moves:\n {best_individual}")

        # Select individuals to create the next generation
        selected_population = []

        for i in range(population_size):
            tournament_size = 5
            tournament = random.sample(range(population_size), tournament_size)
            winner = tournament[0]
            for competitor in tournament[1:]:
                if fitness_scores[competitor] > fitness_scores[winner]:
                    winner = competitor
            selected_population.append(population[winner])

        # Apply crossover and mutation to create the next generation
        new_population = []

        for i in range(population_size):
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            crossover_point = random.randint(1, individual_length - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            for i in range(individual_length):
                if random.random() < mutation_rate:
                    child[i] = random.choice(['up', 'down', 'left', 'right'])
            new_population.append(child)

        population = new_population

        # Check if a solution has been found
        best_individual_index = fitness_scores.index(max(fitness_scores))
        if fitness_scores[best_individual_index] > 0:
            print("Solution found in generation", generation)
            return population[best_individual_index]

    print("No solution found.")
    return None  # If no solution is found
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

    start_pos = (1, 1)
    end_pos = (13, 37)

    population_size = 100
    num_generations = 5000
    mutation_rate = 0.3
    individual_length = 100  # Define the length of each individual's sequence of actions

    best_solution = genetic_algorithm(maze, start_pos, end_pos, individual_length, population_size, num_generations, mutation_rate)

    if best_solution:
        print("Genetic Algorithm Path:", best_solution)
        maze = resetMaze()
        visualize_maze(maze)
        row, col = start_pos
        maze[row][col] = 2  # Mark the start
        for action in best_solution:
            if action == 'up':
                row -= 2
                maze[row][col] = 4  # Mark the path
            elif action == 'down':
                row += 2
                maze[row][col] = 4  # Mark the path
            elif action == 'left':
                col -= 2
                maze[row][col] = 4  # Mark the path
            elif action == 'right':
                col += 2
                maze[row][col] = 4  # Mark the path    
        maze[end_pos[0]][end_pos[1]] = 3  # Mark the end
        visualize_maze(maze)
    else:
        print("No path found using the Genetic Algorithm")

if __name__ == "__main__":
    main()
    
""" 33 steg """