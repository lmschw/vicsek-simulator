from enum import Enum

"""
Contains the evaluation metric options.
"""
class Metrics(Enum):
    AVERAGE_NUMBER_NEIGHBOURS ="avg_num_neighbours", "number of neighbours",
    MIN_AVG_MAX_NUMBER_NEIGHBOURS = "min_avg_max_num_neighbours", "number of neighbours",
    AVG_DISTANCE_NEIGHBOURS = "avg_distance_neighbours", "distance between neighbours",
    MIN_AVG_MAX_DISTANCE_NEIGHBOURS = "min_avg_max_distance_neighbours", "distance between neighbours",

    def __init__(self, val, label):
        self.val = val
        self.label = label