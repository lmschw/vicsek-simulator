from enum import Enum

class NeighbourSelectionModeEnum(Enum):
    RANDOM = 1,
    NEAREST = 2,
    FARTHEST = 3,
    LOWEST_CHANGE = 4