import pygame
import time
import heapq
import random

# Initialize pygame
pygame.init()

# Grid representation (1 = road, 0 = obstacle)
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Pheromone Map for BCO
pheromones = [[1 for _ in range(len(grid[0]))] for _ in range(len(grid))]

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
            neighbors.append((nx, ny))
    return neighbors

def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, g_score[goal]

        for neighbor in get_neighbors(current):
            temp_g_score = g_score[current] + 1
            if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return [], float('inf')

def bco(start, goal):
    paths = []
    costs = []
    for _ in range(5):  # 5 artificial bees
        path = [start]
        cost = 0
        current = start
        while current != goal:
            neighbors = get_neighbors(current)
            if not neighbors:
                break
            weights = [pheromones[n[0]][n[1]] for n in neighbors]
            total_weight = sum(weights)
            probs = [w / total_weight for w in weights]
            next_step = random.choices(neighbors, probs)[0]
            cost += 1
            path.append(next_step)
            current = next_step
        paths.append(path)
        costs.append(cost)
    best_index = costs.index(min(costs))
    return paths[best_index], costs[best_index]

def hybrid_a_star_bco(start, goal):
    path_a, cost_a = a_star(start, goal)
    path_b, cost_b = bco(start, goal)
    refined_path = list(set(path_a + path_b))  # Combine paths
    return refined_path, len(refined_path)

# Running the algorithms
start, goal = (0, 0), (7, 10)
path_a, cost_a = a_star(start, goal)
path_b, cost_b = bco(start, goal)
path_h, cost_h = hybrid_a_star_bco(start, goal)

# Print results
print("A* Cost:", cost_a)
print("BCO Cost:", cost_b)
print("A*-BCO Hybrid Cost:", cost_h)
