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
        positions = self._positions
        x, y = self._x, self._y

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
                self._fitness += 50

            if maze[y][x] == 0:
                known_walls.add(position)
                self._fitness += 5
            elif maze[y][x] == 1:
                if position in positions:
                    self._fitness += 25
                self._x, self._y = x, y

            if (self._x, self._y) == end:
                self._fitness -= 500

            positions = np.append(positions, np.array([(self._x, self._y)], dtype=int), axis=0)

        return self._fitness

class SolverGA:
    def __init__(self, npop, mutRate, individualLength, maze):
        self.n_pop = npop
        self.mut_rate = mutRate
        self.indv_len = individualLength
        self._players = []
        for i in range(npop):
            way = []
            for i in range(individualLength):
                way.append(random.choice(['up', 'down', 'left', 'right']))
            player = Player(way)
            self._players.append(player)
        self.maze = maze
        self._generation = 0

    def fitness_scores(self, end):
        best = math.inf
        best_player = None

        for player in self._players:
            fitness = player.evaluate_path(self.maze, end)
            if fitness < best:
                best = fitness
                best_player = player

        print(f"Generation {self._generation}. The best fitness was {best}")
        best_way = best_player._way
        print(f"Way: {best_way}")

    def best_parents(self):
        tournament_size = 5
        selected_population = []

        for i in range(self.n_pop):
            tournament = random.sample(range(self.n_pop), tournament_size)
            winner = tournament[0]
            for competitor in tournament[1:]:
                if self._players[competitor]._fitness < self._players[winner]._fitness:
                    winner = competitor
            selected_population.append(self._players[winner])

        return selected_population

    def new_generation(self):
        selected_population = self.best_parents()
        new_players = []

        for i in range(self.n_pop):
            parent1 = random.choice(selected_population)._way
            parent2 = random.choice(selected_population)._way
            crosspoint = random.randint(0, self.indv_len - 1)
            child = np.concatenate((parent1[:crosspoint], parent2[crosspoint:]), axis=None)

            for j in range(self.indv_len):
                if random.random() < self.mut_rate:
                    child[j] = random.choice(['up', 'down', 'left', 'right'])

            new_players.append(Player(child))

        self._players = new_players

    def game_over(self, end):
        for player in self._players:
            if end in player._positions:
                print(f"Solution found!\nPath: {player._positions}")
                return True
        return False

    def solve(self, end):
        self.fitness_scores(end)
        while not self.game_over(end):
            self.new_generation()
            self._generation += 1
            self.fitness_scores(end)

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


    end_point = (37, 13)
    solver = SolverGA(100, 0.3, 100, maze)
    solver.solve(end_point)

if __name__ == "__main__":
    main()