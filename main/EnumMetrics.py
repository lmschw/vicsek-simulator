from enum import Enum

class Metrics(str, Enum):
    ORDER = "ORDER",
    CLUSTER_NUMBER = "CLUSTER_NUMBER",
    CLUSTER_SIZE = "CLUSTER_SIZE",
    CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME = "CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME",
    CLUSTER_CONSISTENCY_AVERAGE_STEPS = "CLUSTER_CONSISTENCY_AVERAGE_STEPS",
    CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES = "CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES"