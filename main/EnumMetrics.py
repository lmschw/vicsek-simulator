from enum import Enum

"""
Contains the evaluation metric options.
"""
class Metrics(Enum):
    ORDER = "order", "order",
    CLUSTER_NUMBER = "clusternumber", "number of clusters",
    CLUSTER_NUMBER_WITH_RADIUS = "numclusterr", "number of clusters"
    CLUSTER_SIZE = "clustersize", "cluster size",
    CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME = "clusternumber_lifetime", "numbers of clusters a particle has belonged to over its lifetime",
    CLUSTER_CONSISTENCY_AVERAGE_STEPS = "clusterconst_steps", "average number of steps a cluster has remained consistent",
    CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES = "clusterconst_changes", "number of changes to a cluster"
    ORDER_VALUE_PERCENTAGE = "numorder", "percentage of particles with order-inducing value", # number of order particles
    DUAL_OVERLAY_ORDER_AND_PERCENTAGE = "dual-order-num", "order/percentage of particles with order-inducing value",
    AVERAGE_NUMBER_NEIGHBOURS ="avg_num_neighbours", "number of neighbours",
    MIN_AVG_MAX_NUMBER_NEIGHBOURS = "min_avg_max_num_neighbours", "number of neighbours",
    AVG_DISTANCE_NEIGHBOURS = "avg_distance_neighbours", "distance between neighbours",
    AVG_CENTROID_DISTANCE = "avg_centroid_distance", "average distance from the centroid"
    #MIN_AVG_MAX_DISTANCE_NEIGHBOURS = "min_avg_max_distance_neighbours", "distance between neighbours",

    def __init__(self, val, label):
        self.val = val
        self.label = label