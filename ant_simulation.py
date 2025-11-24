import random
import copy

class Ant:
    def __init__(self, position, hive_id):
        self.position = position
        self.hive_id = hive_id
        self.state = 'searching'
        self.path = [position]

    def move(self, grid, pheromones, decay_factor):
        x, y = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        possible_moves = []
        pheromone_sums = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 6 and 0 <= ny < 6 and grid[nx][ny] != 1:  # not obstacle
                possible_moves.append((nx, ny))
                # sum pheromones in adjacent cells
                adj_sum = sum(pheromones[nx][ny] for dx2, dy2 in directions if 0 <= nx+dx2 < 6 and 0 <= ny+dy2 < 6)
                pheromone_sums.append(adj_sum)

        if not possible_moves:
            return  # stuck, no move

        if self.state == 'returning':
            # follow path back
            if len(self.path) > 1:
                next_pos = self.path[-2]
                self.path.pop()
                self.position = next_pos
                pheromones[x][y] += 10  # add pheromones on return
            else:
                self.state = 'searching'
                self.path = [self.position]
        else:
            # searching
            max_pher = max(pheromone_sums) if pheromone_sums else 0
            if max_pher > 0.1:  # threshold for strong signal
                candidates = [m for m, p in zip(possible_moves, pheromone_sums) if p == max_pher]
                next_pos = random.choice(candidates)
            else:
                next_pos = random.choice(possible_moves)
            self.position = next_pos
            self.path.append(next_pos)

        # check if at food or hive
        if grid[self.position[0]][self.position[1]] == 4 and self.state == 'searching':
            self.state = 'returning'
        elif (self.hive_id == 1 and grid[self.position[0]][self.position[1]] == 2) or \
             (self.hive_id == 2 and grid[self.position[0]][self.position[1]] == 3) and self.state == 'returning':
            self.state = 'searching'
            self.path = [self.position]

def initialize_grid():
    grid = [[0 for _ in range(6)] for _ in range(6)]
    grid[0][0] = 2  # H1
    grid[0][5] = 3  # H2
    grid[5][2] = 4  # F

    # random obstacles, avoid direct paths
    obstacles = 0
    while obstacles < 5:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        if grid[x][y] == 0 and not (x == 0 and y in [0,5]) and not (x == 5 and y == 2):
            grid[x][y] = 1
            obstacles += 1

    return grid

def initialize_ants():
    ants = []
    for i in range(4):
        ants.append(Ant((0,0), 1))
        ants.append(Ant((0,5), 2))
    return ants

def decay_pheromones(pheromones, decay_factor):
    for i in range(6):
        for j in range(6):
            pheromones[i][j] *= decay_factor

def simulate(decay_factor, max_steps=100):
    grid = initialize_grid()
    pheromones = [[0.0 for _ in range(6)] for _ in range(6)]
    ants = initialize_ants()
    food_discoveries = {'H1': 0, 'H2': 0}

    for step in range(max_steps):
        decay_pheromones(pheromones, decay_factor)
        for ant in ants:
            ant.move(grid, pheromones, decay_factor)
            if ant.state == 'returning' and grid[ant.position[0]][ant.position[1]] == 4:
                if ant.hive_id == 1:
                    food_discoveries['H1'] += 1
                else:
                    food_discoveries['H2'] += 1

    return food_discoveries, grid, pheromones, ants

def run_experiments():
    decay_rates = [0.9, 0.95, 0.99]
    results = []

    for decay in decay_rates:
        total_h1 = 0
        total_h2 = 0
        for trial in range(5):  # 5 trials
            disc, _, _, _ = simulate(decay)
            total_h1 += disc['H1']
            total_h2 += disc['H2']
        avg_h1 = total_h1 / 5
        avg_h2 = total_h2 / 5
        results.append((decay, avg_h1, avg_h2))
        print(f"Decay {decay}: H1 avg discoveries {avg_h1}, H2 avg {avg_h2}")

    return results

if __name__ == "__main__":
    run_experiments()