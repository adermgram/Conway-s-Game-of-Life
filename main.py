import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 600, 600
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])


def draw_grid(positions, show_grid=True):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, BLUE, (*top_left, TILE_SIZE, TILE_SIZE))

    if show_grid:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                neighbors.append((nx, ny))
                
    return neighbors

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        alive_neighbors = sum(1 for n in neighbors if n in positions)
        if alive_neighbors in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        alive_neighbors = sum(1 for n in get_neighbors(position) if n in positions)
        if alive_neighbors == 3:
            new_positions.add(position)

    return new_positions

def main():
    running = True
    playing = False
    count = 0
    update_freq = 120  # Default update frequency
    min_update_freq = 10
    max_update_freq = 200

    positions = set()

    show_grid = True

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)


        
        pygame.display.set_caption(f"Game of Life - {'Playing' if playing else 'Paused'} | Speed: {update_freq}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randint(2, 5) * GRID_WIDTH)

                if event.key == pygame.K_UP:
                    update_freq = max(min_update_freq, update_freq - 10)

                if event.key == pygame.K_DOWN:
                    update_freq = min(max_update_freq, update_freq + 10)

                if event.key == pygame.K_t:
                    show_grid = not show_grid

                
        screen.fill(BLACK)
        draw_grid(positions, show_grid)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
