
import pygame
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ROWS, COLS, LIGHT_RADIUS
from constants import BLACK, WHITE, GREEN, RED, BLUE, YELLOW, WALL_COLOR, PATH_COLOR

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.player_img = self.create_player_image()
        self.item_img = self.create_item_image()
        self.exit_img = self.create_exit_image()
        
        # Calculate offset to center the maze
        self.offset_x = (SCREEN_WIDTH - COLS * CELL_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - ROWS * CELL_SIZE) // 2
    
    def create_player_image(self):
        surface = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10), pygame.SRCALPHA)
        pygame.draw.circle(surface, GREEN, (CELL_SIZE//2-5, CELL_SIZE//2-5), CELL_SIZE//2-8)
        return surface
    
    def create_item_image(self):
        surface = pygame.Surface((CELL_SIZE-20, CELL_SIZE-20), pygame.SRCALPHA)
        pygame.draw.polygon(surface, YELLOW, [
            (CELL_SIZE//2-10, 5), 
            (CELL_SIZE//2-20, CELL_SIZE-25), 
            (CELL_SIZE//2-10, CELL_SIZE-30), 
            (CELL_SIZE//2, CELL_SIZE-25)
        ])
        return surface
    
    def create_exit_image(self):
        surface = pygame.Surface((CELL_SIZE-10, CELL_SIZE-10), pygame.SRCALPHA)
        pygame.draw.rect(surface, RED, (0, 0, CELL_SIZE-10, CELL_SIZE-10))
        pygame.draw.rect(surface, (255, 150, 150), (5, 5, CELL_SIZE-20, CELL_SIZE-20))
        return surface
        
    def render_maze(self, game_state):
        # Create a surface for the lighting effect
        if game_state.light_on:
            light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            light_surface.fill((0, 0, 0, 200))  # Semi-transparent black
        
        # Draw the maze with better visuals
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(self.offset_x + x * CELL_SIZE, self.offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if game_state.maze[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    # Add 3D effect to walls
                    pygame.draw.line(self.screen, (100, 100, 140), 
                                    (rect.left, rect.top), 
                                    (rect.right, rect.top), 2)
                    pygame.draw.line(self.screen, (100, 100, 140), 
                                    (rect.left, rect.top), 
                                    (rect.left, rect.bottom), 2)
                    pygame.draw.line(self.screen, (40, 40, 60), 
                                    (rect.right, rect.top), 
                                    (rect.right, rect.bottom), 2)
                    pygame.draw.line(self.screen, (40, 40, 60), 
                                    (rect.left, rect.bottom), 
                                    (rect.right, rect.bottom), 2)
                else:  # Path
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
                    pygame.draw.rect(self.screen, (40, 40, 60), rect, 1)  # Path border
                    
                # Apply lighting effect
                if game_state.light_on:
                    # Calculate distance from player
                    cell_center_x = self.offset_x + x * CELL_SIZE + CELL_SIZE//2
                    cell_center_y = self.offset_y + y * CELL_SIZE + CELL_SIZE//2
                    player_center_x = self.offset_x + game_state.player_pos[0] * CELL_SIZE + CELL_SIZE//2
                    player_center_y = self.offset_y + game_state.player_pos[1] * CELL_SIZE + CELL_SIZE//2
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
        for x, y in game_state.items:
            self.screen.blit(self.item_img, (self.offset_x + x * CELL_SIZE + 10, self.offset_y + y * CELL_SIZE + 10))
        
        # Draw collection effect (if active)
        if game_state.collected_timer > 0:
            effect_radius = int(50 * (1 - game_state.collected_timer))
            effect_alpha = int(200 * game_state.collected_timer)
            effect_surface = pygame.Surface((effect_radius*2, effect_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(effect_surface, (255, 255, 0, effect_alpha), (effect_radius, effect_radius), effect_radius)
            self.screen.blit(effect_surface, 
                      (self.offset_x + game_state.collected_effect[0] * CELL_SIZE + CELL_SIZE//2 - effect_radius,
                       self.offset_y + game_state.collected_effect[1] * CELL_SIZE + CELL_SIZE//2 - effect_radius))
        
        # Draw player with better visuals
        self.screen.blit(self.player_img, (self.offset_x + game_state.player_pos[0] * CELL_SIZE + 5, 
                                     self.offset_y + game_state.player_pos[1] * CELL_SIZE + 5))
        
        # Draw exit with better visuals
        self.screen.blit(self.exit_img, (self.offset_x + (COLS-1) * CELL_SIZE + 5, 
                                   self.offset_y + (ROWS-2) * CELL_SIZE + 5))
        
        # Apply lighting effect
        if game_state.light_on:
            self.screen.blit(light_surface, (0, 0))
