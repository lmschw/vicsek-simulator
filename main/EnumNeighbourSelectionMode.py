from enum import Enum

class NeighbourSelectionMode(str, Enum):
    RANDOM = "RANDOM",
    NEAREST = "NEAREST",
    FARTHEST = "FARTHEST"