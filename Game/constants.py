from enum import Enum

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
    DECISION = "decision"

