
import pygame
import random
from constants import ROWS, COLS

class GameState:
    def __init__(self):
        self.maze = self.generate_maze()
        self.player_pos = [0, 1]
        self.items = []
        self.score = 0
        self.light_on = True
        self.collected_effect = None
        self.collected_timer = 0
        
        # Place items randomly in the maze
        self.place_items(5)
    
    def generate_maze(self):
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
    
    def place_items(self, num_items):
        self.items = []
        for _ in range(num_items):
            while True:
                x, y = random.randint(1, COLS-2), random.randint(1, ROWS-2)
                if self.maze[y][x] == 0 and [x, y] != self.player_pos and [x, y] not in self.items:
                    self.items.append([x, y])
                    break
    
    def reset_game(self):
        self.maze = self.generate_maze()
        self.player_pos = [0, 1]
        self.items = []
        self.score = 0
        self.place_items(5)
    
    def toggle_light(self):
        self.light_on = not self.light_on
    
    def update(self, keys, dt):
        # Player movement
        x, y = self.player_pos
        if keys[pygame.K_UP] and y > 0 and self.maze[y-1][x] == 0:
            self.player_pos[1] -= 1
        elif keys[pygame.K_DOWN] and y < ROWS-1 and self.maze[y+1][x] == 0:
            self.player_pos[1] += 1
        elif keys[pygame.K_LEFT] and x > 0 and self.maze[y][x-1] == 0:
            self.player_pos[0] -= 1
        elif keys[pygame.K_RIGHT] and x < COLS-1 and self.maze[y][x+1] == 0:
            self.player_pos[0] += 1
        
        # Check if player collected an item
        if self.player_pos in self.items:
            self.items.remove(self.player_pos)
            self.score += 10
            self.collected_effect = self.player_pos.copy()
            self.collected_timer = 1.0  # Effect duration in seconds
        
        # Update collection effect timer
        if self.collected_timer > 0:
            self.collected_timer -= dt
        
        # Check if player reached the exit
        if self.player_pos == [COLS-1, ROWS-2]:
            self.score += 50
            self.reset_game()
