import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Among Us")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, is_impostor=False):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5 if not is_impostor else 4.5  # Impostor is slightly slower
        self.is_impostor = is_impostor

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def ai_move(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy)

    def chase(self, target):
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.move(dx, dy)

# Create players
player = Player(WIDTH // 2, HEIGHT // 2, BLUE)
impostor = Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED, True)
crewmates = [Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), GREEN) for _ in range(3)]

all_sprites = pygame.sprite.Group(player, impostor, *crewmates)
ai_players = pygame.sprite.Group(*crewmates)

# Game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    player.move(dx, dy)

    # Move AI crewmates
    for ai_player in ai_players:
        ai_player.ai_move()

    # Move impostor (chase the player)
    impostor.chase(player)

    # Check for collision with impostor
    if pygame.sprite.collide_rect(player, impostor):
        print("Game Over! The impostor caught you!")
        running = False

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display survival time
    current_time = pygame.time.get_ticks()
    survival_time = (current_time - start_time) // 1000  # Convert to seconds
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Time: {survival_time}s", True, BLACK)
    screen.blit(time_text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()