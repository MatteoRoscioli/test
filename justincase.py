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

# Key definitions
ESCAPE = pygame.K_ESCAPE

# Game loop
running = True
clock = pygame.time.Clock()

# Function definitions
def create_monster():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    lives = 3  # Each monster starts with 3 lives
    if side == 'top':
        return [random.randint(0, width), -monster_size // 2, 0, 0, lives]
    elif side == 'bottom':
        return [random.randint(0, width), height + monster_size // 2, 0, 0, lives]
    elif side == 'left':
        return [-monster_size // 2, random.randint(0, height), 0, 0, lives]
    else:  # right
        return [width + monster_size // 2, random.randint(0, height), 0, 0, lives]

def create_boss():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        return [random.randint(0, width), -boss_size // 2, boss_health]
    elif side == 'bottom':
        return [random.randint(0, width), height + boss_size // 2, boss_health]
    elif side == 'left':
        return [-boss_size // 2, random.randint(0, height), boss_health]
    else:  # right
        return [width + boss_size // 2, random.randint(0, height), boss_health]

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_wizard(screen, x, y, size):
    # Draw body
    pygame.draw.rect(screen, BLUE, (x - size // 4, y, size // 2, size // 2))
    # Draw head
    pygame.draw.circle(screen, SKIN, (x, y - size // 4), size // 4)
    # Draw hat
    pygame.draw.polygon(screen, PURPLE, [(x - size // 3, y - size // 4),
                                         (x + size // 3, y - size // 4),
                                         (x, y - size)])

def draw_wand(screen, x, y, angle):
    end_x = x + wand_length * math.cos(math.radians(angle))
    end_y = y - wand_length * math.sin(math.radians(angle))
    pygame.draw.line(screen, BROWN, (x, y), (end_x, end_y), 3)

def draw_monster(screen, x, y, size, lives):
    color = (max(0, 255 - 50 * (3 - lives)), 0, 0)  # Darker red as lives decrease
    pygame.draw.rect(screen, color, (x - size // 2, y - size // 2, size, size))
    # Draw eyes
    eye_size = size // 5
    pygame.draw.circle(screen, WHITE, (int(x - size // 4), int(y - size // 4)), eye_size)
    pygame.draw.circle(screen, WHITE, (int(x + size // 4), int(y - size // 4)), eye_size)
    pygame.draw.circle(screen, BLACK, (int(x - size // 4), int(y - size // 4)), eye_size // 2)
    pygame.draw.circle(screen, BLACK, (int(x + size // 4), int(y - size // 4)), eye_size // 2)
    
    # Draw lives
    font = pygame.font.SysFont(None, 20)
    lives_text = font.render(str(lives), True, WHITE)
    screen.blit(lives_text, (x - lives_text.get_width() // 2, y + size // 2 + 5))

def draw_boss(screen, x, y, size, health):
    pygame.draw.rect(screen, DARK_GRAY, (x - size // 2, y - size // 2, size, size))
    # Draw eyes
    eye_size = size // 4
    pygame.draw.circle(screen, RED, (int(x - size // 4), int(y - size // 4)), eye_size)
    pygame.draw.circle(screen, RED, (int(x + size // 4), int(y - size // 4)), eye_size)
    # Draw health bar
    health_width = int((health / boss_health) * size)
    pygame.draw.rect(screen, RED, (x - size // 2, y - size // 2 - 10, size, 5))
    pygame.draw.rect(screen, GREEN, (x - size // 2, y - size // 2 - 10, health_width, 5))

def create_slash_wave(x, y, angle):
    dx = wave_speed * math.cos(math.radians(angle))
    dy = -wave_speed * math.sin(math.radians(angle))
    return [x, y, dx, dy, wave_lifetime]

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and current_slash == 0 and not game_over:
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
            boss[2] = boss_health * round_number (1,2,3,4,5,6,7,8,9,10,2)  # Increase boss health each round

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
        for wave in slash_waves[:]:
            wave_rect = pygame.Rect(wave[0] - wave_length / 2, wave[1] - wave_width / 2, wave_length, wave_width)
            for monster in monsters[:]:
                monster_rect = pygame.Rect(monster[0] - monster_size / 2, monster[1] - monster_size / 2, monster_size, monster_size)
                if check_collision(wave_rect, monster_rect):
                    monster[4] -= 1  # Decrease monster lives
                    if monster[4] <= 0:
                        monsters.remove(monster)
                        kill_count += 1
                    slash_waves.remove(wave)
                    break  # Each wave can only hit one monster

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
                        monster[4] -= 2  # Thunderbolt does more damage
                        if monster[4] <= 0:
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

    # Draw spell effects
    for wave in slash_waves:
        wave_angle = math.atan2(-wave[3], wave[2])
        start_x = wave[0] - math.cos(wave_angle) * wave_length / 2
        start_y = wave[1] + math.sin(wave_angle) * wave_length / 2
        end_x = wave[0] + math.cos(wave_angle) * wave_length / 2
        end_y = wave[1] - math.sin(wave_angle) * wave_length / 2
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.line(screen, color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(wave_width * (wave[4] / wave_lifetime)))

    # Draw monsters
    for monster in monsters:
        draw_monster(screen, monster[0], monster[1], monster_size, monster[4])

    # Draw boss
    if boss is not None:
        draw_boss(screen, boss[0], boss[1], boss_size, boss[2])

    # Draw kill counter
    font = pygame.font.SysFont(None, 36)
    kill_text = font.render(f"Kills: {kill_count}", True, BLACK)
    screen.blit(kill_text, (10, 10))

    # Draw round number
    round_text = font.render(f"Round: {round_number}", True, BLACK)
    screen.blit(round_text, (10, 50))

    if game_over:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("Game Over", True, RED)
        retry_text = font.render("Press 'R' to try again", True, BLACK)
        screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2 - game_over_text.get_height()//2))
        screen.blit(retry_text, (width//2 - retry_text.get_width()//2, height//2 + game_over_text.get_height()))

    if invincible:
        invincible_text = font.render("Invincible!", True, GOLD)
        screen.blit(invincible_text, (width - invincible_text.get_width() - 10, 10))

    if thunderbolt_active:
        thunderbolt_text = font.render("Thunderbolt Active!", True, PURPLE)
        screen.blit(thunderbolt_text, (width - thunderbolt_text.get_width() - 10, 50))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()