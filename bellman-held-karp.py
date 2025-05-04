import pygame
import heapq
import time

# Initialize pygame
pygame.init()

# Grid definition
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

WIDTH, HEIGHT = 600, 600
ROWS, COLS = len(grid), len(grid[0])
TILE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hybrid Bellman-Ford + Dijkstra")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

start = (0, 0)
end = (7, 10)

def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if grid[i][j] == 1 else BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
    pygame.draw.rect(screen, GREEN, (start[1]*TILE_SIZE, start[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (end[1]*TILE_SIZE, end[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 1:
            neighbors.append((nx, ny))
    return neighbors

def bellman_ford(start):
    dist = {start: 0}
    prev = {}
    for _ in range(ROWS * COLS - 1):
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == 1:
                    for neighbor in get_neighbors((i, j)):
                        if (i, j) in dist:
                            new_dist = dist[(i, j)] + 1
                            if neighbor not in dist or new_dist < dist[neighbor]:
                                dist[neighbor] = new_dist
                                prev[neighbor] = (i, j)
    return dist, prev

def dijkstra(start):
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]
    while heap:
        d, current = heapq.heappop(heap)
        for neighbor in get_neighbors(current):
            new_dist = d + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))
    return dist, prev

def hybrid_path(start, end):
    dist_b, prev_b = bellman_ford(start)
    dist_d, prev_d = dijkstra(start)

    # Average distances
    dist_comb = {}
    prev_comb = {}
    for node in set(dist_b.keys()) | set(dist_d.keys()):
        b = dist_b.get(node, float('inf'))
        d = dist_d.get(node, float('inf'))
        avg = (b + d) / 2
        dist_comb[node] = avg
        prev_comb[node] = prev_b.get(node, prev_d.get(node))

    path = []
    current = end
    while current != start:
        path.append(current)
        current = prev_comb.get(current)
        if current is None:
            return [], float('inf')
    path.append(start)
    path.reverse()
    return path, dist_comb.get(end, float('inf'))

def draw_path(path):
    for cell in path:
        pygame.draw.rect(screen, BLUE, (cell[1]*TILE_SIZE, cell[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.display.flip()
        time.sleep(0.05)

# Run visualization
run = True
clock = pygame.time.Clock()

path, cost = hybrid_path(start, end)
print("Hybrid Path:", path)
print("Cost:", cost)

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_grid()
    draw_path(path)
    pygame.display.flip()

pygame.quit()
