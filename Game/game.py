import pygame
import sys 
from enum import Enum
from typing import List, Tuple, Dict, Optional, Set


class TileType(Enum):

    GRASS = "grass"
    STONE = "stone"
    WATER = "water"
    MOUNTAIN = "mountain"

class GridState(Enum):
    IDLE = "idle"
    UNIT_SELECT = "unit_select"
    MOVING = "moving"
    TARGETING = "targeting"


# Unit Class -------------------------------------------------------
class Unit:
    def __init__(self, name: str, grid_pos: Tuple[int, int], movement_range: int = 3, team: str = "player", hp=100, attack=20):
        self.name = name
        self.grid_pos = grid_pos
        self.movement_range = movement_range
        
        self.has_moved = False
        self.team = team    # "ally", "enemy"
        self.sprite = None  # pygame surface

        self.hp = hp
        self.max_hp = hp
        self.attack = attack

    
    def get_pixel_pos(self, tile_size:int) -> Tuple[int, int]:


        # Convert tile unit to pixel unit
        return (self.grid_pos[0] * tile_size, self.grid_pos[1] * tile_size)


    def can_move(self):
        return not self.has_moved
    


class Grid:

    def __init__(self, tilemap, tile_size=16):
        

        self.tilemap = tilemap
        self.tile_size = tile_size

        self.state = GridState.IDLE
        self.selected_unit: Optional[Unit] = None

        self.show_grid = False # Only show grid when you are selecting a unit to move


        # Unit Management

        self.units = []
        self.unit_positions: Dict[Tuple[int, int], Unit] = {}

        self.valid_moves: Set[Tuple[int, int]] = set()

        self.movement_path: List[Tuple[int, int]] = []

        self.grid_color = (255, 255, 255, 100)
        self.valid_move_color = (0, 255, 0, 100)
        self.select_color = (255, 255, 0, 155)

        self.path_color = (0, 150, 255, 120)


        # Cost for moving through specfic tiles
        self.terrain_cost = {
            TileType.GRASS: 1,
            TileType.STONE: 2,
            TileType.WATER: 99,
            TileType.MOUNTAIN: 3,
        }

    
    def add_unit(self, unit:Unit) -> bool:
        # Returns True if successfully added unit False if place is occupied

        if unit.grid_pos in self.unit_positions:
            print("Position is occupied")
            return False
        
        self.units.append(unit)

        self.unit_positions[unit.grid_pos] = unit

        print(f"Add {unit.name} to position {unit.grid_pos}")

        return True
    
    def remove_unit(self, unit:Unit):

        # Remove the specificed unit and its position.
        if unit in self.units:
            self.units.remove(unit)

            if self.unit.grid_pos in self.unit_positions:
                del self.unit_positions[unit.grid_pos]

    def get_unit_at_pos(self, grid_pos: Tuple[int, int]):

        return self.unit_positions.get(grid_pos)

    def get_terrain_type(self, grid_pos: Tuple[int, int]):

        x,y = grid_pos
        tile_key = f"{x};{y}"

        # Looks for the key in the tilemap dictionary which is a position and 
        # finds the tile type of that position's tile.
        if tile_key in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[tile_key]

            tile_type = tile['type']

            if tile_type == 'grass':
                return TileType.GRASS
            
            elif tile_type == 'stone':
                return TileType.STONE
            
            elif tile_type == 'water':
                return TileType.WATER

            
            elif tile_type == 'mountain':
                return TileType.MOUNTAIN
        
        # Return Grass terrain type if no terrain typ is found
        return TileType.GRASS

        
        
    def is_passable(self, grid_pos: Tuple[int,int]) -> bool:

        # Cannot walk through a unit.
        if grid_pos in self.unit_positions:
            return False

        
        
        terrain_type = self.get_terrain_type(grid_pos)
        

        return self.terrain_cost[terrain_type]
    
    def calculate_movement_range(self, unit: Unit) ->Set[Tuple[int, int]]:

        # Checks if the unit has already moved or not
        if not unit.can_move():
            return set()
        
        # Starting position is the unit's current position
        start_pos = unit.grid_pos

        # Max movement is already determined in the unit class
        max_movement = unit.movement_range

        # distances stores the cost to go to each tile in this map
        distances = {start_pos: 0}

        # Makes sure we don't loop to the same tiles again.
        visited = set()

        # A list of tiles need to explore.
        to_visit = [start_pos]

        # While we still have tiles to look at continue the loop.
        while to_visit:

            # Gets the lowest move_cost tile in the to_visit list to check.
            # current is current tile's position that we are looking at
            current = min(to_visit, key=lambda pos: distances[pos])

            # Removes the tile from the to_visit list so don't visit it anymore
            to_visit.remove(current)

            visited.add(current)

            # Gets the move cost of the current tile we are looking at.
            current_dist = distances[current]

            # Chechking the movement range of the neighboring tiles.
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # If the neighboring tile has already been visited or is not passable skip it.
                if neighbor in visited:
                    continue

                if not self.is_passable(neighbor):
                    continue

                # Calculate the move cost of the neigboring tile.
                terrain = self.get_terrain_type(neighbor)

                # ,1) means if the key doesn't exist in the self.terrain_cost dictionary
                # the cost will be 1
                move_cost = self.terrain_cost.get(terrain,1)

                # Calculate the total distances towards this neighboring tile 
                # if the distances is too far don't add it to the pool of 
                # reachable tiles.
                new_distance = current_dist + move_cost
                
                if new_distance > max_movement:
                    continue
                
                # If the neighboring tile is reachable and is a new tile add it to the 
                # distances dictionary to be saved.
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    if neighbor not in to_visit:
                        to_visit.append(neighbor)

            # Filter all of the tiles in the distance map to see if they are reachable to be 
            # returned.
            reachable = set()

            for pos, dist in distances.items():
                if pos != start_pos and dist <= max_movement:
                    reachable.add(pos)

        return reachable
        
    
    def select_unit(self, grid_pos: Tuple[int, int]) -> bool:
        
        unit = self.get_unit_at_pos(grid_pos=grid_pos)

        if not unit:
            return False
        
        if not unit.can_move():
            print(f"{unit.name} has already moved this turn")
            return False

        self.selected_unit = unit
        self.state = GridState.UNIT_SELECT
        self.show_grid = True

        self.valid_moves = self.calculate_movement_range(unit=unit)

        print(f"Selected {unit.name} - Movement range: {len(self.valid_moves)} tiles")

        return True
    
    def deselect_unit(self):

        self.selected_unit = None
        self.state = GridState.IDLE
        self.show_grid = False
        self.valid_moves.clear()
        self.movement_path.clear()

    
    def move_unit(self, destination: Tuple[int, int]) -> bool:

        if not self.selected_unit:
            return False
        
        if destination not in self.valid_moves:
            print(f"Invalid move to {destination}")
            return False

        original_pos = self.selected_unit.grid_pos

        self.selected_unit.grid_pos = destination
        self.selected_unit.has_moved = True

        del self.unit_positions[original_pos]
        self.unit_positions[destination] = self.selected_unit

        print(f"Moved {self.selected_unit.name} from {original_pos} to {destination}")

        self.deselect_unit()

        return True
    
    def start_new_turn(self):
        for unit in self.units: 
            unit.has_moved = False
        print("New turn has started")

    
    def handle_click(self, grid_pos: Tuple[int, int]) -> bool:

        if self.state == GridState.IDLE:
            return self.select_unit(grid_pos=grid_pos)

        # If you are clicking on a unit that has already been selected then
        # deselect it.
        elif self.state == GridState.UNIT_SELECT:
            if grid_pos == self.selected_unit.grid_pos:
                self.deselect_unit()
                return True

            # If you are newly selecting a unit 
            other_unit = self.get_unit_at_pos(grid_pos=grid_pos)

            if other_unit:
                return self.select_unit(grid_pos=grid_pos)
                
            return self.move_unit(grid_pos)

        return False
    
    def world_to_grid(self, world_pos: Tuple[int, int], camera_offset: Tuple[int, int] = (0,0)) -> Tuple[int,int]:

        adjusted_x = world_pos[0] + camera_offset[0]
        adjusted_y = world_pos[1] + camera_offset[1]

        grid_x = int(adjusted_x // self.tile_size)
        grid_y = int(adjusted_y // self.tile_size)

        return (grid_x, grid_y)
    
    def grid_to_world(self, grid_pos: Tuple[int,int]) -> Tuple[int, int]:

        return(grid_pos[0] * self.tile_size, grid_pos[1] * self.tile_size)
    
   
    def render_grid_lines(self, surface: pygame.Surface, camera_offset: Tuple[int, int] = (0,0)):

        if not self.show_grid:
            return
        

        grid_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        screen_width, screen_height = surface.get_size()

        start_x = camera_offset[0] // self.tile_size

        # + 2 is to draw an extra 2 tiles accounting for tiles that are cut off.
        end_x = (camera_offset[0] + screen_width) // self.tile_size + 2

        start_y = camera_offset[1] // self.tile_size
        end_y = (camera_offset[1] + screen_height) // self.tile_size + 2

        # Drawing the grid outlines 
        # 1, ) in pygame.draw.line() is the line thickness
        # Rendering vertical grid lines
        for x in range(start_x, end_x):
            screen_x = x * self.tile_size - camera_offset[0]
            pygame.draw.line(grid_surface, self.grid_color,
                             (screen_x,0), (screen_x, screen_height), 1)



        # Rendering horizontal grid lines
        for y in range(start_y, end_y):
            screen_y = y * self.tile_size - camera_offset[1]
            pygame.draw.line(grid_surface, self.grid_color,
                             (0,screen_y), (screen_width, screen_y), 1)
            
        
        surface.blit(grid_surface, (0,0))

    
    def render_movement_overlay(self, surface: pygame.Surface, camera_offset: Tuple[int, int] = (0,0)):
        """Render movement range and selection highlights"""

        if self.state == GridState.IDLE:
            return
        
        overlay_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)


        # Highlight valid movement tiles
        for grid_pos in self.valid_moves:
            world_pos = self.grid_to_world(grid_pos=grid_pos)

            screen_x = world_pos[0] - camera_offset[0]
            screen_y = world_pos[1] - camera_offset[1]

            rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)

            pygame.draw.rect(overlay_surface, self.valid_move_color, rect)

            # ,2) is the thickness of the border
            pygame.draw.rect(overlay_surface, (0, 255, 0), rect, 2)


        # Highlighting the unit that is selected.
        if self.selected_unit:
            world_pos = self.grid_to_world(self.selected_unit.grid_pos)

            screen_x = world_pos[0] - camera_offset[0]
            screen_y = world_pos[1] - camera_offset[1]

            rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
            pygame.draw.rect(overlay_surface, self.select_color, rect)
            pygame.draw.rect(overlay_surface, (255, 255, 0), rect, 3)


        surface.blit(overlay_surface, (0,0))


    def render_units(self, surface: pygame.Surface, camera_offset: Tuple[int, int] = (0,0)):

        for unit in self.units:

            world_pos = self.grid_to_world(unit.grid_pos)

            screen_x = world_pos[0] - camera_offset[0]
            screen_y = world_pos[1] - camera_offset[1]

            # Renders the player units as blue
            # Red for enemy units
            color = (0, 0, 255) if unit.team == "player" else (255, 0, 0)

            # Rendering position of the unit making the unit smaller than the tile with - 4
            rect = pygame.Rect(screen_x + 2, screen_y + 2, self.tile_size - 4, self.tile_size - 4)
    
            pygame.draw.rect(surface, color, rect)

            # White border around units
            pygame.draw.rect(surface, (255, 255, 255), rect, 2)

            font = pygame.font.Font(None, 12)

            # Using [:3] rites the first 3 letters of the unit name
            text = font.render(unit.name[:3], True, (255, 255, 255))

            surface.blit(text, (screen_x + 2, screen_y + 2))


    def render(self, surface: pygame.Surface, camera_offset: Tuple[int,int] = (0,0)):

        self.render_grid_lines(surface, camera_offset=camera_offset)
        self.render_movement_overlay(surface=surface, camera_offset=camera_offset)
        self.render_units(surface=surface, camera_offset=camera_offset)


class FireEmblemGame:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Fire Emblem like game")
        
        self.clock = pygame.time.Clock()

        self.tilemap = type('Tilemap', (), {
            'tilemap': {},  # Would contain your actual tilemap data
            'tile_size': 16
        })()

        self.grid = Grid(self.tilemap, tile_size=32)

        self.setup_test_units()

        self.camera_offset = [0,0]

        self.camera_speed = 5

    def setup_test_units(self):

        player1 = Unit("Hero", (5, 5), movement_range=3, team="player")
        player2 = Unit("Mage", (6,5), movement_range=2, team="player")

        enemy1 = Unit("Orc", (10,8), movement_range=2, team="enemy")
        enemy2 = Unit("Goblin", (12, 9), movement_range=4, team="enemy")

        self.grid.add_unit(player1)
        self.grid.add_unit(player2)

        self.grid.add_unit(enemy1)
        self.grid.add_unit(enemy2)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    grid_pos = self.grid.world_to_grid(mouse_pos, tuple(self.camera_offset))

                    self.grid.handle_click(grid_pos=grid_pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.grid.start_new_turn()

                elif event.key == pygame.K_ESCAPE:
                    self.grid.deselect_unit()

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.camera_offset[0] -= self.camera_speed

        if keys[pygame.K_RIGHT]:
            self.camera_offset[0] += self.camera_speed

        if keys[pygame.K_UP]:
            self.camera_offset[1] -= self.camera_speed
        
        if keys[pygame.K_DOWN]:
            self.camera_offset[1] += self.camera_speed
        
        return True
    

    def render(self):

        self.screen.fill((50, 50, 50))

        # Render tilemap here
        # self.tilemap.render(self.screen, offset=self.camera_offset)

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

    def run(self):

        running = True
        while running:
            running = self.handle_input()
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = FireEmblemGame()
    game.run()

            

