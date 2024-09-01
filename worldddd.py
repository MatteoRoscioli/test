import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World's Hardest Game - Endless Edition")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
LAVENDER = (102, 102, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
LIME = (50, 205, 50)
MAGENTA = (255, 0, 255)

# Player
player_radius = 10
player_x = 100
player_y = HEIGHT // 2
player_speed = 5

# Room setup
room_width = WIDTH - 100
room_height = HEIGHT - 100
room_x = 50
room_y = 50

# Game state
lives = 3
fails = 0
collected_coins = 0
current_level = 1
difficulty_factor = 1.0
rounds_without_losing = 3

# Skins
skins = {
    'blue': {'color': BLUE, 'unlocked': True, 'requirement':'Default skin.'},
    'gold': {'color': GOLD, 'unlocked': False, 'requirement':'Play 5 rounds w/out losing.'},
    'purple': {'color': PURPLE, 'unlocked': False, 'requirement': 'Collect 50 coins.'},
    'orange': {'color': ORANGE, 'unlocked': False, 'requirement':'Complete 10 levels'},
    'pink': {'color': PINK, 'unlocked': False, 'requirement':'Collect 100 coins.'},
    'cyan': {'color': CYAN, 'unlocked': False, 'requirement':'Play 10 rounds w/out losing.'},
    'lime': {'color': LIME, 'unlocked': False, 'requirement':'Complete 20 levels.'},
    'magenta': {'color': MAGENTA, 'unlocked': False, 'requirement': 'Collect 200 coins.'}
}
current_skin = 'blue'

# Fonts
font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 36)

# Game states
MAIN_MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
SKINS_MENU = 4

game_state = MAIN_MENU

def draw_text(text, x, y, font=font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def reset_player():
    global player_x, player_y
    player_x, player_y = 100, HEIGHT // 2

def create_obstacles(num_obstacles, speed):
    obstacles = []
    square_size = 45
    quarter_inch = 15
    spacing = square_size + quarter_inch
    
    row1_y = room_y + room_height // 3
    row2_y = room_y + 2 * (room_height // 3)
    
    for i in range(num_obstacles):
        obstacles.append({
            'x': room_x + 150 + i * spacing,
            'y': row1_y,
            'dy': -speed
        })
        
        obstacles.append({
            'x': room_x + 150 + i * spacing,
            'y': row2_y,
            'dy': speed
        })
    
    return obstacles

def create_coins(num_coins):
    coins = []
    for _ in range(num_coins):
        coins.append({
            'x': random.randint(room_x + 50, room_x + room_width - 50),
            'y': random.randint(room_y + 50, room_y + room_height - 50)
        })
    return coins

def generate_level(difficulty):
    num_obstacles = min(13, 5 + difficulty // 2)
    obstacle_speed = min(10, 3 + difficulty * 0.5)
    num_coins = min(10, 2 + difficulty // 2)
    
    return {
        'obstacles': create_obstacles(num_obstacles, obstacle_speed),
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60},
        'coins': create_coins(num_coins)
    }

current_room = generate_level(current_level)
obstacle_size = 25
coin_radius = 5

def main_menu():
    screen.fill(WHITE)
    draw_text("World's Hardest Game - Endless Edition", WIDTH // 2 - 200, HEIGHT // 2 - 100, title_font)
    draw_text("Press SPACE to start", WIDTH // 2 - 100, HEIGHT // 2)
    draw_text("Press S for Skins", WIDTH // 2 - 80, HEIGHT // 2 + 50)

def skins_menu():
    screen.fill(WHITE)
    draw_text("Skins Menu", WIDTH // 2 - 50, 20, title_font)

    skins_per_row = 3
    skin_size = 30
    x_start = 30
    y_start = 80
    x_spacing = (WIDTH - 2 * x_start) // skins_per_row
    y_spacing = 150
    
    for i, (skin, data) in enumerate(skins.items()):
        row = i // skins_per_row
        col = i % skins_per_row
        x = x_start + col * x_spacing
        y = y_start + row * y_spacing
        
        # Draw skin circle
        pygame.draw.circle(screen, data['color'], (x + skin_size, y + skin_size), skin_size)
        
        # Draw skin name and status
        color = GREEN if data['unlocked'] else RED
        draw_text(f"{skin.capitalize()}: {'Unlocked' if data['unlocked'] else 'Locked'}", x, y + skin_size * 2 + 5, color=color)
        
        # Draw requirement (always visible)
        draw_text(f"Req: {data['requirement']}", x, y + skin_size * 2 + 25, color=BLACK)
    
    draw_text("Press 1-8 to select a skin (if unlocked)", WIDTH // 2 - 150, HEIGHT - 60)
    draw_text("Press ESC to return to main menu", WIDTH // 2 - 150, HEIGHT - 30)

def game_over():
    screen.fill(WHITE)
    draw_text("Game Over", WIDTH // 2 - 60, HEIGHT // 2 - 100, title_font)
    draw_text(f"Total Fails: {fails}", WIDTH // 2 - 70, HEIGHT // 2 - 50)
    draw_text(f"Levels Completed: {current_level - 1}", WIDTH // 2 - 100, HEIGHT // 2)
    draw_text(f"Coins Collected: {collected_coins}", WIDTH // 2 - 90, HEIGHT // 2 + 50)
    draw_text("Press SPACE to restart", WIDTH // 2 - 120, HEIGHT // 2 + 100)

def check_skin_unlocks():
    global skins
    if rounds_without_losing >= 5:
        skins['gold']['unlocked'] = True
    if collected_coins >= 50:
        skins['purple']['unlocked'] = True
    if current_level > 10:
        skins['orange']['unlocked'] = True
    if collected_coins >= 100:
        skins['pink']['unlocked'] = True
    if rounds_without_losing >= 10:
        skins['cyan']['unlocked'] = True
    if current_level > 20:
        skins['lime']['unlocked'] = True
    if collected_coins >= 200:
        skins['magenta']['unlocked'] = True

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MAIN_MENU:
                    game_state = PLAYING
                    reset_player()
                elif game_state == GAME_OVER:
                    game_state = MAIN_MENU
                    lives = 3
                    fails = 0
                    collected_coins = 0
                    current_level = 1
                    difficulty_factor = 1.0
                    rounds_without_losing = 0
                    current_room = generate_level(current_level)
            elif event.key == pygame.K_s and game_state == MAIN_MENU:
                game_state = SKINS_MENU
            elif event.key == pygame.K_ESCAPE:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING
                elif game_state == SKINS_MENU:
                    game_state = MAIN_MENU
            elif game_state == SKINS_MENU:
                if pygame.K_1 <= event.key <= pygame.K_8:
                    skin_index = event.key - pygame.K_1
                    skin_name = list(skins.keys())[skin_index]
                    if skins[skin_name]['unlocked']:
                        current_skin = skin_name

    if game_state == PLAYING:
        # Move player
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += player_speed

        # Check room boundaries and update player position
        player_x = max(room_x + player_radius, min(new_x, room_x + room_width - player_radius))
        player_y = max(room_y + player_radius, min(new_y, room_y + room_height - player_radius))

        # Move obstacles
        for obstacle in current_room['obstacles']:
            obstacle['y'] += obstacle['dy']
            
            if obstacle['y'] <= room_y or obstacle['y'] >= room_y + room_height - obstacle_size:
                obstacle['dy'] *= -1

        # Check for collisions
        player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
        for obstacle in current_room['obstacles']:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_size, obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                lives -= 1
                fails += 1
                rounds_without_losing = 0
                if lives <= 0:
                    game_state = GAME_OVER
                reset_player()

        # Check for coin collection
        for coin in current_room['coins'][:]:
            coin_rect = pygame.Rect(coin['x'] - coin_radius, coin['y'] - coin_radius, coin_radius * 2, coin_radius * 2)
            if player_rect.colliderect(coin_rect):
                current_room['coins'].remove(coin)
                collected_coins += 1
                check_skin_unlocks()

        # Check for exit
        exit_rect = pygame.Rect(
            current_room['exit']['x'],
            current_room['exit']['y'],
            current_room['exit']['width'],
            current_room['exit']['height']
        )
        if player_rect.colliderect(exit_rect):
            current_level += 1
            difficulty_factor += 0.1
            current_room = generate_level(current_level)
            reset_player()
            rounds_without_losing += 1
            check_skin_unlocks()

        # Draw everything
        screen.fill(WHITE)
        
        # Draw room
        pygame.draw.rect(screen, BLACK, (room_x, room_y, room_width, room_height), 2)
        
        # Draw player
        pygame.draw.circle(screen, skins[current_skin]['color'], (int(player_x), int(player_y)), player_radius)
        
        # Draw obstacles
        for obstacle in current_room['obstacles']:
            pygame.draw.rect(screen, RED, (obstacle['x'], obstacle['y'], obstacle_size, obstacle_size))
        
        # Draw coins
        for coin in current_room['coins']:
            pygame.draw.circle(screen, YELLOW, (coin['x'], coin['y']), coin_radius)
        
        # Draw exit
        pygame.draw.rect(screen, GREEN, (
            current_room['exit']['x'],
            current_room['exit']['y'],
            current_room['exit']['width'],
            current_room['exit']['height']
        ))

        # Draw HUD
        draw_text(f"Level: {current_level}", 10, 10)
        draw_text(f"Lives: {lives}", 10, 50)
        draw_text(f"Fails: {fails}", 10, 90)
        draw_text(f"Coins: {collected_coins}", 10, 130)
        draw_text(f"Rounds without losing: {rounds_without_losing}", 10, 170)

    elif game_state == MAIN_MENU:
        main_menu()
    elif game_state == SKINS_MENU:
        skins_menu()
    elif game_state == PAUSED:
        draw_text("PAUSED", WIDTH // 2 - 40, HEIGHT // 2, title_font)
        draw_text("Press ESC to resume", WIDTH // 2 - 100, HEIGHT // 2 + 50)
    elif game_state == GAME_OVER:
        game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()