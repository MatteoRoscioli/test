import pygame
import random
import math
import time
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Among Us Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.Font(None, 36)

# High score file
HIGH_SCORE_FILE = "high_score.txt"

# Player class
class Player:
    def __init__(self, x, y, color, is_impostor):
        self.x = x
        self.y = y
        self.color = RED if is_impostor else color
        self.is_impostor = is_impostor
        self.speed = 3 if is_impostor else 5
        self.radius = 20
        self.alive = True

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Keep the player within the screen boundaries
        self.x = max(self.radius, min(new_x, WIDTH - self.radius))
        self.y = max(self.radius, min(new_y, HEIGHT - self.radius))

    def draw(self):
        if self.alive:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            if self.is_impostor:
                text = font.render("IMPOSTOR", True, WHITE)
                screen.blit(text, (self.x - 50, self.y - 50))

    def distance_to(self, other_player):
        return math.sqrt((self.x - other_player.x)**2 + (self.y - other_player.y)**2)

# Bullet class
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 10
        self.radius = 5

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

# Function to get the high score
def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

# Function to save the high score
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Game variables
player = None
impostors = []
impostor_freeze = False
bullets = []
score = 0
round_number = 1
high_score = get_high_score()

# Create the player (you)
player = Player(WIDTH // 2, HEIGHT // 2, BLUE, False)

# Create the initial impostor
impostors.append(Player(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), RED, True))

# Timer for adding new impostors
last_impostor_time = time.time()

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
                bullets.append(Bullet(player.x, player.y, -1, 0))  # Shoot left
            elif event.key == pygame.K_d:
                bullets.append(Bullet(player.x, player.y, 1, 0))   # Shoot right
            elif event.key == pygame.K_w:
                bullets.append(Bullet(player.x, player.y, 0, -1))  # Shoot up
            elif event.key == pygame.K_s:
                bullets.append(Bullet(player.x, player.y, 0, 1))   # Shoot down

    if not game_over:
        # Move the player (user-controlled)
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        player.move(dx, dy)

        if not impostor_freeze:
            # Move the impostors towards the player
            for impostor in impostors:
                angle = math.atan2(player.y - impostor.y, player.x - impostor.x)
                impostor.move(math.cos(angle), math.sin(angle))

        # Check if any impostor caught the player
        for impostor in impostors:
            if impostor.distance_to(player) < impostor.radius + player.radius:
                player.alive = False
                game_over = True
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

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

        # Add new impostors every 10 seconds
        current_time = time.time()
        if current_time - last_impostor_time >= 10:
            for _ in range(round_number):  # Spawn 'round_number' impostors each round
                impostors.append(Player(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), RED, True))
            last_impostor_time = current_time
            round_number += 1  # Increase round number

    # Draw everything
    screen.fill(BLACK)
    player.draw()
    for impostor in impostors:
        impostor.draw()
    for bullet in bullets:
        bullet.draw()

    # Display impostor freeze status and number of impostors
    freeze_text = font.render("Impostors Frozen" if impostor_freeze else "Impostors Active", True, WHITE)
    screen.blit(freeze_text, (10, 10))
    impostor_count = font.render(f"Impostors: {len(impostors)}", True, WHITE)
    screen.blit(impostor_count, (10, 50))

    # Display time until next impostor
    time_left = 10 - (current_time - last_impostor_time)
    next_impostor_text = font.render(f"Next Impostor: {int(time_left)}s", True, WHITE)
    screen.blit(next_impostor_text, (10, 90))

    # Display score, high score, and round number
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH - 200, 50))
    round_text = font.render(f"Round: {round_number}", True, WHITE)
    screen.blit(round_text, (WIDTH - 150, 90))

    if game_over:
        text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
        if score == high_score:
            new_high_score_text = font.render("New High Score!", True, YELLOW)
            screen.blit(new_high_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()