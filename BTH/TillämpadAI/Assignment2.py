import random
import math
import numpy as np

class Player:
    def __init__(self, way):
        self._x, self._y = 1, 1
        self._positions = np.array([(self._x, self._y)], dtype=int)
        self._fitness = 0
        self._way = way
        self._known_walls = set()

    def evaluate_path(self, maze, end):
        known_walls = self._known_walls
        x, y = self._x, self._y
        fitness = 0

        for direction in self._way:
            if direction == 'right':
                x += 2
            elif direction == 'left':
                x -= 2
            elif direction == 'up':
                y -= 2
            elif direction == 'down':
                y += 2

            # Ensure the player's position stays within bounds
            x = max(1, min(x, maze.shape[1] - 2))
            y = max(1, min(y, maze.shape[0] - 2))

            position = (x, y)
            if position in known_walls:
                fitness += 50

            if maze[y][x] == 0:
                known_walls.add(position)
                fitness += 5
            elif maze[y][x] == 1:
                if position in self._positions:
                    fitness += 25
                self._x, self._y = x, y

            if (self._x, self._y) == end:
                fitness -= 500

            self._positions = np.append(self._positions, np.array([(self._x, self._y)], dtype=int), axis=0)

        self._fitness = fitness  # Update the fitness after the loop
        return fitness

class SolverGA:
    def __init__(self, npop, crossover_rate, mutation_rate, individualLength, maze):
        self.n_pop = npop
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.indv_len = individualLength
        self._players = []
        self.maze = maze
        self._generation = 0

    def initialize_population(self):
        self._players = []
        for _ in range(self.n_pop):
            way = [random.choice(['up', 'down', 'left', 'right']) for _ in range(self.indv_len)]
            player = Player(way)
            self._players.append(player)

    def fitness_scores(self, end):
        for player in self._players:
            player.evaluate_path(self.maze, end)
        
    def select_parents(self):
        num_parents = max(2, int(self.n_pop * self.crossover_rate))
        sorted_players = sorted(self._players, key=lambda x: x._fitness)
        return sorted_players[:num_parents]

    def crossover(self, parent1, parent2):
        crosspoint = random.randint(0, self.indv_len - 1)
        child_way = parent1._way[:crosspoint] + parent2._way[crosspoint:]
        return Player(child_way)

    def mutate(self, player):
        for i in range(self.indv_len):
            if random.random() < self.mutation_rate:
                player._way[i] = random.choice(['up', 'down', 'left', 'right'])

    def new_generation(self, parents):
        new_players = parents.copy()

        while len(new_players) < self.n_pop:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_players.append(child)

        self._players = new_players

    def game_over(self, end):
        for player in self._players:
            if end in player._positions:
                print(f"Solution found!\nPath: {player._positions}")
                return True
        return False

    def solve(self, end):
        self.initialize_population()
        while not self.game_over(end):
            self.fitness_scores(end)
            parents = self.select_parents()
            self.new_generation(parents)
            self._generation += 1
            
def main():
    #                            1                   2                   3                   4
    maze = np.array(
    #        0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0
            [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #0
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0], #1
            [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0], #2
            [0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0], #3
            [0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0], #4
            [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0], #5
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0], #6
            [0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0], #7
            [0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0], #8
            [0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0], #9
            [0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0], #10
            [0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0], #11
            [0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0], #12
            [0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0], #13
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  #14
            ], dtype=int)

    npop=100
    crossover_rate=0.6
    mutation_rate=0.1
    individualLength=100
    
    end_point = (37, 13)
    solver = SolverGA(npop, crossover_rate, mutation_rate, individualLength, maze)
    solver.solve(end_point)

if __name__ == "__main__":
    main()