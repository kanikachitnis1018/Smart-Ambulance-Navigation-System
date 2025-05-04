import pygame
import time

pygame.init()

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

ROWS, COLS = len(grid), len(grid[0])
CELL_SIZE = 40
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bellman-Ford Pathfinding")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if grid[i][j] == 1 else BLACK
            pygame.draw.rect(WIN, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(WIN, GRAY, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def get_neighbors(pos):
    x, y = pos
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 1:
            yield (nx, ny)

def bellman_ford(start, end):
    dist = [[float("inf")] * COLS for _ in range(ROWS)]
    prev = [[None] * COLS for _ in range(ROWS)]
    dist[start[0]][start[1]] = 0

    for _ in range(ROWS * COLS - 1):
        for x in range(ROWS):
            for y in range(COLS):
                if grid[x][y] == 0:
                    continue
                for nx, ny in get_neighbors((x, y)):
                    if dist[x][y] + 1 < dist[nx][ny]:
                        dist[nx][ny] = dist[x][y] + 1
                        prev[nx][ny] = (x, y)

    path = []
    x, y = end
    if dist[x][y] == float("inf"):
        print("No path found")
        return []
    while (x, y) != start:
        path.append((x, y))
        x, y = prev[x][y]
    path.append(start)
    path.reverse()

    print("Bellman-Ford Path Cost:", dist[end[0]][end[1]])
    return path

def animate_path(path):
    for x, y in path:
        pygame.draw.rect(WIN, BLUE, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        time.sleep(0.1)

def main():
    start = (0, 0)
    goal = (7, 14)
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        draw_grid()
        pygame.draw.rect(WIN, GREEN, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(WIN, GREEN, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        path = bellman_ford(start, goal)
        animate_path(path)
        run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main()
