from enum import Enum

class SwitchType(str, Enum):
    NOISE = "NOISE",
    NEIGHBOUR_SELECTION_MODE = "NEIGHBOUR_SELECTION_MODE"