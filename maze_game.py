
import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
ROWS, COLS = 15, 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 220, 0)
WALL_COLOR = (70, 70, 100)
PATH_COLOR = (20, 20, 30)
LIGHT_RADIUS = 150

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

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

# Load images or create surfaces for game elements
def create_player_image():
    surface = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10), pygame.SRCALPHA)
    pygame.draw.circle(surface, GREEN, (CELL_SIZE//2-5, CELL_SIZE//2-5), CELL_SIZE//2-8)
    return surface

def create_item_image():
    surface = pygame.Surface((CELL_SIZE-20, CELL_SIZE-20), pygame.SRCALPHA)
    pygame.draw.polygon(surface, YELLOW, [
        (CELL_SIZE//2-10, 5), 
        (CELL_SIZE//2-20, CELL_SIZE-25), 
        (CELL_SIZE//2-10, CELL_SIZE-30), 
        (CELL_SIZE//2, CELL_SIZE-25)
    ])
    return surface

def create_exit_image():
    surface = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10), pygame.SRCALPHA)
    pygame.draw.rect(surface, RED, (0, 0, CELL_SIZE-10, CELL_SIZE-10))
    pygame.draw.rect(surface, (255, 150, 150), (5, 5, CELL_SIZE-20, CELL_SIZE-20))
    return surface

# Create images
player_img = create_player_image()
item_img = create_item_image()
exit_img = create_exit_image()

# Game state
maze = generate_maze()
player_pos = [0, 1]
items = []
score = 0
light_on = True
collected_effect = None
collected_timer = 0

# Place items randomly in the maze
for _ in range(5):
    while True:
        x, y = random.randint(1, COLS-2), random.randint(1, ROWS-2)
        if maze[y][x] == 0 and [x, y] != player_pos and [x, y] not in items:
            items.append([x, y])
            break

# Game loop
running = True
while running:
    dt = clock.tick(15) / 1000  # Time since last frame in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:  # Toggle light
                light_on = not light_on
            elif event.key == pygame.K_r:  # Reset game
                reset_game()
                
    # Handle key presses - using get_pressed for more responsive controls
    keys = pygame.key.get_pressed()
    
    # Player movement (limit movement rate)
    x, y = player_pos
    if keys[pygame.K_UP] and y > 0 and maze[y-1][x] == 0:
        player_pos[1] -= 1
    elif keys[pygame.K_DOWN] and y < ROWS-1 and maze[y+1][x] == 0:
        player_pos[1] += 1
    elif keys[pygame.K_LEFT] and x > 0 and maze[y][x-1] == 0:
        player_pos[0] -= 1
    elif keys[pygame.K_RIGHT] and x < COLS-1 and maze[y][x+1] == 0:
        player_pos[0] += 1
    
    # Check if player collected an item
    if player_pos in items:
        items.remove(player_pos)
        score += 10
        collected_effect = player_pos.copy()
        collected_timer = 1.0  # Effect duration in seconds
    
    # Update collection effect timer
    if collected_timer > 0:
        collected_timer -= dt
    
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
    
    # Draw the maze with better visuals
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:  # Wall
                pygame.draw.rect(screen, WALL_COLOR, rect)
                # Add 3D effect to walls
                pygame.draw.line(screen, (100, 100, 140), 
                                (rect.left, rect.top), 
                                (rect.right, rect.top), 2)
                pygame.draw.line(screen, (100, 100, 140), 
                                (rect.left, rect.top), 
                                (rect.left, rect.bottom), 2)
                pygame.draw.line(screen, (40, 40, 60), 
                                (rect.right, rect.top), 
                                (rect.right, rect.bottom), 2)
                pygame.draw.line(screen, (40, 40, 60), 
                                (rect.left, rect.bottom), 
                                (rect.right, rect.bottom), 2)
            else:  # Path
                pygame.draw.rect(screen, PATH_COLOR, rect)
                pygame.draw.rect(screen, (40, 40, 60), rect, 1)  # Path border
                
            # Apply lighting effect
            if light_on:
                # Calculate distance from player
                cell_center_x = offset_x + x * CELL_SIZE + CELL_SIZE//2
                cell_center_y = offset_y + y * CELL_SIZE + CELL_SIZE//2
                player_center_x = offset_x + player_pos[0] * CELL_SIZE + CELL_SIZE//2
                player_center_y = offset_y + player_pos[1] * CELL_SIZE + CELL_SIZE//2
                dx = cell_center_x - player_center_x
                dy = cell_center_y - player_center_y
                distance = math.sqrt(dx**2 + dy**2)
                
                # Only draw cells within light radius
                if distance <= LIGHT_RADIUS:
                    # Calculate the alpha value based on distance
                    alpha = int(200 * (1 - distance / LIGHT_RADIUS))
                    # Cut out a circle from the light surface at this cell's position
                    pygame.draw.rect(light_surface, (0, 0, 0, 200-alpha), rect)
    
    # Draw items with better visuals
    for x, y in items:
        screen.blit(item_img, (offset_x + x * CELL_SIZE + 10, offset_y + y * CELL_SIZE + 10))
    
    # Draw collection effect (if active)
    if collected_timer > 0:
        effect_radius = int(50 * (1 - collected_timer))
        effect_alpha = int(200 * collected_timer)
        effect_surface = pygame.Surface((effect_radius*2, effect_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(effect_surface, (255, 255, 0, effect_alpha), (effect_radius, effect_radius), effect_radius)
        screen.blit(effect_surface, 
                  (offset_x + collected_effect[0] * CELL_SIZE + CELL_SIZE//2 - effect_radius,
                   offset_y + collected_effect[1] * CELL_SIZE + CELL_SIZE//2 - effect_radius))
    
    # Draw player with better visuals
    screen.blit(player_img, (offset_x + player_pos[0] * CELL_SIZE + 5, offset_y + player_pos[1] * CELL_SIZE + 5))
    
    # Draw exit with better visuals
    screen.blit(exit_img, (offset_x + (COLS-1) * CELL_SIZE + 5, offset_y + (ROWS-2) * CELL_SIZE + 5))
    
    # Apply lighting effect
    if light_on:
        screen.blit(light_surface, (0, 0))
    
    # Draw UI with better visuals
    # Score display with background
    score_bg = pygame.Rect(10, 10, 150, 40)
    pygame.draw.rect(screen, (0, 0, 50, 150), score_bg, border_radius=5)
    pygame.draw.rect(screen, (100, 100, 200), score_bg, 2, border_radius=5)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Light status with background
    light_bg = pygame.Rect(10, 60, 150, 40)
    pygame.draw.rect(screen, (0, 0, 50, 150), light_bg, border_radius=5)
    pygame.draw.rect(screen, (100, 100, 200), light_bg, 2, border_radius=5)
    light_status = font.render(f"Light: {'ON' if light_on else 'OFF'}", True, WHITE)
    screen.blit(light_status, (20, 70))
    
    # Instructions with background
    instr_bg = pygame.Rect(10, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 20, 40)
    pygame.draw.rect(screen, (0, 0, 50, 150), instr_bg, border_radius=5)
    pygame.draw.rect(screen, (100, 100, 200), instr_bg, 2, border_radius=5)
    instructions = font.render("Arrow keys to move, L to toggle light, R to reset", True, WHITE)
    screen.blit(instructions, (20, SCREEN_HEIGHT - 40))
    
    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
