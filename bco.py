import pygame
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

# Window settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = len(grid), len(grid[0])
CELL_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BCO Pathfinding Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# BCO Algorithm
def bco(start, goal, max_iterations=100):
    best_path = []
    best_cost = float('inf')

    for _ in range(max_iterations):
        path = [start]
        current = start
        cost = 0

        while current != goal:
            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
            valid_neighbors = [n for n in neighbors if 0 <= n[0] < ROWS and 0 <= n[1] < COLS and grid[n[0]][n[1]] == 1]

            if not valid_neighbors:
                break

            next_move = random.choice(
                valid_neighbors)  # Random selection (can be improved with pheromone-based probabilities)
            path.append(next_move)
            cost += 1
            current = next_move

        if current == goal and cost < best_cost:
            best_cost = cost
            best_path = path

    return best_path, best_cost


# Car class
class Car:
    def __init__(self, x, y, destination):
        self.x = x
        self.y = y
        self.path, self.total_cost = bco((x, y), destination)

    def move(self):
        if self.path:
            next_pos = self.path.pop(0)
            self.x, self.y = next_pos
            print(f"Car moved to: ({self.x}, {self.y})")

    def draw(self):
        pygame.draw.rect(screen, RED, (self.y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Initialize objects
start_pos = (0, 0)
dest_pos = (7, 10)
car = Car(*start_pos, dest_pos)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw grid
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if grid[i][j] == 1 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Move and draw car
    car.move()
    car.draw()

    pygame.display.flip()
    pygame.time.delay(500)

# Print total cost in terminal
print(f"Total Path Cost: {car.total_cost}")
pygame.quit()
