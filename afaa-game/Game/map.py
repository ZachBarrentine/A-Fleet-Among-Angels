import pygame
import json
import os
import sys

# ----------------- INITIALIZATION -----------------
pygame.init()

# ----------------- CONSTANTS -----------------
# --- Window ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
SIDEBAR_WIDTH = 300
# --- Grid ---
GRID_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH
GRID_HEIGHT = WINDOW_HEIGHT
TILE_SIZE = 32
GRID_COLS = GRID_WIDTH // TILE_SIZE
GRID_ROWS = GRID_HEIGHT // TILE_SIZE
# --- Colors ---
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_GRAY = (128, 128, 128)
C_LIGHT_GRAY = (200, 200, 200)
C_RED = (255, 0, 0)
C_GREEN = (0, 255, 0)
C_CYAN = (0, 255, 255)
C_YELLOW = (255, 255, 0)
C_PURPLE = (255, 0, 255)

# --- Paths ---
ASSET_DIR = "./afaa-game/Game/assets/tiles/"
LEVEL_DIR = "./afaa-game/Game/levels/"

# ----------------- TILE DEFINITIONS -----------------
# Defines properties for each tile, like walkability and special effects.
TILES = {
    0: {"name": "Empty", "file": None, "walkable": True, "effect": None},
    1: {"name": "Grass", "file": "Grass1.png", "walkable": True, "effect": None},
    2: {"name": "Brick", "file": "Brick.png", "walkable": False, "effect": None},
    3: {"name": "River", "file": "River.png", "walkable": False, "effect": None},
    4: {"name": "Metal", "file": "MetalFloor.png", "walkable": True, "effect": None},
    5: {"name": "Mountain", "file": "Mountains.png", "walkable": True, "effect": "slow"},
    6: {"name": "Bridge", "file": "Bridge.png", "walkable": True, "effect": None},
    7: {"name": "Forest", "file": "Forest.png", "walkable": True, "effect": "defense"},
    8: {"name": "Healing", "file": "Healing.png", "walkable": True, "effect": "heal"},
    9: {"name": "Lava", "file": "lava.png", "walkable": True, "effect": "damage"}
}

# ----------------- ASSET LOADING -----------------
def load_tile_images():
    """Loads and scales all tile images from the asset directory."""
    for tile_id, data in TILES.items():
        if data["file"]:
            path = os.path.join(ASSET_DIR, data["file"])
            try:
                img = pygame.image.load(path).convert_alpha()
                data["image"] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except Exception as e:
                print(f"✗ Failed to load {data['file']}: {e}")
                # Create a fallback colored surface if image fails to load
                fallback_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                fallback_surface.fill(C_PURPLE)
                data["image"] = fallback_surface
        else:
            # Create a white surface for the "Empty" tile
            empty_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            empty_surface.fill(C_WHITE)
            data["image"] = empty_surface

# ----------------- EDITOR CLASS -----------------
class TilemapEditor:
    """A Pygame application for creating and editing tilemaps."""
    def __init__(self):
        # --- Pygame Setup ---
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Level Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # --- Asset Loading ---
        load_tile_images()
        self.rotated_cache = {} # Cache for rotated images to improve performance
        
        # --- Editor State ---
        # The tilemap now stores a dictionary for each tile to include rotation
        self.tilemap = [[{'id': 0, 'rot': 0} for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.selected_tile_id = 1
        self.current_rotation = 0 # 0, 90, 180, 270 degrees
        self.is_painting = False
        self.is_erasing = False
        
        # --- UI Elements ---
        self.setup_ui()

    def setup_ui(self):
        """Initializes the positions and dimensions of UI buttons."""
        self.tile_buttons = []
        btn_size, margin = 45, 10
        start_x = GRID_WIDTH + 20
        start_y = 60
        
        # Create a button for each tile type (except Empty)
        for i, (tile_id, data) in enumerate(TILES.items()):
            if tile_id == 0: continue
            row, col = (i - 1) // 2, (i - 1) % 2
            x = start_x + col * (btn_size + margin + 70)
            y = start_y + row * (btn_size + margin)
            self.tile_buttons.append({'rect': pygame.Rect(x, y, btn_size, btn_size), 'id': tile_id})
        
        # Action buttons (Save, Load, etc.)
        y_offset = self.tile_buttons[-1]['rect'].bottom + 30
        self.eraser_btn = pygame.Rect(start_x, y_offset, 120, 40)
        self.save_btn = pygame.Rect(start_x + 130, y_offset, 120, 40)
        y_offset += 50
        self.load_btn = pygame.Rect(start_x, y_offset, 120, 40)
        self.clear_btn = pygame.Rect(start_x + 130, y_offset, 120, 40)

    def run(self):
        """The main loop of the editor."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
            
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_input(self, event):
        """Processes all user input from mouse and keyboard."""
        # --- Keyboard Input ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Rotate selected tile
                self.current_rotation = (self.current_rotation + 90) % 360
                self.rotated_cache.clear() # Clear cache when rotation changes

        # --- Mouse Input ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_painting = True
            self.handle_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_painting = False
        elif event.type == pygame.MOUSEMOTION and self.is_painting:
            self.paint_tile(event.pos)

    def handle_click(self, pos):
        """Handles a single mouse click on the grid or UI."""
        # Check if a UI button was clicked
        for btn in self.tile_buttons:
            if btn['rect'].collidepoint(pos):
                self.selected_tile_id = btn['id']
                self.is_erasing = False
                return

        if self.eraser_btn.collidepoint(pos): self.is_erasing = not self.is_erasing
        elif self.save_btn.collidepoint(pos): self.save_map()
        elif self.load_btn.collidepoint(pos): self.load_map()
        elif self.clear_btn.collidepoint(pos): self.clear_map()
        else:
            # If no UI element was clicked, paint on the grid
            self.paint_tile(pos)

    def paint_tile(self, pos):
        """Places or erases a tile on the grid at the given mouse position."""
        x, y = pos
        if x < GRID_WIDTH: # Only paint within the grid area
            col, row = x // TILE_SIZE, y // TILE_SIZE
            if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                if self.is_erasing:
                    self.tilemap[row][col] = {'id': 0, 'rot': 0}
                else:
                    self.tilemap[row][col] = {'id': self.selected_tile_id, 'rot': self.current_rotation}

    # ----------------- DRAW METHODS -----------------
    def draw(self):
        """Main drawing function, called every frame."""
        self.screen.fill(C_WHITE)
        self.draw_grid()
        self.draw_sidebar()
        pygame.display.flip()

    def draw_grid(self):
        """Draws the entire tilemap to the screen."""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                tile_info = self.tilemap[row][col]
                tile_id = tile_info.get('id', 0)
                tile_rot = tile_info.get('rot', 0)
                
                if tile_id in TILES:
                    base_img = TILES[tile_id]["image"]
                    
                    # Use cached rotated image if available, otherwise create and cache it
                    cache_key = (tile_id, tile_rot)
                    if cache_key not in self.rotated_cache:
                        self.rotated_cache[cache_key] = pygame.transform.rotate(base_img, tile_rot)
                    
                    final_img = self.rotated_cache[cache_key]
                    self.screen.blit(final_img, (col * TILE_SIZE, row * TILE_SIZE))
        
        # Draw grid lines over the tiles
        for x in range(0, GRID_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, C_LIGHT_GRAY, (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, C_LIGHT_GRAY, (0, y), (GRID_WIDTH, y))

    def draw_sidebar(self):
        """Draws the UI sidebar, including buttons and info text."""
        # --- Background ---
        pygame.draw.rect(self.screen, C_LIGHT_GRAY, (GRID_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(self.screen, C_BLACK, (GRID_WIDTH, 0), (GRID_WIDTH, WINDOW_HEIGHT), 2)
        
        # --- Title ---
        title = self.font.render("Level Editor", True, C_BLACK)
        self.screen.blit(title, (GRID_WIDTH + 20, 20))

        # --- Tile Selection Buttons ---
        for btn in self.tile_buttons:
            data = TILES[btn['id']]
            # Highlight selected tile
            if btn['id'] == self.selected_tile_id and not self.is_erasing:
                pygame.draw.rect(self.screen, C_YELLOW, btn['rect'].inflate(4, 4))
            
            self.screen.blit(data["image"], btn['rect'])
            pygame.draw.rect(self.screen, C_BLACK, btn['rect'], 1)
            
            # Text label for each button
            label = self.small_font.render(data['name'], True, C_BLACK)
            self.screen.blit(label, (btn['rect'].right + 8, btn['rect'].centery - 8))
        
        # --- Selected Tile Info & Rotation Preview ---
        info_y = self.tile_buttons[-1]['rect'].bottom + 80
        selected_data = TILES[self.selected_tile_id]
        
        # Draw rotated preview
        preview_key = (self.selected_tile_id, self.current_rotation)
        if preview_key not in self.rotated_cache:
            self.rotated_cache[preview_key] = pygame.transform.rotate(selected_data["image"], self.current_rotation)
        preview_img = pygame.transform.scale(self.rotated_cache[preview_key], (64, 64))
        self.screen.blit(preview_img, (GRID_WIDTH + 20, info_y - 20))
        
        # Info text
        text_x = GRID_WIDTH + 95
        name_text = self.font.render(f"{selected_data['name']}", True, C_BLACK)
        rot_text = self.font.render(f"Rotation: {self.current_rotation}° (R)", True, C_BLACK)
        self.screen.blit(name_text, (text_x, info_y))
        self.screen.blit(rot_text, (text_x, info_y + 25))

        # --- Action Buttons ---
        eraser_color = C_YELLOW if self.is_erasing else C_WHITE
        pygame.draw.rect(self.screen, eraser_color, self.eraser_btn)
        pygame.draw.rect(self.screen, C_BLACK, self.eraser_btn, 2)
        self.screen.blit(self.font.render("Eraser", True, C_BLACK), self.eraser_btn.move(35, 12))
        
        pygame.draw.rect(self.screen, C_GREEN, self.save_btn)
        pygame.draw.rect(self.screen, C_BLACK, self.save_btn, 2)
        self.screen.blit(self.font.render("Save", True, C_BLACK), self.save_btn.move(40, 12))

        pygame.draw.rect(self.screen, C_CYAN, self.load_btn)
        pygame.draw.rect(self.screen, C_BLACK, self.load_btn, 2)
        self.screen.blit(self.font.render("Load", True, C_BLACK), self.load_btn.move(40, 12))
        
        pygame.draw.rect(self.screen, C_RED, self.clear_btn)
        pygame.draw.rect(self.screen, C_BLACK, self.clear_btn, 2)
        self.screen.blit(self.font.render("Clear", True, C_BLACK), self.clear_btn.move(38, 12))

    # ----------------- FILE I/O -----------------
    def save_map(self):
        """Saves the current tilemap and its properties to a JSON file."""
        os.makedirs(LEVEL_DIR, exist_ok=True)
        
        # Find the next available level number to avoid overwriting
        existing_levels = [f for f in os.listdir(LEVEL_DIR) if f.startswith("level") and f.endswith(".json")]
        next_level_num = len(existing_levels)
        file_path = os.path.join(LEVEL_DIR, f"level{next_level_num}.json")
        
        map_data = {
            "tilemap": self.tilemap,
            "tile_properties": {
                str(k): {"walkable": v["walkable"], "effect": v["effect"]}
                for k, v in TILES.items()
            }
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(map_data, f, indent=2)
            print(f"✓ Map saved to {file_path}")
        except Exception as e:
            print(f"✗ Error saving map: {e}")

    def load_map(self):
        """Loads a tilemap from a JSON file."""
        # For simplicity, this loads the most recently saved level.
        os.makedirs(LEVEL_DIR, exist_ok=True)
        existing_levels = [f for f in os.listdir(LEVEL_DIR) if f.startswith("level") and f.endswith(".json")]
        if not existing_levels:
            print("✗ No levels found to load.")
            return

        latest_level_num = len(existing_levels) - 1
        file_path = os.path.join(LEVEL_DIR, f"level{latest_level_num}.json")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Basic validation to ensure the file has the expected structure
                if "tilemap" in data and isinstance(data["tilemap"], list):
                    self.tilemap = data["tilemap"]
                    # Clear cache as new map is loaded
                    self.rotated_cache.clear() 
                    print(f"✓ Map loaded from {file_path}")
                else:
                    print(f"✗ Invalid map format in {file_path}")
        except Exception as e:
            print(f"✗ Error loading map: {e}")

    def clear_map(self):
        """Resets the grid to be completely empty."""
        self.tilemap = [[{'id': 0, 'rot': 0} for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        print("✓ Map cleared.")


if __name__ == "__main__":
    editor = TilemapEditor()
    editor.run()