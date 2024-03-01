from enum import Enum

class Metrics(str, Enum):
    ORDER = "ORDER",
    CLUSTER_NUMBER = "CLUSTER_NUMBER",
    CLUSTER_SIZE = "CLUSTER_SIZE"