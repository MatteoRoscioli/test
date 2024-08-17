import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World's Hardest Game Clone - Room Edition")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player
player_size = 20
player_x = 50
player_y = HEIGHT // 2
player_speed = 5

# Room setup
room_width = WIDTH - 100
room_height = HEIGHT - 100
room_x = 50
room_y = 50

# Rooms
rooms = [
    {
        'obstacles': [
            {'x': 200, 'y': 100, 'dx': 3, 'dy': 3},
            {'x': 400, 'y': 300, 'dx': -3, 'dy': 3},
        ],
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60}
    },
    {
        'obstacles': [
            {'x': 300, 'y': 200, 'dx': 4, 'dy': 0},
            {'x': 500, 'y': 400, 'dx': -4, 'dy': 0},
            {'x': 200, 'y': 300, 'dx': 0, 'dy': 4},
        ],
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60}
    },
    {
        'obstacles': [
            {'x': 200, 'y': 100, 'dx': 5, 'dy': 5},
            {'x': 400, 'y': 300, 'dx': -5, 'dy': 5},
            {'x': 600, 'y': 500, 'dx': 5, 'dy': -5},
            {'x': 300, 'y': 200, 'dx': -5, 'dy': -5},
        ],
        'exit': {'x': room_x + room_width - 30, 'y': room_y + room_height // 2 - 30, 'width': 30, 'height': 60}
    }
]

current_room = 0
obstacle_size = 15

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed

    # Check room boundaries
    if (room_x < new_x < room_x + room_width - player_size and
        room_y < new_y < room_y + room_height - player_size):
        player_x, player_y = new_x, new_y

    # Move obstacles
    for obstacle in rooms[current_room]['obstacles']:
        obstacle['x'] += obstacle['dx']
        obstacle['y'] += obstacle['dy']
        
        if obstacle['x'] <= room_x or obstacle['x'] >= room_x + room_width - obstacle_size:
            obstacle['dx'] *= -1
        if obstacle['y'] <= room_y or obstacle['y'] >= room_y + room_height - obstacle_size:
            obstacle['dy'] *= -1

    # Check for collisions
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for obstacle in rooms[current_room]['obstacles']:
        obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_size, obstacle_size)
        if player_rect.colliderect(obstacle_rect):
            player_x, player_y = 50, HEIGHT // 2  # Reset player position

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
            player_x, player_y = 50, HEIGHT // 2  # Reset player position for next room

    # Draw everything
    screen.fill(WHITE)
    
    # Draw room
    pygame.draw.rect(screen, BLACK, (room_x, room_y, room_width, room_height), 2)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    
    # Draw obstacles
    for obstacle in rooms[current_room]['obstacles']:
        pygame.draw.rect(screen, RED, (obstacle['x'], obstacle['y'], obstacle_size, obstacle_size))
    
    # Draw exit
    pygame.draw.rect(screen, GREEN, (
        rooms[current_room]['exit']['x'],
        rooms[current_room]['exit']['y'],
        rooms[current_room]['exit']['width'],
        rooms[current_room]['exit']['height']
    ))

    # Draw room number
    font = pygame.font.Font(None, 36)
    room_text = font.render(f"Room {current_room + 1}", True, BLACK)
    screen.blit(room_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()