import pygame
import time
import heapq

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
pygame.display.set_caption("A* Pathfinding Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# A* Algorithm with Cost Calculation
def astar(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            total_cost = g_score[current]
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, total_cost

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] == 1:
                temp_g_score = g_score[current] + 1  # Step cost is 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return [], float('inf')

# Car class
class Car:
    def __init__(self, x, y, destination):
        self.x = x
        self.y = y
        self.path, self.total_cost = astar((x, y), destination)

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
