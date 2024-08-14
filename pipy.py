import pygame
import random
import math
import time

# ... (previous code remains unchanged until the game loop)

# Timer for adding new impostors
last_impostor_time = time.time()
IMPOSTOR_SPAWN_INTERVAL = 10  # Changed from 60 to 10 seconds

# Game loop
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    # ... (previous code remains unchanged)

    if not game_over:
        # ... (previous code remains unchanged)

        # Add new impostor every 10 seconds
        current_time = time.time()
        if current_time - last_impostor_time >= IMPOSTOR_SPAWN_INTERVAL:
            impostors.append(Player(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), RED, True))
            last_impostor_time = current_time

    # ... (previous code remains unchanged)

    # Display time until next impostor
    time_left = IMPOSTOR_SPAWN_INTERVAL - (current_time - last_impostor_time)
    next_impostor_text = font.render(f"Next Impostor: {int(time_left)}s", True, WHITE)
    screen.blit(next_impostor_text, (10, 90))

    # ... (rest of the code remains unchanged)

pygame.quit()