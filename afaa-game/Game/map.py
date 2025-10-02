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

# Tile definitions with properties
TILES = {
    0: {
        "name": "Empty",
        "color": WHITE,
        "file": None,
        "walkable": True,
        "effect": None
    },
    1: {
        "name": "Grass",
        "color": GREEN,
        "file": "Grass1.png",
        "walkable": True,
        "effect": None
    },
    2: {
        "name": "Brick",
        "color": GRAY,
        "file": "Brick.png",
        "walkable": False,  # Wall/obstacle
        "effect": None
    },
    3: {
        "name": "River",
        "color": CYAN,
        "file": "River.png",
        "walkable": False,  # Can't walk through water
        "effect": None
    },
    4: {
        "name": "Metal",
        "color": YELLOW,
        "file": "MetalFloor.png",
        "walkable": True,
        "effect": None
    },
    5: {
        "name": "Mountain",
        "color": (139, 69, 19),
        "file": "Mountains.png",
        "walkable": True,
        "effect": "slow"  # Reduces movement speed
    },
    6: {
        "name": "Bridge",
        "color": (64, 64, 64),
        "file": "Bridge.png",
        "walkable": True,
        "effect": None
    },
    7: {
        "name": "Forest",
        "color": (34, 139, 34),
        "file": None,
        "walkable": True,
        "effect": "defense"  # Reduces damage taken
    },
    8: {
        "name": "Healing",
        "color": (255, 182, 193),
        "file": None,
        "walkable": True,
        "effect": "heal"  # Provides healing
    },
    9: {
        "name": "Lava",
        "color": (255, 69, 0),
        "file": None,
        "walkable": True,
        "effect": "damage"  # Deals damage
    }
}

# Terrain effect descriptions
TERRAIN_EFFECTS = {
    "slow": {"desc": "Slow Movement", "color": (139, 69, 19)},
    "defense": {"desc": "Damage Reduction", "color": (34, 139, 34)},
    "heal": {"desc": "Healing", "color": (255, 182, 193)},
    "damage": {"desc": "Damage", "color": (255, 69, 0)}
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
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(tile_data["color"])
                tile_data["image"] = surf
        else:
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(tile_data["color"])
            tile_data["image"] = surf


class TilemapEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tilemap Editor - Terrain Effects")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 16)
        self.tiny_font = pygame.font.Font(None, 14)
        
        load_tile_images()
        
        self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
        self.selected_tile = 1
        self.eraser_mode = False
        self.mouse_pressed = False
        self.show_properties = True
        
        self.setup_ui()

    def setup_ui(self):
        """Create UI buttons"""
        self.tile_buttons = []
        btn_size = 50
        btn_margin = 8
        start_x = GRID_WIDTH + 15
        start_y = 50
        
        # Create tile selection buttons (2 columns)
        for i, (tile_id, tile_data) in enumerate(TILES.items()):
            if tile_id == 0:
                continue
            row = (i - 1) // 2
            col = (i - 1) % 2
            x = start_x + col * (btn_size + btn_margin + 50)
            y = start_y + row * (btn_size + btn_margin)
            
            self.tile_buttons.append({
                'rect': pygame.Rect(x, y, btn_size, btn_size),
                'tile_id': tile_id,
                'name': tile_data['name']
            })
        
        # Action buttons
        y_offset = start_y + 6 * (btn_size + btn_margin)
        self.eraser_btn = pygame.Rect(start_x, y_offset, 100, 35)
        y_offset += 45
        self.save_btn = pygame.Rect(start_x, y_offset, 100, 35)
        y_offset += 45
        self.load_btn = pygame.Rect(start_x, y_offset, 100, 35)
        y_offset += 45
        self.clear_btn = pygame.Rect(start_x, y_offset, 100, 35)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.show_properties = not self.show_properties
        return True

    def handle_click(self, pos):
        """Handle mouse clicks on UI elements"""
        for btn in self.tile_buttons:
            if btn['rect'].collidepoint(pos):
                self.selected_tile = btn['tile_id']
                self.eraser_mode = False
                return
        
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
        # Only paint if within grid bounds
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            col = x // TILE_SIZE
            row = y // TILE_SIZE
            # Double check indices are valid (prevents any edge case crashes)
            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                self.tilemap[row][col] = 0 if self.eraser_mode else self.selected_tile

    def save_map(self):
        dir_path = "./afaa-game/Game/levels/"
        os.makedirs(dir_path, exist_ok=True)
        
        all_lvls = [f for f in os.listdir(dir_path) if f.startswith("level") and f.endswith(".json")]
        num_lvls = len(all_lvls)
        
        file_path = f"{dir_path}level{num_lvls}.json"
        
        # Save map with tile properties
        map_data = {
            "tilemap": self.tilemap,
            "tile_properties": {
                str(k): {
                    "walkable": v["walkable"],
                    "effect": v["effect"]
                } for k, v in TILES.items()
            }
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(map_data, f, indent=2)
            print(f"✓ Map saved to {file_path}")
        except Exception as e:
            print(f"✗ Error saving map: {e}")

    def load_map(self):
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "tilemap" in data:
                        self.tilemap = data["tilemap"]
                    else:
                        self.tilemap = data
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
                
                tile_img = TILES[tile_id]["image"]
                self.screen.blit(tile_img, (x, y))
                
                # Draw property indicators if enabled
                if self.show_properties and tile_id != 0:
                    tile_data = TILES[tile_id]
                    
                    # Red X for non-walkable tiles
                    if not tile_data["walkable"]:
                        pygame.draw.line(self.screen, RED, 
                                       (x + 2, y + 2), 
                                       (x + TILE_SIZE - 2, y + TILE_SIZE - 2), 3)
                        pygame.draw.line(self.screen, RED, 
                                       (x + TILE_SIZE - 2, y + 2), 
                                       (x + 2, y + TILE_SIZE - 2), 3)
                    
                    # Effect indicator
                    if tile_data["effect"]:
                        effect_color = TERRAIN_EFFECTS[tile_data["effect"]]["color"]
                        pygame.draw.circle(self.screen, effect_color, 
                                         (x + TILE_SIZE - 8, y + 8), 5)
                
                pygame.draw.rect(self.screen, (200, 200, 200), 
                               (x, y, TILE_SIZE, TILE_SIZE), 1)

    def draw_sidebar(self):
        """Draw the sidebar UI"""
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (GRID_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(self.screen, BLACK, 
                        (GRID_WIDTH, 0), (GRID_WIDTH, WINDOW_HEIGHT), 2)
        
        title = self.font.render("Terrain Editor", True, BLACK)
        self.screen.blit(title, (GRID_WIDTH + 15, 10))
        
        # Tile buttons with properties
        for btn in self.tile_buttons:
            tile_data = TILES[btn['tile_id']]
            tile_img = tile_data["image"]
            
            if btn['tile_id'] == self.selected_tile and not self.eraser_mode:
                pygame.draw.rect(self.screen, YELLOW, btn['rect'].inflate(6, 6))
            
            preview = pygame.transform.scale(tile_img, (btn['rect'].width, btn['rect'].height))
            self.screen.blit(preview, btn['rect'])
            pygame.draw.rect(self.screen, BLACK, btn['rect'], 2)
            
            # Property indicators on button
            if not tile_data["walkable"]:
                pygame.draw.line(self.screen, RED, 
                               btn['rect'].topleft, btn['rect'].bottomright, 2)
            
            if tile_data["effect"]:
                effect_color = TERRAIN_EFFECTS[tile_data["effect"]]["color"]
                pygame.draw.circle(self.screen, effect_color, 
                                 (btn['rect'].right - 5, btn['rect'].top + 5), 4)
            
            # Label
            label = self.tiny_font.render(btn['name'], True, BLACK)
            self.screen.blit(label, (btn['rect'].right + 5, btn['rect'].top))
            
            # Effect text
            if tile_data["effect"]:
                effect_text = self.tiny_font.render(
                    TERRAIN_EFFECTS[tile_data["effect"]]["desc"], True, BLACK)
                self.screen.blit(effect_text, (btn['rect'].right + 5, btn['rect'].top + 12))
        
        # Action buttons
        eraser_color = RED if self.eraser_mode else WHITE
        if self.eraser_mode:
            pygame.draw.rect(self.screen, YELLOW, self.eraser_btn.inflate(6, 6))
        pygame.draw.rect(self.screen, eraser_color, self.eraser_btn)
        pygame.draw.rect(self.screen, BLACK, self.eraser_btn, 2)
        text = self.font.render("Eraser", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.eraser_btn.center))
        
        pygame.draw.rect(self.screen, GREEN, self.save_btn)
        pygame.draw.rect(self.screen, BLACK, self.save_btn, 2)
        text = self.font.render("Save", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.save_btn.center))
        
        pygame.draw.rect(self.screen, CYAN, self.load_btn)
        pygame.draw.rect(self.screen, BLACK, self.load_btn, 2)
        text = self.font.render("Load", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.load_btn.center))
        
        pygame.draw.rect(self.screen, YELLOW, self.clear_btn)
        pygame.draw.rect(self.screen, BLACK, self.clear_btn, 2)
        text = self.font.render("Clear", True, BLACK)
        self.screen.blit(text, text.get_rect(center=self.clear_btn.center))
        
        # Legend
        legend_y = self.clear_btn.bottom + 20
        legend = self.tiny_font.render("Legend:", True, BLACK)
        self.screen.blit(legend, (GRID_WIDTH + 15, legend_y))
        
        legend_y += 20
        legend_text = self.tiny_font.render("Red X = Obstacle", True, RED)
        self.screen.blit(legend_text, (GRID_WIDTH + 15, legend_y))
        
        legend_y += 15
        legend_text = self.tiny_font.render("Circle = Effect", True, BLACK)
        self.screen.blit(legend_text, (GRID_WIDTH + 15, legend_y))
        
        legend_y += 15
        legend_text = self.tiny_font.render("Press P to toggle", True, BLACK)
        self.screen.blit(legend_text, (GRID_WIDTH + 15, legend_y))

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
        pygame.display.set_caption("Game - Terrain Effects Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        load_tile_images()
        
        self.tilemap = None
        self.player_pos = [1, 1]
        self.player_color = PURPLE
        self.player_health = 100
        self.max_health = 100
        self.move_cooldown = 0
        self.status_message = ""
        self.status_timer = 0
        
        self.load_map()

    def load_map(self):
        try:
            if os.path.exists('map.json'):
                with open('map.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "tilemap" in data:
                        self.tilemap = data["tilemap"]
                    else:
                        self.tilemap = data
                print("✓ Game: Map loaded")
            else:
                print("✗ Game: No map.json found")
                self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]
        except Exception as e:
            print(f"✗ Game: Error loading map: {e}")
            self.tilemap = [[0] * GRID_COLS for _ in range(GRID_ROWS)]

    def can_move_to(self, col, row):
        """Check if player can move to this tile"""
        if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
            return False
        
        tile_id = self.tilemap[row][col]
        return TILES[tile_id]["walkable"]

    def apply_terrain_effect(self):
        """Apply effect of current terrain tile"""
        col, row = self.player_pos
        tile_id = self.tilemap[row][col]
        effect = TILES[tile_id]["effect"]
        
        if effect == "heal":
            if self.player_health < self.max_health:
                self.player_health = min(self.max_health, self.player_health + 5)
                self.set_status("Healing! +5 HP", GREEN)
        
        elif effect == "damage":
            self.player_health = max(0, self.player_health - 3)
            self.set_status("Taking damage! -3 HP", RED)
        
        elif effect == "slow":
            self.move_cooldown = 20  # Slower movement
            self.set_status("Movement slowed by terrain", (139, 69, 19))
        
        elif effect == "defense":
            self.set_status("Protected by forest cover", (34, 139, 34))

    def set_status(self, message, color):
        """Set status message with timer"""
        self.status_message = message
        self.status_color = color
        self.status_timer = 120  # Show for 2 seconds at 60 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.move_cooldown > 0:
                    continue
                
                new_pos = self.player_pos.copy()
                
                if event.key == pygame.K_LEFT:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[0] += 1
                elif event.key == pygame.K_UP:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[1] += 1
                elif event.key == pygame.K_r:
                    self.load_map()
                    self.player_health = self.max_health
                    continue
                
                # Check if movement is valid
                if self.can_move_to(new_pos[0], new_pos[1]):
                    self.player_pos = new_pos
                    self.apply_terrain_effect()
                    self.move_cooldown = 5  # Normal cooldown
                else:
                    self.set_status("Can't move there - obstacle!", RED)
        
        return True

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw tilemap (clean, no property indicators in game mode)
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
        
        # Draw HUD
        self.draw_hud()
        
        pygame.display.flip()

    def draw_hud(self):
        """Draw health bar and status"""
        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        
        pygame.draw.rect(self.screen, BLACK, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        health_width = int((self.player_health / self.max_health) * bar_width)
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        health_text = self.font.render(f"HP: {self.player_health}/{self.max_health}", True, WHITE)
        self.screen.blit(health_text, (bar_x + 5, bar_y + 2))
        
        # Status message
        if self.status_timer > 0:
            status_surf = self.font.render(self.status_message, True, self.status_color)
            status_rect = status_surf.get_rect(center=(GRID_WIDTH // 2, 50))
            
            bg_rect = status_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, WHITE, bg_rect)
            pygame.draw.rect(self.screen, BLACK, bg_rect, 2)
            self.screen.blit(status_surf, status_rect)
            
            self.status_timer -= 1

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            
            if self.move_cooldown > 0:
                self.move_cooldown -= 1
            
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "game":
        game = Game()
        game.run()
    else:
        editor = TilemapEditor()
        editor.run()