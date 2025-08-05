
from typing import Tuple

class Unit:
    def __init__(self, name: str, grid_pos: Tuple[int, int], movement_range: int = 3, team: str = "player", hp=100, attack=20, attack_range=1):
        self.name = name
        self.grid_pos = grid_pos
        self.movement_range = movement_range
        

        self.attack_range = attack_range

        self.has_moved = False
        self.team = team    # "ally", "enemy"
        self.sprite = None  # pygame surface

        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.level = 1

    def get_pixel_pos(self, tile_size:int) -> Tuple[int, int]:


        # Convert tile unit to pixel unit
        return (self.grid_pos[0] * tile_size, self.grid_pos[1] * tile_size)


    def can_move(self):
        return not self.has_moved
    
    def take_dmg(self, incoming_dmg):
        self.hp -= incoming_dmg
    