
import pygame
import sys
from game_logic import GameState
from renderer import GameRenderer
from ui import UIManager

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Maze Game")
clock = pygame.time.Clock()

# Create game components
game_state = GameState()
renderer = GameRenderer(screen)
ui_manager = UIManager(screen)

# Game loop
running = True
while running:
    dt = clock.tick(15) / 1000  # Time since last frame in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:  # Toggle light
                game_state.toggle_light()
            elif event.key == pygame.K_r:  # Reset game
                game_state.reset_game()
                
    # Handle key presses - using get_pressed for more responsive controls
    keys = pygame.key.get_pressed()
    
    # Update game state
    game_state.update(keys, dt)
    
    # Render the game
    screen.fill((0, 0, 0))
    renderer.render_maze(game_state)
    ui_manager.render_ui(game_state)
    
    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
