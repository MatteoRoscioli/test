import pygame
import sys
import math
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Harry Potter vs Monsters")

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
SKIN = (255, 224, 189)
PURPLE = (128, 0, 128)

# Hotbar properties
HOTBAR_SLOTS = 9
HOTBAR_SIZE = 400
SLOT_SIZE = HOTBAR_SIZE // HOTBAR_SLOTS
HOTBAR_Y = height - SLOT_SIZE - 10
HOTBAR_X = (width - HOTBAR_SIZE) // 2
selected_slot = 0

# Hotbar items (you can customize these)
hotbar_items = [
    {"name": "Wand", "color": BROWN, "icon": None},
    {"name": "Potion", "color": BLUE, "icon": None},
    {"name": "Spell Book", "color": PURPLE, "icon": None},
    {"name": "Broom", "color": DARK_GRAY, "icon": None},
    {"name": "Invisibility Cloak", "color": SILVER, "icon": None},
    {"name": "Time Turner", "color": GOLD, "icon": None},
    {"name": "Marauder's Map", "color": GRAY, "icon": None},
    {"name": "Remembrall", "color": RED, "icon": None},
    {"name": "Golden Snitch", "color": GOLD, "icon": None},
]

# Wizard properties
wizard_x = width // 2
wizard_y = height // 2
wizard_speed = 10
wizard_size = 60
wand_angle = 0

# Wand properties
wand_length = 40
slash_duration = 10
slash_angle = 90  # Total angle of slash arc
current_slash = 0

# Spell wave properties
slash_waves = []
wave_speed = 15
wave_lifetime = 30
wave_width = 60
wave_length = 30

# Monster properties
monsters = []
monster_size = 50
monster_speed = 2
max_monsters = 10
spawn_interval = 5  # seconds
last_spawn_time = time.time()
monsters_to_spawn = 1

# Kill counter
kill_count = 0
high_score = 0

# Game state
game_over = False
invincible = False

# Thunderbolt properties
thunderbolt_active = False
thunderbolt_start_time = 0
thunderbolt_duration = 2  # Thunderbolt lasts for 2 seconds
thunderbolt_cooldown = 10  # Thunderbolt cooldown is 10 seconds
last_thunderbolt_time = 0
thunderbolt_radius = 100

# Arrow key press counters
up_arrow_press_count = 0
down_arrow_press_count = 0
arrow_press_time = 2  # seconds to press 10 times
last_arrow_press_time = 0

# Game loop
running = True
clock = pygame.time.Clock()

def draw_wizard(surface, x, y, size):
    # Robe
    pygame.draw.rect(surface, BLACK, (int(x - size / 3), int(y - size / 2), int(size / 1.5), int(size)))
    # Face
    pygame.draw.circle(surface, SKIN, (int(x), int(y - size / 3)), int(size / 6))
    # Hair
    pygame.draw.arc(surface, BLACK, (int(x - size / 6), int(y - size / 2), int(size / 3), int(size / 3)), 3.14, 2 * 3.14, 5)
    # Glasses
    pygame.draw.circle(surface, BLACK, (int(x - size / 12), int(y - size / 3)), int(size / 18), 2)
    pygame.draw.circle(surface, BLACK, (int(x + size / 12), int(y - size / 3)), int(size / 18), 2)
    pygame.draw.line(surface, BLACK, (int(x), int(y - size / 3)), (int(x + size / 12), int(y - size / 3)), 2)
    # Scar
    pygame.draw.line(surface, RED, (int(x - size / 12), int(y - size / 2.5)), (int(x + size / 24), int(y - size / 2.2)), 2)

def draw_wand(surface, x, y, angle):
    wand_end_x = x + math.cos(math.radians(angle)) * wand_length
    wand_end_y = y - math.sin(math.radians(angle)) * wand_length
    pygame.draw.line(surface, BROWN, (int(x), int(y)), (int(wand_end_x), int(wand_end_y)), 3)

def create_slash_wave(x, y, angle):
    dx = math.cos(math.radians(angle)) * wave_speed
    dy = -math.sin(math.radians(angle)) * wave_speed
    return [x, y, dx, dy, wave_lifetime]

def create_monster():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x = random.randint(0, width)
        y = -monster_size
    elif side == 'bottom':
        x = random.randint(0, width)
        y = height + monster_size
    elif side == 'left':
        x = -monster_size
        y = random.randint(0, height)
    else:  # right
        x = width + monster_size
        y = random.randint(0, height)
    return [x, y]

def draw_monster(surface, x, y, size):
    # Body
    pygame.draw.circle(surface, (0, 128, 0), (int(x), int(y)), int(size / 2))
    # Eyes
    eye_size = size // 8
    pygame.draw.circle(surface, RED, (int(x - size / 4), int(y - size / 4)), eye_size)
    pygame.draw.circle(surface, RED, (int(x + size / 4), int(y - size / 4)), eye_size)
    # Mouth
    pygame.draw.arc(surface, BLACK, (int(x - size / 3), int(y), int(size / 1.5), int(size / 2)), 0, 3.14, 3)
    # Tentacles
    for i in range(4):
        angle = i * (360 / 4)
        end_x = x + math.cos(math.radians(angle)) * (size / 2)
        end_y = y + math.sin(math.radians(angle)) * (size / 2)
        pygame.draw.line(surface, (0, 100, 0), (int(x), int(y)), (int(end_x), int(end_y)), 3)

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_thunderbolt(surface, x, y):
    # Draw thunderbolt as a vertical line
    pygame.draw.line(surface, PURPLE, (int(x), int(y - thunderbolt_radius)), (int(x), int(y + thunderbolt_radius)), 5)
    pygame.draw.line(surface, PURPLE, (int(x - 10), int(y - thunderbolt_radius + 20)),
                     (int(x + 10), int(y - thunderbolt_radius + 20)), 5)
    pygame.draw.line(surface, PURPLE, (int(x - 10), int(y + thunderbolt_radius - 20)),
                     (int(x + 10), int(y + thunderbolt_radius - 20)), 5)
    pygame.draw.line(surface, PURPLE, (int(x - 20), int(y - thunderbolt_radius + 40)),
                     (int(x + 20), int(y - thunderbolt_radius + 40)), 5)

def draw_minecraft_hotbar(surface):
    # Draw the main hotbar rectangle
    hotbar_rect = pygame.Rect(HOTBAR_X, HOTBAR_Y, HOTBAR_SIZE, SLOT_SIZE)
    pygame.draw.rect(surface, (100, 100, 100), hotbar_rect)
    pygame.draw.rect(surface, (50, 50, 50), hotbar_rect, 2)

    # Draw individual slots
    for i in range(HOTBAR_SLOTS):
        slot_x = HOTBAR_X + i * SLOT_SIZE
        slot_rect = pygame.Rect(slot_x, HOTBAR_Y, SLOT_SIZE, SLOT_SIZE)
        pygame.draw.rect(surface, (150, 150, 150), slot_rect, 1)

        # Draw item in slot
        if i < len(hotbar_items):
            item = hotbar_items[i]
            item_rect = pygame.Rect(slot_x + 4, HOTBAR_Y + 4, SLOT_SIZE - 8, SLOT_SIZE - 8)
            pygame.draw.rect(surface, item["color"], item_rect)

            # Draw item name
            font = pygame.font.SysFont(None, 16)
            text = font.render(item["name"], True, WHITE)
            text_rect = text.get_rect(center=(slot_x + SLOT_SIZE // 2, HOTBAR_Y + SLOT_SIZE + 15))
            surface.blit(text, text_rect)

    # Highlight selected slot
    selected_rect = pygame.Rect(HOTBAR_X + selected_slot * SLOT_SIZE, HOTBAR_Y, SLOT_SIZE, SLOT_SIZE)
    pygame.draw.rect(surface, WHITE, selected_rect, 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                selected_slot = (selected_slot - 1) % HOTBAR_SLOTS
            elif event.button == 5:  # Scroll down
                selected_slot = (selected_slot + 1) % HOTBAR_SLOTS
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_slash == 0 and not game_over:
                current_slash = slash_duration
                slash_waves.append(create_slash_wave(wizard_x, wizard_y, wand_angle))
            elif event.key == pygame.K_r and game_over:
                # Reset the game
                wizard_x = width // 2
                wizard_y = height // 2
                monsters = []
                slash_waves = []
                kill_count = 0
                game_over = False
                last_spawn_time = time.time()
                monsters_to_spawn = 1
                invincible = False
                thunderbolt_active = False
                up_arrow_press_count = 0
                down_arrow_press_count = 0
            elif event.key == pygame.K_UP and not game_over:
                current_time = time.time()
                if current_time - last_arrow_press_time <= arrow_press_time:
                    up_arrow_press_count += 1
                else:
                    up_arrow_press_count = 1
                last_arrow_press_time = current_time
                if up_arrow_press_count >= 10:
                    invincible = True
                    up_arrow_press_count = 0
            elif event.key == pygame.K_DOWN and not game_over:
                current_time = time.time()
                if current_time - last_arrow_press_time <= arrow_press_time:
                    down_arrow_press_count += 1
                else:
                    down_arrow_press_count = 1
                last_arrow_press_time = current_time
                if down_arrow_press_count >= 10:
                    invincible = False
                    down_arrow_press_count = 0
            elif event.key == pygame.K_2 and not game_over:
                current_time = time.time()
                if not thunderbolt_active and (current_time - last_thunderbolt_time >= thunderbolt_cooldown):
                    thunderbolt_active = True
                    thunderbolt_start_time = current_time
                    last_thunderbolt_time = current_time
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                               pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                selected_slot = event.key - pygame.K_1

    if not game_over:
        # Handle key presses for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            wizard_x -= wizard_speed
        if keys[pygame.K_d]:
            wizard_x += wizard_speed
        if keys[pygame.K_w]:
            wizard_y -= wizard_speed
        if keys[pygame.K_s]:
            wizard_y += wizard_speed

        # Handle key presses for wand rotation
        if keys[pygame.K_LEFT]:
            wand_angle += 5
        if keys[pygame.K_RIGHT]:
            wand_angle -= 5

        # Keep the wizard within the screen boundaries
        wizard_x = max(wizard_size // 2, min(width - wizard_size // 2, wizard_x))
        wizard_y = max(wizard_size // 2, min(height - wizard_size // 2, wizard_y))

        # Update slash animation
        if current_slash > 0:
            current_slash -= 1

        # Update slash waves
        for wave in slash_waves:
            wave[0] += wave[2]
            wave[1] += wave[3]
            wave[4] -= 1
        slash_waves = [wave for wave in slash_waves if wave[4] > 0]

        # Spawn monsters
        current_time = time.time()
        if current_time - last_spawn_time >= spawn_interval and len(monsters) < max_monsters:
            for _ in range(monsters_to_spawn):
                monsters.append(create_monster())
            last_spawn_time = current_time
            monsters_to_spawn = min(monsters_to_spawn + 1, max_monsters)

        # Update monsters
        for monster in monsters:
            dx = wizard_x - monster[0]
            dy = wizard_y - monster[1]
            distance = math.hypot(dx, dy)
            if distance != 0:
                monster[0] += (dx / distance) * monster_speed
                monster[1] += (dy / distance) * monster_speed

            # Check for collision with wizard
            if not invincible and not thunderbolt_active:
                wizard_rect = pygame.Rect(wizard_x - wizard_size / 2, wizard_y - wizard_size / 2, wizard_size, wizard_size)
                monster_rect = pygame.Rect(monster[0] - monster_size / 2, monster[1] - monster_size / 2, monster_size, monster_size)
                if check_collision(wizard_rect, monster_rect):
                    game_over