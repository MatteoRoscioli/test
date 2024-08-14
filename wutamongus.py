import random
import time

# ASCII art for game elements
spaceship = '''
    _____
   |     |
 .-'-----'-.
/           \
|           |
|           |
|           |
 \_________/
'''

crewmate = '''
 .----.
( o  o )
 )    (
(______)
'''

impostor = '''
 .----.
( >  < )
 )    (
(______)
'''

dead_body = '''
   ___
  (x_x)
  /|\\ 
  / \\
'''

# Game setup
num_players = 5
players = ['Crewmate' for _ in range(num_players - 1)] + ['Impostor']
random.shuffle(players)

# Game state
alive_players = list(range(num_players))
game_over = False

def print_game_state():
    print(spaceship)
    for i in alive_players:
        if players[i] == 'Impostor':
            print(f"Player {i + 1}: {impostor}")
        else:
            print(f"Player {i + 1}: {crewmate}")

def emergency_meeting():
    global alive_players, game_over
    print("\nEmergency Meeting!")
    print("Who do you think is the Impostor?")
    for i in alive_players:
        print(f"{i + 1}: Player {i + 1}")
    
    vote = int(input("Enter the number of the player you want to vote out: ")) - 1
    if vote in alive_players:
        alive_players.remove(vote)
        if players[vote] == 'Impostor':
            print(f"\nPlayer {vote + 1} was the Impostor. Crewmates win!")
            game_over = True
        else:
            print(f"\nPlayer {vote + 1} was not the Impostor. The game continues...")
    else:
        print("Invalid vote. No one was ejected.")

def impostor_kill():
    global alive_players, game_over
    if 'Impostor' not in [players[i] for i in alive_players]:
        return
    
    targets = [i for i in alive_players if players[i] != 'Impostor']
    if targets:
        victim = random.choice(targets)
        alive_players.remove(victim)
        print(f"\nOh no! Player {victim + 1} was killed!")
        print(dead_body)
        if len([p for p in alive_players if players[p] != 'Impostor']) <= 1:
            print("The Impostor has won!")
            game_over = True

# Main game loop
print("Welcome to Text Among Us!")
while not game_over:
    print_game_state()
    action = input("What would you like to do? (1: Call Emergency Meeting, 2: Skip): ")
    
    if action == '1':
        emergency_meeting()
    elif action == '2':
        print("Skipping...")
    else:
        print("Invalid action. Skipping...")
    
    if not game_over:
        impostor_kill()
    
    time.sleep(2)

print("Game Over!")