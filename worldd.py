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
    square_size = 25  # Size of each square
    spacing = 40  # Increased spacing between squares
    
    # Calculate starting y-positions for two rows
    row1_y = room_y + room_height // 3
    row2_y = room_y + 2 * (room_height // 3)
    
    for i in range(13):
        # Obstacle moving up
        obstacles.append({
            'x': room_x + 150 + i * (square_size + spacing),  # Increased spacing
            'y': row1_y,
            'dy': -5  # Speed
        })
        
        # Obstacle moving down
        obstacles.append({
            'x': room_x + 150 + i * (square_size + spacing),  # Increased spacing
            'y': row2_y,
            'dy': 5  # Speed
        })
    
    return obstacles

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
obstacle_size = 25  # Size of obstacles
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

# ... (rest of the code remains unchanged)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # ... (game loop code remains unchanged)

 pygame.quit()
sys.exit()