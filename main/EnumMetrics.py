from enum import Enum

"""
Contains the evaluation metric options.
"""
class Metrics(str, Enum):
    ORDER = "order",
    CLUSTER_NUMBER = "clusternumber",
    CLUSTER_SIZE = "clustersize",
    CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME = "clusternumber_lifetime",
    CLUSTER_CONSISTENCY_AVERAGE_STEPS = "clusterconst_steps",
    CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES = "clusterconst_changes",
    ORDER_VALUE_PERCENTAGE = "numorder" # number of order particles