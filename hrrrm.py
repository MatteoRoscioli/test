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

# Boss properties
boss = None
boss_size = 100
boss_speed = 1
boss_health = 100
boss_spawn_interval = 60  # seconds
last_boss_spawn_time = time.time()
boss_attack_interval = 3  # seconds
last_boss_attack_time = time.time()

# Kill counter
kill_count = 0

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

# Round properties
round_number = 1
monsters_per_round = 10
boss_defeated = False

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
SKIN = (255, 224, 189)
PURPLE = (128, 0, 128)

# Game loop
running = True
clock = pygame.time.Clock()

# Added functions
def create_slash_wave(x, y, angle):
    rad_angle = math.radians(angle)
    dx = math.cos(rad_angle) * wave_speed
    dy = -math.sin(rad_angle) * wave_speed
    return [x, y, dx, dy, wave_lifetime]

def create_monster():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, width)
        y = -monster_size
    elif side == "bottom":
        x = random.randint(0, width)
        y = height + monster_size
    elif side == "left":
        x = -monster_size
        y = random.randint(0, height)
    else:  # right
        x = width + monster_size
        y = random.randint(0, height)
    return [x, y]

def create_boss():
    x = random.choice([-boss_size, width + boss_size])
    y = random.randint(0, height)
    return [x, y, boss_health]

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_wizard(screen, x, y, size):
    pygame.draw.circle(screen, SKIN, (int(x), int(y)), size // 2)
    pygame.draw.rect(screen, BLACK, (int(x - size // 4), int(y - size // 4), size // 2, size // 2))

def draw_wand(screen, x, y, angle):
    end_x = x + math.cos(math.radians(angle)) * wand_length
    end_y = y - math.sin(math.radians(angle)) * wand_length
    pygame.draw.line(screen, BROWN, (int(x), int(y)), (int(end_x), int(end_y)), 3)

def draw_monster(screen, x, y, size):
    pygame.draw.circle(screen, GREEN, (int(x), int(y)), size // 2)

def draw_boss(screen, x, y, size, health):
    pygame.draw.circle(screen, RED, (int(x), int(y)), size // 2)
    health_width = int((health / boss_health) * size)
    pygame.draw.rect(screen, GREEN, (int(x - size // 2), int(y - size // 2 - 10), health_width, 5))

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                boss = None
                kill_count = 0
                game_over = False
                last_spawn_time = time.time()
                monsters_to_spawn = 1
                invincible = False
                thunderbolt_active = False
                up_arrow_press_count = 0
                down_arrow_press_count = 0
                round_number = 1
                monsters_per_round = 10
                boss_defeated = False
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
        wizard_x = max(wizard_size//2, min(width - wizard_size//2, wizard_x))
        wizard_y = max(wizard_size//2, min(height - wizard_size//2, wizard_y))

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
        if len(monsters) == 0 and boss is None:
            if boss_defeated:
                # Start a new round
                round_number += 1
                monsters_per_round += 5  # Increase difficulty each round
                boss_defeated = False
            
            if len(monsters) < monsters_per_round:
                monsters.append(create_monster())
        
        # Spawn boss when all monsters are defeated
        if len(monsters) == 0 and boss is None and not boss_defeated:
            boss = create_boss()
            boss[2] = boss_health * round_number  # Increase boss health each round

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
                wizard_rect = pygame.Rect(wizard_x - wizard_size/2, wizard_y - wizard_size/2, wizard_size, wizard_size)
                monster_rect = pygame.Rect(monster[0] - monster_size/2, monster[1] - monster_size/2, monster_size, monster_size)
                if check_collision(wizard_rect, monster_rect):
                    game_over = True

        # Check for collisions between slash waves and monsters
        for wave in slash_waves:
            wave_rect = pygame.Rect(wave[0] - wave_length / 2, wave[1] - wave_width / 2, wave_length, wave_width)
            for monster in monsters[:]:
                monster_rect = pygame.Rect(monster[0] - monster_size / 2, monster[1] - monster_size / 2, monster_size, monster_size)
                if check_collision(wave_rect, monster_rect):
                    monsters.remove(monster)
                    kill_count += 1

        # Update thunderbolt status
        if thunderbolt_active:
            if current_time - thunderbolt_start_time >= thunderbolt_duration:
                thunderbolt_active = False
            else:
                # Thunderbolt effect
                pygame.draw.circle(screen, PURPLE, (int(wizard_x), int(wizard_y)), thunderbolt_radius, 2)
                # Check for collisions between thunderbolt and monsters
                for monster in monsters[:]:
                    monster_rect = pygame.Rect(monster[0] - monster_size / 2, monster[1] - monster_size / 2, monster_size, monster_size)
                    thunderbolt_rect = pygame.Rect(wizard_x - thunderbolt_radius, wizard_y - thunderbolt_radius, thunderbolt_radius * 2, thunderbolt_radius * 2)
                    if check_collision(thunderbolt_rect, monster_rect):
                        monsters.remove(monster)
                        kill_count += 1

        # Boss movement and attacks
        if boss is not None:
            dx = wizard_x - boss[0]
            dy = wizard_y - boss[1]
            distance = math.hypot(dx, dy)
            if distance != 0:
                boss[0] += (dx / distance) * boss_speed
                boss[1] += (dy / distance) * boss_speed

            # Boss attacks
            if current_time - last_boss_attack_time >= boss_attack_interval:
                angle = math.atan2(dy, dx)
                slash_waves.append(create_slash_wave(boss[0], boss[1], math.degrees(angle)))
                last_boss_attack_time = current_time

            # Check for collision with wizard
            if not invincible and not thunderbolt_active:
                wizard_rect = pygame.Rect(wizard_x - wizard_size/2, wizard_y - wizard_size/2, wizard_size, wizard_size)
                boss_rect = pygame.Rect(boss[0] - boss_size/2, boss[1] - boss_size/2, boss_size, boss_size)
                if check_collision(wizard_rect, boss_rect):
                    game_over = True

            # Check for collisions between slash waves and boss
            boss_rect = pygame.Rect(boss[0] - boss_size/2, boss[1] - boss_size/2, boss_size, boss_size)
            for wave in slash_waves[:]:
                wave_rect = pygame.Rect(wave[0] - wave_length/2, wave[1] - wave_width/2, wave_length, wave_width)
                if check_collision(wave_rect, boss_rect):
                    boss[2] -= 10  # Decrease boss health
                    slash_waves.remove(wave)
                    if boss[2] <= 0:
                        boss = None
                        kill_count += 10 * round_number  # More points for defeating the boss, scaled by round
                        boss_defeated = True

        # Thunderbolt effect on boss
        if thunderbolt_active and boss is not None:
            boss_rect = pygame.Rect(boss[0] - boss_size/2, boss[1] - boss_size/2, boss_size, boss_size)
            thunderbolt_rect = pygame.Rect(wizard_x - thunderbolt_radius, wizard_y - thunderbolt_radius, thunderbolt_radius*2, thunderbolt_radius*2)
            if check_collision(thunderbolt_rect, boss_rect):
                boss[2] -= 20  # Decrease boss health more with thunderbolt
                if boss[2] <= 0:
                    boss = None
                    kill_count += 10 * round_number  # More points for defeating the boss, scaled by round
                    boss_defeated = True

    # Drawing
    screen.fill(WHITE)

    # Draw the wizard
    draw_wizard(screen, wizard_x, wizard_y, wizard_size)
    
    # Draw the wand
    if current_slash == 0:
        draw_wand(screen, wizard_x + wizard_size//2, wizard_y - wizard_size//4, wand_angle)
    else:
        # Animate the spell cast
        slash_progress = (slash_duration - current_slash) / slash_duration
        current_angle = wand_angle - (slash_angle / 2) + (slash_angle * slash_progress)
        draw_wand(screen, wizard_x + wizard_size//2, wizard_y - wizard_size//4, current_angle)
