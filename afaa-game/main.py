import pygame
import asyncio
import sys
import os
sys.path.append("./afaa-game")

from Game.unit import Unit
from Game.grid import Grid
from Game.dialogue import DialogueBox
from Game.constants import GridState, SCREEN_WIDTH, SCREEN_HEIGHT
from Game.state import State_Manager, State


def load_tile_images(tile_size):
    """Loads tile images from the assets folder."""
    # This dictionary maps the tile 'type' string to its image file
    tile_files = {
        'grass': 'Grass1.png',
        'stone': 'Brick.png',
        'water': 'River.png',
        'mountain': 'Mountains.png'
    }
    
    loaded_images = {}
    asset_dir = "afaa-game/Game/assets/tiles/"
    
    for tile_type, filename in tile_files.items():
        path = os.path.join(asset_dir, filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            loaded_images[tile_type] = pygame.transform.scale(img, (tile_size, tile_size))
        except Exception as e:
            print(f"Error loading image for {tile_type}: {e}")
            # Create a bright pink fallback surface for missing images
            fallback_surface = pygame.Surface((tile_size, tile_size))
            fallback_surface.fill((255, 0, 255))
            loaded_images[tile_type] = fallback_surface


    return loaded_images

class FireEmblemGame:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("A Fleet Among Angels")
        
        self.clock = pygame.time.Clock()

        # self.tilemap = type('Tilemap', (), {
        #     'tilemap': {},  # Would contain your actual tilemap data
        #     'tile_size': 16
        # })()

        self.tilemap = self.load_tilemap_from_file("./afaa-game/Game/levels/level10.json")



        self.grid = Grid(self.tilemap, tile_size=64)

        self.tile_images = load_tile_images(self.grid.tile_size)


        self.setup_test_units()

        self.camera_offset = [0,0]


        self.state_manager = State_Manager()
        
        self.running = True

        self.camera_speed = 5

        

    def setup_test_units(self):

        player1 = Unit("Hero", (5, 5), movement_range=3, team="player", attack_range=1, sprite_path="afaa-game/Game/Assets/Unit/test.png")
        player2 = Unit("Mage", (6,5), movement_range=2, team="player", attack_range=2, sprite_path="afaa-game/Game/Assets/Unit/test2.png")

        enemy1 = Unit("Orc", (10,8), movement_range=2, team="enemy", attack_range=1, sprite_path="afaa-game/Game/Assets/Unit/test3.png")
        enemy2 = Unit("Goblin", (12, 9), movement_range=4, team="enemy", attack_range=1, sprite_path="afaa-game/Game/Assets/Unit/test4.png")

        self.grid.add_unit(player1)
        self.grid.add_unit(player2)

        self.grid.add_unit(enemy1)
        self.grid.add_unit(enemy2)

 
    def handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state_manager.current_state == "title":
                if self.handle_title_events(event) == False:
                    return False
                continue
            

            elif self.state_manager.current_state == "battle":


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        grid_pos = self.grid.world_to_grid(mouse_pos, tuple(self.camera_offset))

                        self.grid.handle_click(grid_pos=grid_pos, mouse_pos=mouse_pos)


                elif event.type == pygame.MOUSEMOTION:

                    mouse_pos = pygame.mouse.get_pos()
                    self.grid.update_hover(mouse_pos=mouse_pos)
                    

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        if self.grid.current_phase == "player":
                            self.grid.start_new_turn("enemy")
                            print(f"Switched to enemy phase")
                        
                        elif self.grid.current_phase == "enemy":
                            self.grid.start_new_turn("player")
                            print(f"Switched to player")


                    elif event.key == pygame.K_ESCAPE:


                        if self.grid.state == GridState.TARGETING:
                            self.grid.state = GridState.DECISION
                            self.grid.valid_attack_targets = set()


                        elif self.grid.state == GridState.DECISION:
                            self.grid.state = GridState.UNIT_SELECT

                    
                        elif self.grid.state == GridState.UNIT_SELECT:

                            self.grid.state = GridState.IDLE

                            if self.grid.history:

                                print(f"The length of grid history is {len(self.grid.history)}")
                                original_pos = self.grid.history.pop()
                                current_pos = self.grid.selected_unit.grid_pos
                                
                                self.grid.selected_unit.grid_pos = original_pos

                                del self.grid.unit_positions[current_pos]

                                self.grid.unit_positions[original_pos] = self.grid.selected_unit

                                print(f"Undid move")
                            
                            self.grid.deselect_unit(undo=True)

                        # else:
                        #     self.grid.deselect_unit()
                        

        

        keys = pygame.key.get_pressed()

        if self.state_manager.current_state == "battle":
            if keys[pygame.K_LEFT]:
                self.camera_offset[0] -= self.camera_speed

            if keys[pygame.K_RIGHT]:
                self.camera_offset[0] += self.camera_speed

            if keys[pygame.K_UP]:
                self.camera_offset[1] -= self.camera_speed
            
            if keys[pygame.K_DOWN]:
                self.camera_offset[1] += self.camera_speed
            
        return True
    
    def handle_title_events(self, event):

        

        title_state = self.state_manager.states["title"]

        if title_state.ui["start"].handle_event(event):
            print("Start button was clicked on the title screen")
            self.state_manager.switch_states("battle")
            return None


        elif title_state.ui["load"].handle_event(event):
            print("Load button on title screen was clicked")
            return None
        
        elif title_state.ui["exit"].handle_event(event):
            print("Exit button on title screen was clicked")

            # End the game.
            return False


    def update_title(self,dt):

        if self.state_manager.current_state == "title":

            title_state = self.state_manager.states["title"]

            for key, component in title_state.ui.items():
                if hasattr(component, 'update'):
                    component.update(dt)
    

    def render(self):

        self.screen.fill((50, 50, 50))

        if self.state_manager.current_state == "title":
            self.state_manager.states[self.state_manager.current_state].draw(self.screen)
            
        
        elif self.state_manager.current_state == "battle":
            # Render tilemap here
            # self.tilemap.render(self.screen, offset=self.camera_offset)

            self.render_tilemap()

            self.grid.render(self.screen, tuple(self.camera_offset))

            self.render_ui()

        # Update screen.
        pygame.display.flip()

    def render_ui(self):

        font = pygame.font.Font(None, 36)

        instruction = [
            "Click unit to select",
            "Click highlighted tile to move",
            "SPACE: New turn",
            "ESC: Deselect",
            "Arrows: Move camera"
        ]

        for i, instruction in enumerate(instruction):
            text = font.render(instruction, True, (255, 255, 255))
            
            # Blitting the instructions under each other through each iteration
            self.screen.blit(text, (10, 10 + i * 30))


        state_text =f"State: {self.grid.state.value}"

        if self.grid.selected_unit:
            state_text += f" - {self.grid.selected_unit.name}"

        text = font.render(state_text, True, (255, 255, 0))
        self.screen.blit(text, (10, 200))

    


    async def run(self):
        while self.running:
            self.running = self.handle_input()

            dt = self.clock.tick(60) / 1000.0 

            self.update_title(dt)
            # Enemy AI implementation with timer

            if self.state_manager.current_state == "battle":
                if self.grid.current_phase == "enemy":
                    current_time = pygame.time.get_ticks()
                    
                    if current_time - self.grid.enemy_turn_timer >= self.grid.enemy_turn_delay:
                        self.grid.enemy_ai()
                        self.grid.enemy_turn_timer = current_time

            self.render()
            self.clock.tick(60)
            await asyncio.sleep(0)


    def load_tilemap_from_file(self, filepath):
        """Load tilemap from JSON file created by the editor"""
        import json
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Create a tilemap object compatible with your Grid class
            tilemap_obj = type('Tilemap', (), {
                'tilemap': {},
                'tile_size': 64  # Your game uses 64px tiles
            })()
            
            # If the file has the new format with tile_properties
            if isinstance(data, dict) and "tilemap" in data:
                map_data = data["tilemap"]
                tile_props = data.get("tile_properties", {})
            else:
                map_data = data
                tile_props = {}
            
            # Convert the 2D array to your game's format
            for row_idx, row in enumerate(map_data):
                for col_idx, tile_id in enumerate(row):
                    if tile_id != 0:  # Skip empty tiles
                        key = f"{col_idx};{row_idx}"
                        tilemap_obj.tilemap[key] = {
                            'type': self.get_tile_type_name(tile_id),
                            'walkable': tile_props.get(str(tile_id), {}).get('walkable', True),
                            'effect': tile_props.get(str(tile_id), {}).get('effect', None)
                        }
            
            print(f"✓ Loaded tilemap from {filepath}")
            return tilemap_obj
            
        except FileNotFoundError:
            print(f"✗ Map file not found: {filepath}")
            return self.create_empty_tilemap()
        except Exception as e:
            print(f"✗ Error loading map: {e}")
            return self.create_empty_tilemap()

    def get_tile_type_name(self, tile_id):
        """Convert tile ID to type name for your game"""
        tile_mapping = {
            1: 'grass',
            2: 'stone',
            3: 'water',
            4: 'stone',
            5: 'mountain',
            6: 'stone',
            7: 'grass',  # Forest
            8: 'grass',  # Healing
            9: 'stone'   # Lava
        }
        return tile_mapping.get(tile_id, 'grass')

    def create_empty_tilemap(self):
        """Create an empty tilemap as fallback"""
        return type('Tilemap', (), {
            'tilemap': {},
            'tile_size': 64
        })()
    
    # Add this new method to your FireEmblemGame class
    def render_tilemap(self):
        """Renders the background terrain tiles based on camera position."""
        screen_width, screen_height = self.screen.get_size()

        # Calculate the range of grid coordinates visible on screen to avoid drawing the whole map
        start_col = self.camera_offset[0] // self.grid.tile_size
        end_col = start_col + (screen_width // self.grid.tile_size) + 2
        start_row = self.camera_offset[1] // self.grid.tile_size
        end_row = start_row + (screen_height // self.grid.tile_size) + 2

        # Loop through only the visible tiles
        for x in range(start_col, end_col):
            for y in range(start_row, end_row):
                tile_key = f"{x};{y}"
                tile_data = self.tilemap.tilemap.get(tile_key)

                if tile_data:
                    tile_type = tile_data.get('type', 'grass') # Default to 'grass' if type is missing
                    tile_image = self.tile_images.get(tile_type)
                    
                    if tile_image:
                        # Calculate the tile's position on the screen
                        screen_x = x * self.grid.tile_size - self.camera_offset[0]
                        screen_y = y * self.grid.tile_size - self.camera_offset[1]
                        self.screen.blit(tile_image, (screen_x, screen_y))

 
        

if __name__ == "__main__":
    game = FireEmblemGame()
    asyncio.run(game.run())