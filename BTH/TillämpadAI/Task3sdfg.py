import random

def create_individual(length):
    actions = ['up', 'down', 'left', 'right']
    individual = []
    for i in range(length):
        individual.append(random.choice(actions))
    return individual

def evaluate_fitness(individual, maze, start, end):
    row, col = start
    visited_positions = set()  # Create a set to track visited positions
    fitness = 0.0  # Initialize fitness score
    steps = 0

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
        
        steps == steps + 1
        
        # Check if the individual has reached the end
        if (row, col) == end:
            return fitness + 100, steps  # Reward maximum fitness when the end is reached

        # Check if the next position is a wall
        if maze[wall_row][wall_col] == 0:
            fitness -= 0.5  # Penalize for hitting a wall
        else:
            # Check if the position is already visited
            if (new_row, new_col) in visited_positions:
                fitness -= 0.2  # Penalize for revisiting a position
            else:
                fitness += 0.1 # Revarding finding a new position

            # Update the visited positions
            visited_positions.add((new_row, new_col))

            # Update the current position
            row, col = new_row, new_col
    steps = -1        
    return fitness, steps

def genetic_algorithm(maze, start, end, individual_length, population_size, num_generations, mutation_rate):
    population = []
    for i in range(population_size):
        population.append(create_individual(individual_length))
    
    found_end_index = -1

    for generation in range(num_generations):
        # Evaluate the fitness of each individual
        fitness_scores = []
        
        for ind in population:
            fitness_score, end_index = evaluate_fitness(ind, maze, start, end)
            fitness_scores.append(fitness_score)
            if end_index > 1:
                found_end_index = end_index
                print(found_end_index)
    
        # Find the best individual in this generation
        best_fitness = max(fitness_scores)
        best_individual_index = fitness_scores.index(max(fitness_scores))
        best_individual = population[best_individual_index]

        # Check if a solution has been found
        if fitness_scores[best_individual_index] > 0:
            best_individual = best_individual[:found_end_index +1]
            print(f"Solution found in generation {generation}, It's Fitness: {best_fitness}, How many moves: {len(best_individual)}, It's Individual's Moves:\n {best_individual}")
            return population[best_individual_index]
        else:
            # Print generation
            print(f"Generation {generation}/{num_generations}")
            # Print the moves of the best individual for this generation
            # print(f"Generation {generation}, Best Fitness: {best_fitness}, Best Individual's Moves:\n {best_individual}")

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
        row, col = start_pos

        for action in best_solution:
            new_row, new_col = row, col  # Initialize new_row and new_col

            # Check if there's a wall between the current position and the new position
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
            row, col = new_row, new_col
            maze[row][col] = 4  # Mark the path

        maze[start_pos[0]][start_pos[1]] = 2  # Mark the start
        maze[end_pos[0]][end_pos[1]] = 3  # Mark the end
        visualize_maze(maze)
    else:
            print("No path found using the Genetic Algorithm")

if __name__ == "__main__":
    main()
    
""" 33 steg """