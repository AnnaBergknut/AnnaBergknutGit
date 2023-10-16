import random
import math

class Player:
    def __init__(self, way):
        self._positions = [(1, 1)]
        self._x = 1
        self._y = 1
        self._fitness = 0
        self._way = way
        self._known_walls = []

    def evaluate_path(self, maze, end):

        for direction in self._way:
            x = self._x
            y = self._y
            if direction == 'right':
                x += 1
            elif direction == 'left':
                x -= 1
            elif direction == 'up':
                y -= 1
            elif direction == 'down':
                y += 1

            if (x, y) in self._known_walls:
                self._fitness += 50

            if maze[y][x] == 0:
                self._known_walls.append((x, y))
                self._fitness += 5
            elif maze[y][x] == 1:
                if (x, y) in self._positions:
                    self._fitness += 25
                self._x = x
                self._y = y

            if (self._x, self._y) == end:
                self._fitness -= 500

            self._positions.append((self._x, self._y))

        return self._fitness

class SolverGA:
    def __init__(self, npop, mutRate, individualLength, maze):
        self.n_pop = npop
        self.mut_rate = mutRate
        self.indv_len = individualLength
        self._players = []
        for _ in range(npop):
            way = []
            for _ in range(individualLength):
                way.append(random.choice(['up', 'down', 'left', 'right']))
            player = Player(way)
            self._players.append(player)
        self._all_fit = {}
        self.maze = maze
        self._generation = 0

    def fitness_scores(self, end):
        self._all_fit = {}
        best = math.inf
        index = 0
        for player in self._players:
            self._all_fit[index] = (player, player.evaluate_path(self.maze, end))
            if self._all_fit[index][1] < best:
                best = self._all_fit[index][1]
                best_player = index
            index += 1
        print(f"Generation {self._generation}. The best fitness was {best}")
        path = self._all_fit[best_player]
        best_way = path[0]._way
        print(f"Way: {best_way}")

    def best_parents(self):

        selected_population = []
        for i in range(self.n_pop):
            tournament_size = 5
            tournament = random.sample(range(self.n_pop), tournament_size)
            winner = tournament[0]
            for competitor in tournament[1:]:
                if self._all_fit[competitor][1] < self._all_fit[winner][1]:
                    winner = competitor
            selected_population.append(self._all_fit[winner][0])
        return selected_population

    def new_generation(self):
        self._players = []
        selected_population = self.best_parents()
        for i in range(self.n_pop):
            parent1 = random.choice(selected_population)._way
            parent2 = random.choice(selected_population)._way
            crosspoint = random.randint(0, self.indv_len - 1)
            child = parent1[:crosspoint] + parent2[crosspoint:]
            for j in range(self.indv_len):
                if random.random() < self.mut_rate:
                    child[j] = random.choice(['up', 'down', 'left', 'right'])
            self._players.append(Player(child))

    def game_over(self, end):
        for player in self._players:
            if end in player._positions:
                print(f"Solution found! \nPath: {player._positions}")
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
    #        0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0
    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #0
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
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]] #14

    # Define the end point you want to reach
    end_point = (37, 13)
    # # Create a SolverGA instance and solve the maze
    solver = SolverGA(100, 0.3, 150, maze)
    solver.solve(end_point)


if __name__ == "__main__":
    main()