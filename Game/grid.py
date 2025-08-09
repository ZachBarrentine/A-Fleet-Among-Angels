import pygame
from Game.unit import Unit
from Game.constants import TileType, GridState
from typing import List, Tuple, Dict, Optional, Set

class Grid:

    def __init__(self, tilemap, tile_size=16):
        

        self.tilemap = tilemap
        self.tile_size = tile_size

        self.current_phase = "player"   # either "player" or "enemy"


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

        self.history = []
        self.decision_menu = {}

        self.hovered_option = None
        self.menu_rects = {}
        
        self.valid_attack_targets = set()


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

            if unit.grid_pos in self.unit_positions:
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

        if unit.team != self.current_phase:
            print(f"Not your team's turn")
            return False
        
        
        if not unit.can_move():
            print(f"{unit.name} has already moved this turn")
            return False

        self.selected_unit = unit
        self.state = GridState.UNIT_SELECT
        self.show_grid = True

        self.history.clear() # Clear movement history for unit if not this unit
                             # will share the same movement history as previously selected and moved units.

        self.valid_moves = self.calculate_movement_range(unit=unit)

        print(f"Selected {unit.name} - Movement range: {len(self.valid_moves)} tiles")

        return True
    
    def deselect_unit(self, undo=False):

        if undo:
            self.valid_moves.clear()
            self.movement_path.clear()
            self.selected_unit.has_moved = False

        self.selected_unit = None
        self.state = GridState.IDLE
        self.show_grid = False
       

    
    def move_unit(self, destination: Tuple[int, int]) -> bool:

        if not self.selected_unit:
            return False
        
        if destination not in self.valid_moves:
            print(f"Invalid move to {destination}")
            return False

        
        original_pos = self.selected_unit.grid_pos

        self.history.append(original_pos)





        self.selected_unit.grid_pos = destination
        self.selected_unit.has_moved = True

        del self.unit_positions[original_pos]
        self.unit_positions[destination] = self.selected_unit

        print(f"Moved {self.selected_unit.name} from {original_pos} to {destination}")


        self.state = GridState.DECISION
        self.setup_decision_menu()
        return True
    
    def setup_decision_menu(self):
        if not self.selected_unit:
            return  
        
        # Have to pass in the unit's attack range even if not using it here because 
        # the set that stores all of the possible attack positions will be filled with incorrect
        # attack range.
        avaiable_attack, _ = self.can_attack_from_position(self.selected_unit.grid_pos, self.selected_unit.attack_range)

        self.decision_menu = {
        "Attack": avaiable_attack,
        "wait": True,
        "item": True
    }
    
    def render_decision_ui(self, surface, camera_offset: Tuple[int,int]):
        
        # If you are not in the decision state or have not selected a unit on the
        # screen you shouldn't render the decision ui.
        if self.state != GridState.DECISION or not self.selected_unit:
            return

        unit_world_pos = self.grid_to_world(self.selected_unit.grid_pos)

        unit_screen_x = unit_world_pos[0] - camera_offset[0] + self.tile_size //2
        unit_screen_y = unit_world_pos[1] - camera_offset[1]

        menu_width = 100
        menu_height = len(self.decision_menu) * 30 + 10
        option_height = 25

        menu_x = unit_screen_x - menu_width // 2
        menu_y = unit_screen_y - menu_height -10

        # Ensures the menu stays on the screen
        screen_width, screen_height = surface.get_size()

        menu_x = max(0, min(menu_x, screen_width - menu_width))
        menu_y = max(0, min(menu_y, screen_height - menu_height))

        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)

        pygame.draw.rect(menu_surface, (40, 40, 40, 200), (0, 0, menu_width, menu_height))
        pygame.draw.rect(menu_surface, (255, 255, 255), (0, 0, menu_width, menu_height), 2)

        font = pygame.font.Font(None, 24)

        y_offset = 5

        self.menu_rects.clear()

        for option_name, enabled in self.decision_menu.items():

            option_rect = pygame.Rect(menu_x + 5, menu_y + y_offset, menu_width - 10, option_height)
            self.menu_rects[option_name] = option_rect


            if enabled:
                text_color = (255, 255, 255 )
                if option_name == self.hovered_option:

                    pygame.draw.rect(menu_surface, (100, 100, 150),
                                     (5, y_offset, menu_width - 10, option_height))
            else:
                text_color = (128, 128, 128)

            


            text = font.render(option_name, True, text_color)
            text_rect = text.get_rect(center=(menu_width//2, y_offset + option_height // 2))

            menu_surface.blit(text, text_rect)

            y_offset += 30

        surface.blit(menu_surface, (menu_x, menu_y))





        

    
    def handle_decision_click(self, mouse_pos: Tuple[int, int]) -> bool:

        for option_name, enabled in self.decision_menu.items():
            if option_name in self.menu_rects and self.menu_rects[option_name].collidepoint(mouse_pos):

                if enabled:
                    self.execute_decision(option_name)
                    return True
        
        return False
    
    
    def update_hover(self, mouse_pos: Tuple[int,int]):

        if self.state != GridState.DECISION:
            self.hovered_option = None
            return
        
        self.hovered_option = None

        for option_name, enabled in self.decision_menu.items():
            if option_name in self.menu_rects and self.menu_rects[option_name].collidepoint(mouse_pos):
                if enabled:
                    self.hovered_option = option_name
                    break



    def execute_decision(self, action: str):

        if action == "wait":

            self.selected_unit.has_moved = True
            self.deselect_unit(undo=False)

        elif action == "Attack":
            
            
            self.state = GridState.TARGETING

            can_attack, enemies = self.can_attack_from_position(self.selected_unit.grid_pos, attack_range=self.selected_unit.attack_range)

            if can_attack:
                self.valid_attack_targets = enemies
                print(f"{self.selected_unit.name} is ready to attack! Click on an enemy to target.")

            else:
                print(f"No enemies to attack")



        elif action == "item":

            # Implement items later
            self.execute_decision("wait")

    def perform_attack(self, attacker: Unit, target: Unit):
        damage  = attacker.attack + (attacker.level * 2)
        
        target.take_dmg(damage)

        if target.hp <= 0:
            self.remove_unit(unit=target)

        print(f"{self.selected_unit.name} did {damage} damage to {target.name}")
        
        if target.hp <= 0:
            print(f"{target.name} has been defeated")
            return True
        

        return False


    def handle_click(self, grid_pos: Tuple[int, int], mouse_pos: Tuple[int,int] = None) -> bool:

        if self.state == GridState.DECISION:
            if mouse_pos:
                return self.handle_decision_click(mouse_pos)
        
            return False
        
        if self.state == GridState.IDLE:
            return self.select_unit(grid_pos=grid_pos)

        elif self.state == GridState.UNIT_SELECT:
            if grid_pos == self.selected_unit.grid_pos:
                
                self.selected_unit.has_moved = True
                self.state = GridState.DECISION
                self.setup_decision_menu()

                return True
            
            other_unit = self.get_unit_at_pos(grid_pos=grid_pos)

            if other_unit:
                return self.select_unit(grid_pos=grid_pos)
            
            return self.move_unit(grid_pos)

        elif self.state == GridState.TARGETING:
            target_unit = self.get_unit_at_pos(grid_pos=grid_pos)

            if target_unit and target_unit.team != self.selected_unit.team:

                can_attack, enemies = self.can_attack_from_position(self.selected_unit.grid_pos, self.selected_unit.attack_range)

                

                if can_attack and target_unit in enemies:

                    is_defeated = self.perform_attack(self.selected_unit, target_unit)

                    self.selected_unit.has_moved = True

                    self.show_grid = False

                    self.valid_attack_targets = set() 

                    self.deselect_unit(undo=False)

                    return True
                
                else:
                    print(f"Enemy out of range")
                
            else:
                print(f"Invalid target")


            return False




    def render_attack_overlay(self, surface: pygame.Surface, camera_offset: Tuple[int,int] = (0,0)):

        if self.state != GridState.TARGETING:
            return
        
        overlay_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        # Highlight enemies in range
        if hasattr(self, 'valid_attack_targets'):
            for target_unit in self.valid_attack_targets:
                world_pos = self.grid_to_world(target_unit.grid_pos)

                screen_x = world_pos[0] - camera_offset[0]
                screen_y = world_pos[1] - camera_offset[1]

                # rect of the enemy unit that will be used for highlighting effect
                rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)

                pygame.draw.rect(overlay_surface, (255, 0, 0, 100), rect)
                pygame.draw.rect(overlay_surface, (255, 0, 0), rect, 3)


        if self.selected_unit:
            world_pos = self.grid_to_world(self.selected_unit.grid_pos)


            screen_x = world_pos[0] - camera_offset[0]
            screen_y = world_pos[1] - camera_offset[1]

            rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)

            pygame.draw.rect(overlay_surface, self.select_color, rect)

            pygame.draw.rect(overlay_surface, (255, 255, 0), rect, 3)


        surface.blit(overlay_surface, (0,0))





    def can_attack_from_position(self, unit_pos, attack_range=1):

        enemies_to_attack = set()

        if attack_range == 1:

            # Can only attack adjacent sides if attack range is 1.
            for dx , dy in ([(0, 1), (1, 0), (0, -1), (-1, 0)]):
                target_pos = (unit_pos[0] + dx, unit_pos[1] + dy)

                target_unit = self.get_unit_at_pos(target_pos)
        

                if target_unit and target_unit.team != self.selected_unit.team:
                    enemies_to_attack.add(target_unit)
            

            
            
        # attack_range of 2+
        else:
            
            for dx in range(-attack_range, attack_range + 1):
                for dy in range(-attack_range, attack_range + 1):

                    if dx == 0 and dy == 0:
                        continue
                        
                    distance = abs(dx) + abs(dy)

                    if distance == attack_range:
                        target_pos = (unit_pos[0] + dx, unit_pos[1] + dy)

                        target_unit = self.get_unit_at_pos(target_pos)

                        if target_unit and target_unit.team != self.selected_unit.team:
                            enemies_to_attack.add(target_unit)


        if len(enemies_to_attack) != 0:
            return True, enemies_to_attack
        
        else:
            return False, None


    def start_new_turn(self, phase: str):

        if phase:
            self.current_phase = phase

        for unit in self.units:
            if unit.team == self.current_phase:
                unit.has_moved = False

        print("New turn has started")

    
    def all_units_moved(self) -> bool:
       
        return all(u.has_moved for u in self.units if u.team == self.current_phase)


    
    
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

            # Render the unit's sprite else fall back to using red and blue squares.
            if unit.sprite:
                surface.blit(unit.sprite, (screen_x + 2, screen_y + 2))

            else:
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


            mouse_pos = pygame.mouse.get_pos()
            hover_grid_pos = self.world_to_grid(mouse_pos, camera_offset=camera_offset)


            if hover_grid_pos == unit.grid_pos:

                # Health bar dimensions
                bar_width = self.tile_size - 4
                bar_height = 5
                bar_x = screen_x + 2
                bar_y = screen_y + 6 # Making the health bar be above the unit

                # Background of the bar is gray for visability
                pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

                # Foreground green/red 

                hp_ratio = max(0, unit.hp / unit.max_hp)
                hp_color = (0, 255, 0) if hp_ratio > 0.5 else (255, 0, 0)

                pygame.draw.rect(surface, hp_color, (bar_x, bar_y, bar_width * hp_ratio, bar_height))


    def render(self, surface: pygame.Surface, camera_offset: Tuple[int,int] = (0,0)):

        self.render_grid_lines(surface, camera_offset=camera_offset)
        self.render_movement_overlay(surface=surface, camera_offset=camera_offset)
        self.render_attack_overlay(surface=surface, camera_offset=camera_offset)

        self.render_units(surface=surface, camera_offset=camera_offset)
        self.render_decision_ui(surface=surface, camera_offset=camera_offset)

    def enemy_ai(self):
        """Simple enemy AI that moves towards players and attacks when possible"""
        
        # Get all enemy units that haven't moved yet
        enemy_units = [unit for unit in self.units 
                    if unit.team == "enemy" and not unit.has_moved]
        
        if not enemy_units:
            # All enemies have moved, switch to player turn
            self.start_new_turn("player")
            return
        
        # Process each enemy unit
        for enemy_unit in enemy_units:
            if enemy_unit.has_moved:
                continue
                
            # Select the enemy unit
            self.selected_unit = enemy_unit
            self.state = GridState.UNIT_SELECT
            
            # Calculate movement range
            self.valid_moves = self.calculate_movement_range(enemy_unit)
            
            # Find the closest player unit
            closest_player = self.find_closest_player(enemy_unit)
            
            if closest_player:
                # Try to attack first if already in range
                can_attack, targets = self.can_attack_from_position(
                    enemy_unit.grid_pos, enemy_unit.attack_range
                )
                
                if can_attack and targets:
                    # Attack the first available target
                    target = next(iter(targets))  # Get first target from set
                    print(f"{enemy_unit.name} attacks {target.name}!")
                    self.perform_attack(enemy_unit, target)
                    enemy_unit.has_moved = True
                else:
                    # Move towards closest player
                    best_move = self.find_best_move_towards_target(
                        enemy_unit, closest_player
                    )
                    
                    if best_move and best_move in self.valid_moves:
                        # Move the enemy
                        original_pos = enemy_unit.grid_pos
                        enemy_unit.grid_pos = best_move
                        
                        # Update unit positions
                        del self.unit_positions[original_pos]
                        self.unit_positions[best_move] = enemy_unit
                        
                        print(f"{enemy_unit.name} moves from {original_pos} to {best_move}")
                        
                        # Check if can attack after moving
                        can_attack, targets = self.can_attack_from_position(
                            best_move, enemy_unit.attack_range
                        )
                        
                        if can_attack and targets:
                            # Attack after moving
                            target = next(iter(targets))
                            print(f"{enemy_unit.name} attacks {target.name} after moving!")
                            self.perform_attack(enemy_unit, target)
                    
                    enemy_unit.has_moved = True
            else:
                # No players found, just mark as moved
                enemy_unit.has_moved = True
            
            # Clear selection
            self.selected_unit = None
            self.state = GridState.IDLE
            self.valid_moves.clear()
        
        # Check if all enemies have moved
        if self.all_units_moved():
            print("All enemies have moved, switching to player turn")
            self.start_new_turn("player")

    def find_closest_player(self, enemy_unit):
        """Find the closest player unit to the given enemy unit"""
        player_units = [unit for unit in self.units if unit.team == "player"]
        
        if not player_units:
            return None
        
        closest_player = None
        min_distance = float('inf')
        
        for player_unit in player_units:
            distance = self.calculate_distance(enemy_unit.grid_pos, player_unit.grid_pos)
            if distance < min_distance:
                min_distance = distance
                closest_player = player_unit
        
        return closest_player

    def calculate_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_best_move_towards_target(self, enemy_unit, target_unit):
        """Find the best move that gets the enemy closer to the target"""
        if not self.valid_moves:
            return None
        
        target_pos = target_unit.grid_pos
        best_move = None
        min_distance = float('inf')
        
        # Check each possible move
        for move_pos in self.valid_moves:
            distance = self.calculate_distance(move_pos, target_pos)
            
            # Prefer moves that get us closer to the target
            if distance < min_distance:
                min_distance = distance
                best_move = move_pos
            # If same distance, prefer moves that might allow attacking next turn
            elif distance == min_distance:
                # Check if this position would allow attacking next turn
                potential_attack_distance = distance - enemy_unit.attack_range
                current_best_attack_distance = self.calculate_distance(best_move, target_pos) - enemy_unit.attack_range
                
                if potential_attack_distance < current_best_attack_distance:
                    best_move = move_pos
        
        return best_move