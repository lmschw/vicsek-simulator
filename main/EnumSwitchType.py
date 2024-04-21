from enum import Enum

"""
Contains the different hyperparameters that can be used to switch between behaviours.
"""
class SwitchType(str, Enum):
    NOISE = "NOISE",
    NEIGHBOUR_SELECTION_MODE = "NEIGHBOUR_SELECTION_MODE",
    K = "K"