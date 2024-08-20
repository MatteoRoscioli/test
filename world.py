import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World's Hardest Game - Enhanced Edition")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

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

# Function to create obstacles
def create_obstacles():
    obstacles = []
    square_size = 45  # Reduced size to fit 13 squares
    quarter_inch = 15  # Reduced spacing
    spacing = square_size + quarter_inch
    
    # Calculate starting y-positions for two rows
    row1_y = room_y + room_height // 3
    row2_y = room_y + 2 * (room_height // 3)
    
    for i in range(13):
        # Obstacle moving up
        obstacles.append({
            'x': room_x + 150 + i * spacing,  # Start further from the player
            'y': row1_y,
            'dy': -5,  # Increased speed
            'min_y': room_y + obstacle_size,  # Minimum y position
            'max_y': room_y + room_height - obstacle_size  # Maximum y position
        })
        
        # Obstacle moving down
        obstacles.append({
            'x': room_x + 150 + i * spacing,  # Start further from the player
            'y': row2_y,
            'dy': 5,  # Increased speed
            'min_y': room_y + obstacle_size,  # Minimum y position
            'max_y': room_y + room_height - obstacle_size  # Maximum y position
        })
    
    return obstacles

# In the game loop, replace the obstacle movement code with:
# Move obstacles
for obstacle in rooms[current_room]['obstacles']:
    obstacle['y'] += obstacle['dy']
    
    if obstacle['y'] <= obstacle['min_y'] or obstacle['y'] >= obstacle['max_y']:
        obstacle['dy'] *= -1
        obstacle['y'] = max(obstacle['min_y'], min(obstacle['y'], obstacle['max_y']))

# Rooms
rooms = [
    {
        'obstacles': create_obstacles(),
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60},
        'coins': [{'x': 300, 'y': 200}, {'x': 500, 'y': 400}]
    },
    {
        'obstacles': create_obstacles(),
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60},
        'coins': [{'x': 250, 'y': 150}, {'x': 550, 'y': 450}, {'x': 400, 'y': 300}]
    },
    {
        'obstacles': create_obstacles(),
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60},
        'coins': [{'x': 200, 'y': 200}, {'x': 400, 'y': 400}, {'x': 600, 'y': 200}, {'x': 300, 'y': 500}]
    }
]

current_room = 0
obstacle_size = 25  # Update obstacle size
coin_radius = 5

# Game state
lives = 3
fails = 0
collected_coins = 0
total_coins = sum(len(room['coins']) for room in rooms)

# Fonts
font = pygame.font.Font(None, 36)

# Game states
MAIN_MENU = 0
LEVEL_SELECT = 1
PLAYING = 2
PAUSED = 3
GAME_OVER = 4

game_state = MAIN_MENU

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def reset_player():
    global player_x, player_y, collected_coins
    player_x, player_y = 100, HEIGHT // 2
    collected_coins = 0
    for room in rooms:
        room['coins'] = [coin for coin in room['coins']]

def main_menu():
    screen.fill(WHITE)
    draw_text("World's Hardest Game Clone", WIDTH // 2 - 150, HEIGHT // 2 - 100)
    draw_text("Press SPACE to start", WIDTH // 2 - 100, HEIGHT // 2)
    draw_text("Press L for level select", WIDTH // 2 - 120, HEIGHT // 2 + 50)

def level_select():
    screen.fill(WHITE)
    draw_text("Level Select", WIDTH // 2 - 60, 50)
    for i in range(len(rooms)):
        draw_text(f"Level {i + 1}", WIDTH // 2 - 40, 150 + i * 50)

def game_over():
    screen.fill(WHITE)
    draw_text("Game Over", WIDTH // 2 - 60, HEIGHT // 2 - 50)
    draw_text(f"Total Fails: {fails}", WIDTH // 2 - 70, HEIGHT // 2 + 50)
    draw_text("Press SPACE to restart", WIDTH // 2 - 120, HEIGHT // 2 + 100)

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
                    current_room = 0
            elif event.key == pygame.K_l and game_state == MAIN_MENU:
                game_state = LEVEL_SELECT
            elif event.key == pygame.K_ESCAPE:
                if game_state == PLAYING:
                    game_state = PAUSED
                elif game_state == PAUSED:
                    game_state = PLAYING
            elif game_state == LEVEL_SELECT:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    current_room = int(event.unicode) - 1
                    game_state = PLAYING
                    reset_player()

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
        for obstacle in rooms[current_room]['obstacles']:
            obstacle['y'] += obstacle['dy']
            
            if obstacle['y'] <= room_y or obstacle['y'] >= room_y + room_height - obstacle_size:
                obstacle['dy'] *= -1

        # Check for collisions
        player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
        for obstacle in rooms[current_room]['obstacles']:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_size, obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                lives -= 1
                fails += 1
                if lives <= 0:
                    game_state = GAME_OVER
                reset_player()

        # Check for coin collection
        for coin in rooms[current_room]['coins'][:]:
            coin_rect = pygame.Rect(coin['x'] - coin_radius, coin['y'] - coin_radius, coin_radius * 2, coin_radius * 2)
            if player_rect.colliderect(coin_rect):
                rooms[current_room]['coins'].remove(coin)
                collected_coins += 1

        # Check for exit
        exit_rect = pygame.Rect(
            rooms[current_room]['exit']['x'],
            rooms[current_room]['exit']['y'],
            rooms[current_room]['exit']['width'],
            rooms[current_room]['exit']['height']
        )
        if player_rect.colliderect(exit_rect):
            current_room += 1
            if current_room >= len(rooms):
                print("Congratulations! You've completed all rooms!")
                running = False
            else:
                reset_player()

        # Draw everything
        screen.fill(WHITE)
        
        # Draw room
        pygame.draw.rect(screen, BLACK, (room_x, room_y, room_width, room_height), 2)
        
        # Draw player
        pygame.draw.circle(screen, BLUE, (int(player_x), int(player_y)), player_radius)
        
        # Draw obstacles
        for obstacle in rooms[current_room]['obstacles']:
            pygame.draw.rect(screen, RED, (obstacle['x'], obstacle['y'], obstacle_size, obstacle_size))
        
        # Draw coins
        for coin in rooms[current_room]['coins']:
            pygame.draw.circle(screen, YELLOW, (coin['x'], coin['y']), coin_radius)
        
        # Draw exit
        pygame.draw.rect(screen, GREEN, (
            rooms[current_room]['exit']['x'],
            rooms[current_room]['exit']['y'],
            rooms[current_room]['exit']['width'],
            rooms[current_room]['exit']['height']
        ))

        # Draw HUD
        draw_text(f"Room: {current_room + 1}", 10, 10)
        draw_text(f"Lives: {lives}", 10, 50)
        draw_text(f"Fails: {fails}", 10, 90)
        draw_text(f"Coins: {collected_coins}/{total_coins}", 10, 130)

    elif game_state == MAIN_MENU:
        main_menu()
    elif game_state == LEVEL_SELECT:
        level_select()
    elif game_state == PAUSED:
        draw_text("PAUSED", WIDTH // 2 - 40, HEIGHT // 2)
        draw_text("Press ESC to resume", WIDTH // 2 - 100, HEIGHT // 2 + 50)
    elif game_state == GAME_OVER:
        game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()