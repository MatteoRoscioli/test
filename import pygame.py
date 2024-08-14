import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")

print(f"Pygame display size: {pygame.display.get_surface().get_size()}")  # Corrected debug print

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# Game variables
player_health = 100
pebble_health = 20
pebble_bite = -10

# Game states
INTRO = 0
INTRO_TEXT = 1
MAZE = 2
BATTLE = 3
OUT_OF_MAZE = 4

current_state = INTRO

# Function definitions remain the same
def draw_text(text, x, y, font=font, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def pebble_troll_attack():
    global player_health
    player_health += pebble_bite
    update_battle_text(f"Pebble Troll bit you for {-pebble_bite} damage!")

def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

battle_text = ""

def update_battle_text(text):
    global battle_text
    battle_text = text

def restart_game():
    global player_health, pebble_health, current_state
    player_health = 100
    pebble_health = 20
    current_state = BATTLE
    update_battle_text("")

# Intro text remains the same
intro_text = [
    "You spawn in your bed in the treehouse. You wake up and you see three lights floating around you.",
    "You get the crap scared out of you and quickly you grab your staff and run outside onto the front porch.",
    "You hear the lock click behind you.",
    "You suddenly remember you left the keys inside. So you decide to venture out in search of adventure.",
    "As you walk to the village gate, you realize that the gates were locked. A villager walks toward you and says,",
    "'So you're trying to get out of the village, huh? Well you can't. It is per the village regulation.",
    "No one can exit unless they defeat the Maze. The village leader said so himself!' As he walks away,",
    "you decide to go to the so called Maze.",
    "And this is where our story begins."
]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    print(f"Current state: {current_state}")  # Debug print
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and current_state == INTRO_TEXT:
            current_state = MAZE

    screen.fill(BLACK)
    
    # Force a simple draw operation
    pygame.draw.circle(screen, BLACK, (400, 300), 50)  # Draw a black circle

    if current_state == INTRO:
        print("Drawing INTRO screen")  # Debug print
        draw_text("MAZE ADVENTURE", WIDTH // 2 - 100, 50)
        draw_text("To skip, press SKIP. To continue, press CONTINUE.", WIDTH // 2 - 250, 100)

        def skip_intro():
            global current_state
            current_state = MAZE

        def continue_intro():
            global current_state
            current_state = INTRO_TEXT

        button_width = 200
        button_height = 50
        button_y = HEIGHT // 2

        button("SKIP", WIDTH // 2 - button_width - 20, button_y, button_width, button_height, (200, 200, 200), (150, 150, 150), skip_intro)
        button("CONTINUE", WIDTH // 2 + 20, button_y, button_width, button_height, (200, 200, 200), (150, 150, 150), continue_intro)

    elif current_state == INTRO_TEXT:
        print("Drawing INTRO_TEXT screen")  # Debug print
        y = 50
        for line in intro_text:
            wrapped_lines = wrap_text(line, small_font, WIDTH - 100)
            for wrapped_line in wrapped_lines:
                draw_text(wrapped_line, 50, y, small_font)
                y += 30
        draw_text("Press SPACE to continue", 300, 550)

    elif current_state == MAZE:
        print("Drawing MAZE screen")  # Debug print
        draw_text("You have found yourself inside the Maze.", 100, 50)
        draw_text("Which way do you go?", 100, 100)

        def go_left():
            global current_state
            current_state = BATTLE

        def go_right():
            global current_state
            current_state = OUT_OF_MAZE

        def go_straight():
            draw_text("You continue straight and find a mysterious door.", 100, 300)

        button("LEFT", 200, 200, 150, 50, (200, 200, 200), (150, 150, 150), go_left)
        button("RIGHT", 350, 200, 150, 50, (200, 200, 200), (150, 150, 150), go_right)
        button("STRAIGHT", 500, 200, 150, 50, (200, 200, 200), (150, 150, 150), go_straight)

    elif current_state == OUT_OF_MAZE:
        print("Drawing OUT_OF_MAZE screen")  # Debug print
        draw_text("Congratulations! You found a secret exit.", 100, 50)
        draw_text("You're out of the maze!", 100, 100)
        draw_text("You've successfully escaped the village.", 100, 150)
        draw_text("Your adventure continues beyond the village gates...", 100, 200)

        # You can add more descriptive text or even new gameplay options here
        # For example:
        draw_text("What would you like to do next?", 100, 300)

        def explore_forest():
            # Add functionality for exploring the forest
            pass

        def enter_nearby_town():
            # Add functionality for entering a nearby town
            pass

        button("EXPLORE FOREST", 200, 350, 200, 50, (200, 200, 200), (150, 150, 150), explore_forest)
        button("ENTER NEARBY TOWN", 450, 350, 200, 50, (200, 200, 200), (150, 150, 150), enter_nearby_town)

    elif current_state == BATTLE:
        print("Drawing BATTLE screen")  # Debug print
        draw_text("BATTLE WITH PEBBLE TROLLS", 250, 50)
        draw_text(f"Player Health: {player_health}", 100, 100)
        draw_text(f"Pebble Troll Health: {pebble_health}", 100, 150)

        def attack():
            global pebble_health
            damage = 5
            pebble_health -= damage
            update_battle_text(f"You dealt {damage} damage to the Pebble Troll!")
            pebble_troll_attack()

        def defend():
            global player_health
            heal_amount = 5
            player_health += heal_amount
            update_battle_text(f"You defended and healed {heal_amount} health.")
            pebble_troll_attack()

        button("ATTACK", 200, 250, 150, 50, (200, 200, 200), (150, 150, 150), attack)
        button("DEFEND", 400, 250, 150, 50, (200, 200, 200), (150, 150, 150), defend)

        draw_text(battle_text, 100, 350, small_font)

        if pebble_health <= 0:
            draw_text("You defeated the Pebble Troll!", 250, 400)
            button("CONTINUE", 325, 450, 150, 50, (200, 200, 200), (150, 150, 150), lambda: setattr(sys.modules[__name__], 'current_state', MAZE))
        elif player_health <= 0:
            draw_text("Game Over! The Pebble Troll defeated you.", 200, 400)
            button("RESTART", 325, 450, 150, 50, (200, 200, 200), (150, 150, 150), restart_game)

    player_health = max(player_health, 0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()