import pygame
import sys
import math
import random
import time

# Load background images
alley_background = pygame.image.load("alley_background.png")
alley_wall_left = pygame.image.load("alley_wall_left.png")
alley_wall_right = pygame.image.load("alley_wall_right.png")
alley_floor = pygame.image.load("alley_floor.png")

# Set the size of the alley
alley_width = 600
alley_height = 400
alley_x = (800 - alley_width) // 2
alley_y = (600 - alley_height) // 2

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

