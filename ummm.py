import pygame
import random
import math
import time
import os

# ... (previous code remains the same)

# Game loop
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                impostor_freeze = not impostor_freeze
            elif event.key == pygame.K_a:
                bullets.append(Bullet(player.x, player.y, -1))  # Shoot left
            elif event.key == pygame.K_d:
                bullets.append(Bullet(player.x, player.y, 1))   # Shoot right
            elif event.key == pygame.K_w:
                bullets.append(Bullet(player.x, player.y, 0, -1))  # Shoot up
            elif event.key == pygame.K_s:
                bullets.append(Bullet(player.x, player.y, 0, 1))   # Shoot down

    if not game_over:
        # ... (rest of the game logic remains the same)

        # Move and check bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                bullets.remove(bullet)
            else:
                for impostor in impostors[:]:
                    if math.sqrt((bullet.x - impostor.x)**2 + (bullet.y - impostor.y)**2) < bullet.radius + impostor.radius:
                        impostors.remove(impostor)
                        bullets.remove(bullet)
                        score += 1  # Increase score when killing an impostor
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                        break

        # ... (rest of the code remains the same)

pygame.quit()