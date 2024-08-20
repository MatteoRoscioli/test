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
    pygame.draw.line(surface, PURPLE, (int(x - 10), int(y - thunderbolt_radius + 20)), (int(x + 10), int(y - thunderbolt_radius + 20)), 5)
    pygame.draw.line(surface, PURPLE, (int(x - 10), int(y + thunderbolt_radius - 20)), (int(x + 10), int(y + thunderbolt_radius - 20)), 5)
    pygame.draw.line(surface, PURPLE, (int(x - 20), int(y - thunderbolt_radius + 40)), (int(x + 20), int(y - thunderbolt_radius + 40)), 5)

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
            current_time = time.time()
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

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the wizard
    draw_wizard(screen, wizard_x, wizard_y, wizard_size)

    # Draw the wand
    if current_slash == 0:
        draw_wand(screen, wizard_x + wizard_size // 2, wizard_y - wizard_size // 4, wand_angle)
    else:
        # Animate the spell cast
        slash_progress = (slash_duration - current_slash) / slash_duration
        current_angle = wand_angle - (slash_angle / 2) + (slash_angle * slash_progress)
        draw_wand(screen, wizard_x + wizard_size // 2, wizard_y - wizard_size // 4, current_angle)

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
        draw_monster(screen, monster[0], monster[1], monster_size)

    # Draw kill counter
    font = pygame.font.SysFont(None, 36)
    kill_text = font.render(f"Kills: {kill_count}", True, BLACK)
    screen.blit(kill_text, (10, 10))
    font = pygame.font.SysFont(None, 36)
    high_score_text = font.render(f"High Score:" )
    if game_over:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("Game Over", True, RED)
        retry_text = font.render("Press 'R' to try again", True, BLACK)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        screen.blit(retry_text, (width // 2 - retry_text.get_width() // 2, height // 2 + game_over_text.get_height()))
        high_score = max(high_score, kill_count)
        high_score_font = pygame.font.SysFont(None, 72)
        high_score_text = high_score_font.render("High Score = " + str(high_score), True, RED)
        screen.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, height // 3 - high_score_text.get_height() // 2))

    if invincible:
        invincible_text = font.render("Invincible!", True, GOLD)
        screen.blit(invincible_text, (width - invincible_text.get_width() - 10, 10))

    if thunderbolt_active:
        thunderbolt_text = font.render("Thunderbolt Active!", True, PURPLE)
        screen.blit(thunderbolt_text, (width - thunderbolt_text.get_width() - 10, 50))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()