from enum import Enum

"""
Contains all the different ways of selecting a subset of neighbours from all possible neighbours.
"""
class NeighbourSelectionMode(str, Enum):
    RANDOM = "RANDOM",
    NEAREST = "NEAREST",
    FARTHEST = "FARTHEST",
    LEAST_ORIENTATION_DIFFERENCE = "LEAST_ORIENTATION_DIFFERENCE",
    HIGHEST_ORIENTATION_DIFFERENCE = "HIGHEST_ORIENTATION_DIFFERENCE",
    ALL = "ALL"