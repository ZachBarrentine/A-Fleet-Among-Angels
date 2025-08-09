from enum import Enum

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


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

