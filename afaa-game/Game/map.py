import pygame
import json
import os
import sys

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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Asset path
ASSET_DIR = "./afaa-game/Game/assets/tiles/"

# Tile definitions (images will be loaded later)
TILES = {
    0: {"name": "Empty", "color": WHITE, "file": None},
    1: {"name": "Grass", "color": GREEN, "file": "Grass1.png"},
    2: {"name": "Brick", "color": GRAY, "file": "Brick.png"},
    3: {"name": "River", "color": CYAN, "file": "River.png"},
    4: {"name": "Metal", "color": YELLOW, "file": "MetalFloor.png"},
    5: {"name": "Mountain", "color": (139, 69, 19), "file": "Mountains.png"},
    6: {"name": "Bridge", "color": (64, 64, 64), "file": "Bridge.png"},
}


def load_tile_images():
    """Load all tile images after display is initialized"""
    for tile_id, tile_data in TILES.items():
        if tile_data["file"]:
            path = os.path.join(ASSET_DIR, tile_data["file"])
            try:
                img = pygame.image.load(path).convert_alpha()
                tile_data["image"] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                print(f"✓ Loaded {tile_data['name']}")
            except Exception as e:
                print(f"✗ Failed to load {tile_data['file']}: {e}")
                # Create colored placeholder
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(tile_data["color"])
                tile_data["image"] = surf
        else:
            # Empty tile
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(tile_data["color"])
            tile_data["image"] = surf


class TilemapEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tilemap Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)
        
        # NOW load the images after display is set
        load_tile_images()
        
        self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
        self.selected_tile = 1
        self.eraser_mode = False
        self.mouse_pressed = False
        
        self.setup_ui()

    def setup_ui(self):
        """Create UI buttons"""
        self.tile_buttons = []
        btn_size = 60
        btn_margin = 10
        start_x = GRID_WIDTH + 20
        start_y = 50
        
        # Create tile selection buttons
        for i, (tile_id, tile_data) in enumerate(TILES.items()):
            if tile_id == 0:
                continue
            row = (i - 1) // 3
            col = (i - 1) % 3
            x = start_x + col * (btn_size + btn_margin)
            y = start_y + row * (btn_size + btn_margin)
            
            self.tile_buttons.append({
                'rect': pygame.Rect(x, y, btn_size, btn_size),
                'tile_id': tile_id,
                'name': tile_data['name']
            })
        
        # Action buttons
        y_offset = start_y + 4 * (btn_size + btn_margin)
        self.eraser_btn = pygame.Rect(start_x, y_offset, 100, 40)
        y_offset += 50
        self.save_btn = pygame.Rect(start_x, y_offset, 100, 40)
        y_offset += 50
        self.load_btn = pygame.Rect(start_x, y_offset, 100, 40)
        y_offset += 50
        self.clear_btn = pygame.Rect(start_x, y_offset, 100, 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pressed = True
                self.handle_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_pressed = False
            elif event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                self.paint_tile(event.pos)
        return True

    def handle_click(self, pos):
        """Handle mouse clicks on UI elements"""
        # Check tile buttons
        for btn in self.tile_buttons:
            if btn['rect'].collidepoint(pos):
                self.selected_tile = btn['tile_id']
                self.eraser_mode = False
                return
        
        # Check action buttons
        if self.eraser_btn.collidepoint(pos):
            self.eraser_mode = True
        elif self.save_btn.collidepoint(pos):
            self.save_map()
        elif self.load_btn.collidepoint(pos):
            self.load_map()
        elif self.clear_btn.collidepoint(pos):
            self.clear_map()
        else:
            self.paint_tile(pos)

    def paint_tile(self, pos):
        """Paint tile at mouse position"""
        x, y = pos
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            col = x // TILE_SIZE
            row = y // TILE_SIZE
            self.tilemap[row][col] = 0 if self.eraser_mode else self.selected_tile

    def save_map(self):
        try:
            with open("map.json", 'w') as f:
                json.dump(self.tilemap, f, indent=2)
            print("✓ Map saved to map.json")
        except Exception as e:
            print(f"✗ Error saving map: {e}")

    def load_map(self):
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    self.tilemap = json.load(f)
                print("✓ Map loaded from map.json")
            else:
                print("✗ No map.json file found")
        except Exception as e:
            print(f"✗ Error loading map: {e}")

    def clear_map(self):
        self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
        print("✓ Map cleared")

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_sidebar()
        pygame.display.flip()

    def draw_grid(self):
        """Draw the tilemap grid"""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                tile_id = self.tilemap[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                # Draw tile image
                tile_img = TILES[tile_id]["image"]
                self.screen.blit(tile_img, (x, y))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, (200, 200, 200), 
                               (x, y, TILE_SIZE, TILE_SIZE), 1)

    def draw_sidebar(self):
        """Draw the sidebar UI"""
        # Background
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (GRID_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(self.screen, BLACK, 
                        (GRID_WIDTH, 0), (GRID_WIDTH, WINDOW_HEIGHT), 2)
        
        # Title
        title = self.font.render("Tilemap Editor", True, BLACK)
        self.screen.blit(title, (GRID_WIDTH + 20, 10))
        
        # Tile buttons
        for btn in self.tile_buttons:
            tile_img = TILES[btn['tile_id']]["image"]
            
            # Highlight selected tile
            if btn['tile_id'] == self.selected_tile and not self.eraser_mode:
                pygame.draw.rect(self.screen, YELLOW, btn['rect'].inflate(6, 6))
            
            # Draw tile preview
            preview = pygame.transform.scale(tile_img, (btn['rect'].width, btn['rect'].height))
            self.screen.blit(preview, btn['rect'])
            pygame.draw.rect(self.screen, BLACK, btn['rect'], 2)
            
            # Label
            label = self.small_font.render(btn['name'], True, BLACK)
            label_pos = (btn['rect'].centerx - label.get_width() // 2, 
                        btn['rect'].bottom + 5)
            self.screen.blit(label, label_pos)
        
        # Eraser button
        eraser_color = RED if self.eraser_mode else WHITE
        if self.eraser_mode:
            pygame.draw.rect(self.screen, YELLOW, self.eraser_btn.inflate(6, 6))
        pygame.draw.rect(self.screen, eraser_color, self.eraser_btn)
        pygame.draw.rect(self.screen, BLACK, self.eraser_btn, 2)
        text = self.font.render("Eraser", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.eraser_btn.center))
        
        # Save button
        pygame.draw.rect(self.screen, GREEN, self.save_btn)
        pygame.draw.rect(self.screen, BLACK, self.save_btn, 2)
        text = self.font.render("Save", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.save_btn.center))
        
        # Load button
        pygame.draw.rect(self.screen, CYAN, self.load_btn)
        pygame.draw.rect(self.screen, BLACK, self.load_btn, 2)
        text = self.font.render("Load", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.load_btn.center))
        
        # Clear button
        pygame.draw.rect(self.screen, YELLOW, self.clear_btn)
        pygame.draw.rect(self.screen, BLACK, self.clear_btn, 2)
        text = self.font.render("Clear", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.clear_btn.center))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        pygame.display.set_caption("Game - Tilemap Viewer")
        self.clock = pygame.time.Clock()
        
        # Load images after display is set
        load_tile_images()
        
        self.tilemap = None
        self.player_pos = [1, 1]
        self.player_color = PURPLE
        self.load_map()

    def load_map(self):
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    self.tilemap = json.load(f)
                print("✓ Game: Map loaded")
            else:
                print("✗ Game: No map.json found")
                self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
        except Exception as e:
            print(f"✗ Game: Error loading map: {e}")
            self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.player_pos[0] > 0:
                    self.player_pos[0] -= 1
                elif event.key == pygame.K_RIGHT and self.player_pos[0] < GRID_COLS - 1:
                    self.player_pos[0] += 1
                elif event.key == pygame.K_UP and self.player_pos[1] > 0:
                    self.player_pos[1] -= 1
                elif event.key == pygame.K_DOWN and self.player_pos[1] < GRID_ROWS - 1:
                    self.player_pos[1] += 1
                elif event.key == pygame.K_r:
                    self.load_map()
        return True

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw tilemap
        if self.tilemap:
            for row in range(len(self.tilemap)):
                for col in range(len(self.tilemap[0])):
                    tile_id = self.tilemap[row][col]
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    
                    tile_img = TILES[tile_id]["image"]
                    self.screen.blit(tile_img, (x, y))
        
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
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        game = Game()
        game.run()
    else:
        editor = TilemapEditor()
        editor.run()