import pygame
import json
import os
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
GRID_WIDTH = 700
GRID_HEIGHT = 700
SIDEBAR_WIDTH = 300
TILE_SIZE = 32
GRID_COLS = GRID_WIDTH // TILE_SIZE
GRID_ROWS = GRID_HEIGHT // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Tile types with colors (can be replaced with images later)
TILE_TYPES = {
    0: {"name": "Empty", "color": WHITE},
    1: {"name": "Grass", "color": GREEN},
    2: {"name": "Stone", "color": GRAY},
    3: {"name": "Water", "color": BLUE},
    4: {"name": "Sand", "color": YELLOW},
    5: {"name": "Wood", "color": BROWN},
    6: {"name": "Metal", "color": DARK_GRAY},
    7: {"name": "Lava", "color": RED},
    8: {"name": "Ice", "color": CYAN}
}

class TilemapEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tilemap Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Initialize tilemap
        self.tilemap = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        
        # Current selected tile
        self.selected_tile = 1
        self.eraser_mode = False
        
        # UI elements
        self.tile_buttons = []
        self.create_ui_elements()
        
        # Mouse state
        self.mouse_pressed = False
        
    def create_ui_elements(self):
        """Create UI buttons for tile selection"""
        button_width = 80
        button_height = 40
        button_margin = 10
        start_x = GRID_WIDTH + 20
        start_y = 50
        
        # Create tile selection buttons
        for i, (tile_id, tile_data) in enumerate(TILE_TYPES.items()):
            if tile_id == 0:  # Skip empty tile for selection
                continue
            
            row = (i - 1) // 3
            col = (i - 1) % 3
            
            x = start_x + col * (button_width + button_margin)
            y = start_y + row * (button_height + button_margin)
            
            button_rect = pygame.Rect(x, y, button_width, button_height)
            self.tile_buttons.append({
                'rect': button_rect,
                'tile_id': tile_id,
                'color': tile_data['color'],
                'name': tile_data['name']
            })
        
        # Eraser button
        eraser_y = start_y + 4 * (button_height + button_margin)
        self.eraser_button = pygame.Rect(start_x, eraser_y, button_width, button_height)
        
        # Save/Load buttons
        save_y = eraser_y + button_height + button_margin
        load_y = save_y + button_height + button_margin
        
        self.save_button = pygame.Rect(start_x, save_y, button_width, button_height)
        self.load_button = pygame.Rect(start_x, load_y, button_width, button_height)
        
        # Clear button
        clear_y = load_y + button_height + button_margin
        self.clear_button = pygame.Rect(start_x, clear_y, button_width, button_height)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_pressed = True
                    self.handle_click(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    self.mouse_pressed = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.handle_grid_paint(event.pos)
        
        return True
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        x, y = pos
        
        # Check tile selection buttons
        for button in self.tile_buttons:
            if button['rect'].collidepoint(pos):
                self.selected_tile = button['tile_id']
                self.eraser_mode = False
                return
        
        # Check eraser button
        if self.eraser_button.collidepoint(pos):
            self.eraser_mode = True
            return
        
        # Check save button
        if self.save_button.collidepoint(pos):
            self.save_map()
            return
        
        # Check load button
        if self.load_button.collidepoint(pos):
            self.load_map()
            return
        
        # Check clear button
        if self.clear_button.collidepoint(pos):
            self.clear_map()
            return
        
        # Handle grid painting
        self.handle_grid_paint(pos)
    
    def handle_grid_paint(self, pos):
        """Handle painting on the grid"""
        x, y = pos
        
        # Check if click is within grid area
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            
            if 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS:
                if self.eraser_mode:
                    self.tilemap[grid_y][grid_x] = 0
                else:
                    self.tilemap[grid_y][grid_x] = self.selected_tile
    
    def save_map(self):
        """Save the current tilemap to a JSON file"""
        try:
            tilemap_data = {"tilemap": {}}
            
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    tile_id = self.tilemap[row][col]
                    if tile_id != 0:  # Only save non-empty tiles
                        key = f"{col};{row}"
                        tile_name = TILE_TYPES[tile_id]['name'].lower()
                        tilemap_data["tilemap"][key] = {
                            "type": tile_name,
                            "variant": 1,  # Default variant
                            "pos": [col, row]
                        }
            
            with open('map.json', 'w') as f:
                json.dump(tilemap_data, f, indent=2)
            print("Map saved to map.json")
        except Exception as e:
            print(f"Error saving map: {e}")
    
    def load_map(self):
        """Load a tilemap from a JSON file"""
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    data = json.load(f)
                    self.tilemap = data['tilemap']
                print("Map loaded from map.json")
            else:
                print("No map.json file found")
        except Exception as e:
            print(f"Error loading map: {e}")
    
    def clear_map(self):
        """Clear the entire tilemap"""
        self.tilemap = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        print("Map cleared")
    
    def draw_grid(self):
        """Draw the tilemap grid"""
        # Draw tiles
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                tile_id = self.tilemap[row][col]
                color = TILE_TYPES[tile_id]['color']
                
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def draw_sidebar(self):
        """Draw the sidebar with tools and buttons"""
        # Draw sidebar background
        sidebar_rect = pygame.Rect(GRID_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, sidebar_rect)
        pygame.draw.line(self.screen, BLACK, (GRID_WIDTH, 0), (GRID_WIDTH, WINDOW_HEIGHT), 2)
        
        # Draw title
        title_text = self.font.render("Tilemap Editor", True, BLACK)
        self.screen.blit(title_text, (GRID_WIDTH + 20, 10))
        
        # Draw tile selection buttons
        for button in self.tile_buttons:
            # Highlight selected tile
            color = button['color']
            if button['tile_id'] == self.selected_tile and not self.eraser_mode:
                pygame.draw.rect(self.screen, BLACK, button['rect'], 3)
            
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, BLACK, button['rect'], 2)
            
            # Draw tile name
            text = pygame.font.Font(None, 16).render(button['name'], True, BLACK)
            text_rect = text.get_rect(center=(button['rect'].centerx, button['rect'].bottom + 10))
            self.screen.blit(text, text_rect)
        
        # Draw eraser button
        eraser_color = RED if self.eraser_mode else WHITE
        if self.eraser_mode:
            pygame.draw.rect(self.screen, BLACK, self.eraser_button, 3)
        
        pygame.draw.rect(self.screen, eraser_color, self.eraser_button)
        pygame.draw.rect(self.screen, BLACK, self.eraser_button, 2)
        
        eraser_text = self.font.render("Eraser", True, BLACK)
        eraser_text_rect = eraser_text.get_rect(center=self.eraser_button.center)
        self.screen.blit(eraser_text, eraser_text_rect)
        
        # Draw save button
        pygame.draw.rect(self.screen, GREEN, self.save_button)
        pygame.draw.rect(self.screen, BLACK, self.save_button, 2)
        
        save_text = self.font.render("Save", True, BLACK)
        save_text_rect = save_text.get_rect(center=self.save_button.center)
        self.screen.blit(save_text, save_text_rect)
        
        # Draw load button
        pygame.draw.rect(self.screen, CYAN, self.load_button)
        pygame.draw.rect(self.screen, BLACK, self.load_button, 2)
        
        load_text = self.font.render("Load", True, BLACK)
        load_text_rect = load_text.get_rect(center=self.load_button.center)
        self.screen.blit(load_text, load_text_rect)
        
        # Draw clear button
        pygame.draw.rect(self.screen, YELLOW, self.clear_button)
        pygame.draw.rect(self.screen, BLACK, self.clear_button, 2)
        
        clear_text = self.font.render("Clear", True, BLACK)
        clear_text_rect = clear_text.get_rect(center=self.clear_button.center)
        self.screen.blit(clear_text, clear_text_rect)
        
        # Draw instructions
        instructions = [
            "Instructions:",
            "• Click tiles to select",
            "• Click on grid to paint",
            "• Hold and drag to paint",
            "• Use eraser to remove",
            "• Save/Load your maps",
            "",
            f"Grid: {GRID_COLS}x{GRID_ROWS}",
            f"Tile size: {TILE_SIZE}px"
        ]
        
        start_y = 450
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 20).render(instruction, True, BLACK)
            self.screen.blit(text, (GRID_WIDTH + 20, start_y + i * 25))
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            
            # Clear screen
            self.screen.fill(WHITE)
            
            # Draw everything
            self.draw_grid()
            self.draw_sidebar()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Game class to use the saved tilemap
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        pygame.display.set_caption("Game - Using Saved Tilemap")
        self.clock = pygame.time.Clock()
        self.tilemap = None
        self.load_map()
        
        # Simple player
        self.player_pos = [1, 1]  # Grid position
        self.player_color = PURPLE
        
    def load_map(self):
        """Load the tilemap from JSON file"""
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    data = json.load(f)
                    self.tilemap = data['tilemap']
                print("Game: Map loaded successfully")
            else:
                print("Game: No map.json found, creating empty map")
                self.tilemap = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        except Exception as e:
            print(f"Game: Error loading map: {e}")
            self.tilemap = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Simple player movement
                if event.key == pygame.K_LEFT and self.player_pos[0] > 0:
                    self.player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and self.player_pos[0] < GRID_COLS - 1:
                    self.player_pos[0] += 1
                elif event.key == pygame.K_UP and self.player_pos[1] > 0:
                    self.player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and self.player_pos[1] < GRID_ROWS - 1:
                    self.player_pos[1] += 1
                elif event.key == pygame.K_r:  # Reload map
                    self.load_map()
        
        return True
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(WHITE)
        
        # Draw tilemap
        if self.tilemap:
            for row in range(len(self.tilemap)):
                for col in range(len(self.tilemap[0])):
                    tile_id = self.tilemap[row][col]
                    color = TILE_TYPES[tile_id]['color']
                    
                    rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
        
        # Draw player
        player_rect = pygame.Rect(
            self.player_pos[0] * TILE_SIZE + 4,
            self.player_pos[1] * TILE_SIZE + 4,
            TILE_SIZE - 8,
            TILE_SIZE - 8
        )
        pygame.draw.rect(self.screen, self.player_color, player_rect)
        pygame.draw.rect(self.screen, BLACK, player_rect, 2)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        # Run the game
        game = Game()
        game.run()
    else:
        # Run the tilemap editor
        editor = TilemapEditor()
        editor.run()