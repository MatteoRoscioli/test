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
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, is_impostor=False):
        super().__init__()
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        self.color = RED if is_impostor else color
        self.is_impostor = is_impostor
        self.draw_character()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2.7 if is_impostor else 3

    def draw_character(self):
        pygame.draw.ellipse(self.image, self.color, (0, 0, 30, 35))
        pygame.draw.ellipse(self.image, CYAN, (5, 5, 20, 15))
        pygame.draw.rect(self.image, self.color, (5, 35, 8, 5))
        pygame.draw.rect(self.image, self.color, (17, 35, 8, 5))
        if self.is_impostor:
            pygame.draw.polygon(self.image, RED, [(5, 0), (15, -10), (25, 0)])

    def move(self, dx, dy, walls):
        original_x, original_y = self.rect.x, self.rect.y
        
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x, self.rect.y = original_x, original_y
                return
            
    def ai_move(self, walls):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy, walls)

    def chase(self, target, walls):
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.move(dx, dy, walls)

# Create map
walls = [
    pygame.Rect(0, 0, WIDTH, 10),
    pygame.Rect(0, 0, 10, HEIGHT),
    pygame.Rect(WIDTH-10, 0, 10, HEIGHT),
    pygame.Rect(0, HEIGHT-10, WIDTH, 10),
    pygame.Rect(200, 0, 10, 150),
    pygame.Rect(200, 250, 10, 150),
    pygame.Rect(400, 200, 10, 150),
    pygame.Rect(400, 450, 10, 150),
    pygame.Rect(600, 0, 10, 150),
    pygame.Rect(600, 250, 10, 150),
    pygame.Rect(0, 200, 190, 10),
    pygame.Rect(210, 400, 190, 10),
    pygame.Rect(410, 200, 190, 10),
]

# Create players
player = Player(WIDTH // 2, HEIGHT // 2, BLUE)
impostor = Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED, True)
crewmate_colors = [GREEN, YELLOW, (255, 165, 0)]
crewmates = [Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice(crewmate_colors)) for _ in range(3)]

all_sprites = pygame.sprite.Group(player, impostor, *crewmates)
ai_players = pygame.sprite.Group(*crewmates)

# Game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

def is_alone(player, others, distance=100):
    return all(math.hypot(player.rect.x - other.rect.x, player.rect.y - other.rect.y) > distance for other in others)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    player.move(dx, dy, walls)

    for ai_player in ai_players:
        ai_player.ai_move(walls)

    impostor.chase(player, walls)

    if pygame.sprite.collide_rect(player, impostor) and is_alone(player, crewmates):
        print("Game Over! The impostor killed you!")
        running = False

    screen.fill(WHITE)
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)
    all_sprites.draw(screen)

    current_time = pygame.time.get_ticks()
    survival_time = (current_time - start_time) // 1000
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Time: {survival_time}s", True, BLACK)
    screen.blit(time_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()