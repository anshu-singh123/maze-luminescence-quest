
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
    
    def render_ui(self, game_state):
        # Draw UI with better visuals
        # Score display with background
        score_bg = pygame.Rect(10, 10, 150, 40)
        pygame.draw.rect(self.screen, (0, 0, 50, 150), score_bg, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), score_bg, 2, border_radius=5)
        score_text = self.font.render(f"Score: {game_state.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Light status with background
        light_bg = pygame.Rect(10, 60, 150, 40)
        pygame.draw.rect(self.screen, (0, 0, 50, 150), light_bg, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), light_bg, 2, border_radius=5)
        light_status = self.font.render(f"Light: {'ON' if game_state.light_on else 'OFF'}", True, WHITE)
        self.screen.blit(light_status, (20, 70))
        
        # Instructions with background
        instr_bg = pygame.Rect(10, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 20, 40)
        pygame.draw.rect(self.screen, (0, 0, 50, 150), instr_bg, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), instr_bg, 2, border_radius=5)
        instructions = self.font.render("Arrow keys to move, L to toggle light, R to reset", True, WHITE)
        self.screen.blit(instructions, (20, SCREEN_HEIGHT - 40))
