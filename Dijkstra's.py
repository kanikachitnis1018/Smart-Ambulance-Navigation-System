import pygame
import heapq

# Initialize Pygame
pygame.init()

# Grid dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Grid Visualization")

# Grid layout (1 = road, 0 = obstacle)
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

start = (0, 0)
end = (7, 10)

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 1:
            neighbors.append((nx, ny))
    return neighbors

def dijkstra(start, end):
    heap = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {start: None}

    while heap:
        curr_cost, current = heapq.heappop(heap)

        if current == end:
            break

        for neighbor in get_neighbors(current):
            new_cost = curr_cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, cost_so_far[end]

def draw_grid(win, path):
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = WHITE if grid[i][j] == 1 else BLACK
            pygame.draw.rect(win, color, rect)
            pygame.draw.rect(win, GREY, rect, 1)

    for (x, y) in path:
        pygame.draw.rect(win, BLUE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(win, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(win, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()

def main():
    path, cost = dijkstra(start, end)
    print("Dijkstra Path Cost:", cost)
    print("Path:", path)

    running = True
    while running:
        draw_grid(win, path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
