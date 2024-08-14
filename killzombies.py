import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft Steve's Zombie Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
steve = pygame.image.load("steve.png")
zombie = pygame.image.load("zombie.png")
arrow = pygame.image.load("arrow.png")

# Scale images
steve = pygame.transform.scale(steve, (50, 50))
zombie = pygame.transform.scale(zombie, (40, 40))
arrow = pygame.transform.scale(arrow, (30, 10))

# Player
player_x = 50
player_y = HEIGHT // 2

# Arrows
arrows = []

# Zombies
zombies = []

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                arrows.append([player_x + 50, player_y + 25])

    # Move arrows
    for arrow in arrows:
        arrow[0] += 10
        if arrow[0] > WIDTH:
            arrows.remove(arrow)

    # Spawn zombies
    if random.randint(1, 60) == 1:
        zombies.append([WIDTH, random.randint(0, HEIGHT - 40)])

    # Move zombies
    for zombie_pos in zombies:
        zombie_pos[0] -= 2
        if zombie_pos[0] < 0:
            zombies.remove(zombie_pos)

    # Check for collisions
    for arrow in arrows:
        for zombie_pos in zombies:
            if (arrow[0] > zombie_pos[0] and
                arrow[0] < zombie_pos[0] + 40 and
                arrow[1] > zombie_pos[1] and
                arrow[1] < zombie_pos[1] + 40):
                arrows.remove(arrow)
                zombies.remove(zombie_pos)
                break

    # Clear the screen
    screen.fill(WHITE)

    # Draw player
    screen.blit(steve, (player_x, player_y))

    # Draw arrows
    for arrow_pos in arrows:
        screen.blit(arrow, arrow_pos)

    # Draw zombies
    for zombie_pos in zombies:
        screen.blit(zombie, zombie_pos)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()