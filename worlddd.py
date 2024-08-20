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