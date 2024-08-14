
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Among Us")

# Colors
ORANGE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

# Create players
player = Player(WIDTH // 2, HEIGHT // 2, BLUE)
impostor = Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED)

all_sprites = pygame.sprite.Group(player, impostor)

# Game loop
running = True
clock = pygame.time.Clock()

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

    # Move impostor (simple AI)
    if random.random() < 0.02:  # 2% chance to change direction each frame
        impostor.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

    # Check for collision
    if pygame.sprite.collide_rect(player, impostor):
        print("Game Over! The impostor caught you!")
        running = False

    # Draw everything
    screen.fill(WIDTH)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()