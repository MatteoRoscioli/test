import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q*bert")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game variables
CUBE_SIZE = 50
GRID_SIZE = 7

# Player
player_pos = [3, 0]
player_img = pygame.Surface((CUBE_SIZE // 2, CUBE_SIZE // 2))
player_img.fill(ORANGE)

# Enemy
enemy_pos = [0, 0]
enemy_img = pygame.Surface((CUBE_SIZE // 2, CUBE_SIZE // 2))
enemy_img.fill(RED)

# Cube grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_cube(x, y, color):
    points = [
        (x, y + CUBE_SIZE // 2),
        (x + CUBE_SIZE // 2, y),
        (x + CUBE_SIZE, y + CUBE_SIZE // 2),
        (x + CUBE_SIZE // 2, y + CUBE_SIZE)
    ]
    pygame.draw.polygon(screen, color, points)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - y):
            color = BLUE if grid[y][x] else WHITE
            draw_cube(
                WIDTH // 2 - (GRID_SIZE // 2 - x) * CUBE_SIZE + y * CUBE_SIZE // 2,
                HEIGHT // 2 + y * CUBE_SIZE * 3 // 4 - GRID_SIZE * CUBE_SIZE // 2,
                color
            )

def move_player(dx, dy):
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < GRID_SIZE - new_y and 0 <= new_y < GRID_SIZE:
        player_pos[0], player_pos[1] = new_x, new_y
        grid[new_y][new_x] = 1

def move_enemy():
    dx, dy = random.choice([(0, 1), (1, 0), (-1, 1), (1, -1)])
    new_x, new_y = enemy_pos[0] + dx, enemy_pos[1] + dy
    if 0 <= new_x < GRID_SIZE - new_y and 0 <= new_y < GRID_SIZE:
        enemy_pos[0], enemy_pos[1] = new_x, new_y

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_player(-1, 1)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(1, -1)

    move_enemy()

    screen.fill(BLACK)
    draw_grid()

    # Draw player
    player_screen_pos = (
        WIDTH // 2 - (GRID_SIZE // 2 - player_pos[0]) * CUBE_SIZE + player_pos[1] * CUBE_SIZE // 2,
        HEIGHT // 2 + player_pos[1] * CUBE_SIZE * 3 // 4 - GRID_SIZE * CUBE_SIZE // 2
    )
    screen.blit(player_img, player_screen_pos)

    # Draw enemy
    enemy_screen_pos = (
        WIDTH // 2 - (GRID_SIZE // 2 - enemy_pos[0]) * CUBE_SIZE + enemy_pos[1] * CUBE_SIZE // 2,
        HEIGHT // 2 + enemy_pos[1] * CUBE_SIZE * 3 // 4 - GRID_SIZE * CUBE_SIZE // 2
    )
    screen.blit(enemy_img, enemy_screen_pos)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()