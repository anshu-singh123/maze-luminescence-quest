
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
ROWS, COLS = 15, 15
BLACK, WHITE, GREEN, RED, BLUE, YELLOW = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)
LIGHT_RADIUS = 120

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Generate a random maze using Depth-First Search algorithm
def generate_maze():
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    
    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
                maze[y + dy//2][x + dx//2] = 0
                carve_path(nx, ny)
    
    carve_path(1, 1)
    # Create entrance and exit
    maze[1][0] = 0  # Entrance
    maze[ROWS-2][COLS-1] = 0  # Exit
    return maze

# Game state
maze = generate_maze()
player_pos = [0, 1]
items = []
score = 0
light_on = True

# Place items randomly in the maze
for _ in range(5):
    while True:
        x, y = random.randint(1, COLS-2), random.randint(1, ROWS-2)
        if maze[y][x] == 0 and [x, y] != player_pos and [x, y] not in items:
            items.append([x, y])
            break

# Function to reset the game
def reset_game():
    global maze, player_pos, items, score
    maze = generate_maze()
    player_pos = [0, 1]
    items = []
    for _ in range(5):
        while True:
            x, y = random.randint(1, COLS-2), random.randint(1, ROWS-2)
            if maze[y][x] == 0 and [x, y] != player_pos and [x, y] not in items:
                items.append([x, y])
                break
    score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Handle key presses - using get_pressed for more responsive controls
    keys = pygame.key.get_pressed()
    
    # Player movement (limit movement rate with a small delay)
    x, y = player_pos
    if keys[pygame.K_UP] and y > 0 and maze[y-1][x] == 0:
        player_pos[1] -= 1
    elif keys[pygame.K_DOWN] and y < ROWS-1 and maze[y+1][x] == 0:
        player_pos[1] += 1
    elif keys[pygame.K_LEFT] and x > 0 and maze[y][x-1] == 0:
        player_pos[0] -= 1
    elif keys[pygame.K_RIGHT] and x < COLS-1 and maze[y][x+1] == 0:
        player_pos[0] += 1
        
    # Special key handling for one-time actions - using event loop for toggle actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:  # Toggle light
                light_on = not light_on
                print("Light toggled:", "ON" if light_on else "OFF")  # Debug message
            elif event.key == pygame.K_r:  # Reset game
                reset_game()
                print("Game reset")  # Debug message
    
    # Check if player collected an item
    if player_pos in items:
        items.remove(player_pos)
        score += 10
    
    # Check if player reached the exit
    if player_pos == [COLS-1, ROWS-2]:
        score += 50
        reset_game()
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Calculate offset to center the maze
    offset_x = (SCREEN_WIDTH - COLS * CELL_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - ROWS * CELL_SIZE) // 2
    
    # Create a surface for the lighting effect
    if light_on:
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        light_surface.fill((0, 0, 0, 200))  # Semi-transparent black
    
    # Draw the maze
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)
                
                # Apply lighting effect
                if light_on:
                    # Calculate distance from player
                    dx = (offset_x + x * CELL_SIZE + CELL_SIZE//2) - (offset_x + player_pos[0] * CELL_SIZE + CELL_SIZE//2)
                    dy = (offset_y + y * CELL_SIZE + CELL_SIZE//2) - (offset_y + player_pos[1] * CELL_SIZE + CELL_SIZE//2)
                    distance = (dx**2 + dy**2)**0.5
                    
                    # Only draw cells within light radius
                    if distance <= LIGHT_RADIUS:
                        # Cut out a circle from the light surface
                        pygame.draw.circle(light_surface, (0, 0, 0, 0), 
                                          (offset_x + player_pos[0] * CELL_SIZE + CELL_SIZE//2, 
                                           offset_y + player_pos[1] * CELL_SIZE + CELL_SIZE//2), 
                                          LIGHT_RADIUS)
    
    # Draw items
    for x, y in items:
        pygame.draw.rect(screen, YELLOW, (offset_x + x * CELL_SIZE + 10, offset_y + y * CELL_SIZE + 10, CELL_SIZE - 20, CELL_SIZE - 20))
    
    # Draw player
    pygame.draw.rect(screen, GREEN, (offset_x + player_pos[0] * CELL_SIZE + 5, offset_y + player_pos[1] * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
    
    # Draw exit
    pygame.draw.rect(screen, RED, (offset_x + (COLS-1) * CELL_SIZE + 5, offset_y + (ROWS-2) * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
    
    # Apply lighting effect
    if light_on:
        screen.blit(light_surface, (0, 0))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Draw instructions
    instructions = font.render("Arrow keys to move, L to toggle light, R to reset", True, WHITE)
    screen.blit(instructions, (20, SCREEN_HEIGHT - 40))
    
    # Draw current light status
    light_status = font.render(f"Light: {'ON' if light_on else 'OFF'}", True, WHITE)
    screen.blit(light_status, (20, 60))
    
    # Update the display
    pygame.display.flip()
    clock.tick(15)  # Lower FPS to make movement more manageable

pygame.quit()
sys.exit()
