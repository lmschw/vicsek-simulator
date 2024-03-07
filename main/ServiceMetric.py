
import numpy as np
import math
from collections import defaultdict
import EnumMetrics as metrics

def evaluateSingleTimestep(positions, orientations, metric, radius=None, threshold=0.99):
     """
        Evaluates the simulation data for a single timestep according to the selected metric.

        Parameters:
            - positions (array): the position of every particle at this timestep
            - orientations (array): the orientation of every particle at this timestep
            - metric (EnumMetrics): the metric for evaluating the data
            - radius (int) [optional]: the perception radius of every particle. Radius is only relevant for certain metrics such as Clustering, therefore it can be None for the others.

        Returns:
            An array of the results according to the metric.
     """
     n = len(positions)
     match metric:
        case metrics.Metrics.ORDER:
            sumOrientation = orientations[0]
            for j in range(1, n):
                sumOrientation += orientations[j]
            return np.sqrt(sumOrientation[0]**2 + sumOrientation[1]**2) / n
        case metrics.Metrics.CLUSTER_NUMBER:
            nClusters, _ = findClusters(positions, orientations, radius, threshold)
            return nClusters
        case metrics.Metrics.CLUSTER_SIZE:
            nClusters, clusters = findClusters(positions, orientations, radius, threshold)
            clusterSizes = computeClusterSizes(nClusters, clusters)
            return clusterSizes
        case metrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME:
            _, clusters = findClusters(positions, orientations, radius, threshold)
            return clusters

         
def findClusters(positions, orientations, radius, threshold=0.99):
    """
    Finds clusters in the particle distribution. The clustering is performed according to the following constraints:
        - to belong to a cluster, a particle needs to be within the radius of at least one other member of the same cluster
        - to belong to a cluster, the orientation has to be similar or equal (<= 1.29° orientation difference by default)
    
    Parameters:
        - positions (array): the position of every particle at the current timestep
        - orientations (array): the orientations of every particle at the current timestep
        - radius (int): the perception radius of the particles
    
    Returns:
        A tuple containing the number of clusters and the clusters.
    """
    if radius == None:
        print("ERROR: Radius needs to be provided for clustering.")

    n = len(positions)
    clusters = np.zeros(n)
    clusterMembers = np.zeros((n,n))
    for i in range(n):
        neighbourIndices = findNeighbours(i, positions, radius)
        for neighbourIdx in neighbourIndices:
            if cosAngle(orientations[i], orientations[neighbourIdx]) >= threshold:
                clusterMembers[i][neighbourIdx] = 1
    
    clusterCounter = 1
    for i in range(n):
        if markClusters(i, clusterCounter, clusters, clusterMembers, n) == True:
            clusterCounter += 1

    return clusterCounter, clusters
       
            
def findNeighbours(i, positions, radius):
    """
    Determines which particles are neighoburs of particle i.

    Parameters:
        - i (int): the index of the target particle for which the neighbours should be found
        - positions (array): the position of every particle at the current timestep
        - radius (int): the perception radius of every particle

    Returns:
        A list of indices of all neighbours within the perception range.
    """
    return [idx for idx in range(len(positions)) if isNeighbour(radius, positions, i, idx) and idx != i]


def isNeighbour(radius, positions, targetIdx, candidateIdx):
    """
    Checks if two particles are neighbours.

    Parameters:
        - radius (int): the perception radius of every particle
        - positions (array): the position of every particle at the current timestep
        - targetIdx (int): the index of the target particle within the positions array
        - candidateIdx (int): the index of the candidate particle within the positions array
    
    Returns:
        A boolean stating whether or not the two particles are neighbours.
    """
    return ((positions[candidateIdx][0] - positions[targetIdx][0])**2 + (positions[candidateIdx][1] - positions[targetIdx][1])**2) <= radius **2 

def cosAngle(vec1, vec2):
    """
    Checks the relative orientations of two particles. If the cosAngle is close to 1, their directions are identical. 
    If it is close to -1, they look in opposite directions.

    Parameters:
        - vec1 (vector): the orientation of the first particle
        - vec2 (vector): the orientation of the second particle

    Returns:
        The cosAngle as an integer representing the similarity of the orientations.
    """
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec2[0]**2 + vec2[1]**2))

def markClusters(currentIdx, clusterCounter, clusters, clusterMembers, n):
    """
    Recursive function that marks all neighbours with a similar orientation as belonging to the same cluster.

    Parameters:
        - currentIdx (int): index of the current particle within the clusters array
        - clusterCounter (int): the current maximum of found clusters. Will not be updated in this function
        - clusters (array): represents the cluster membership of all particles by the id of the cluster
        - clusterMembers (array of arrays): represents which other particles are neighbours with a similar 
            orientation to the current particle, i.e. the members of the same cluster as seen by the current particle
        - n (int): the total number of particles in the domain

    Returns:
        If any particle's cluster id has been updated. If the particle's own id is not updated, neither are its children.
        Therefore, the return values are not compared.
    """
    if clusters[currentIdx] != 0:
        return False
    clusters[currentIdx] = clusterCounter
    for i in range(n):
        if clusterMembers[currentIdx][i] == 1:
            markClusters(i, clusterCounter, clusters, clusterMembers, n)
    return True

def computeClusterSizes(clusterCounter, clusters):
    """
    Computes the size of every cluster.

    Parameters:
        - clusterCounter (int): the total number of clusters in the current state of the domain
        - clusters (array): array containing the id of the cluster that every particle belongs to

    Returns:
        An array with the length of clusterCounter containing the size of the respective cluster.
    """
    clusterSizes = clusterCounter * [0]
    for cluster in clusters:
        clusterSizes[int(cluster)] += 1
    return clusterSizes

def computeClusterNumberOverParticleLifetime(clusters):
    """
    Computes the number of clusters that every particle has belonged to over the whole course of a simulation.

    Parameters:
        - clusters (array of arrays): Contains the cluster membership for every particle at every timestep

    Returns:
        A dictionary with the index of the particle as its key and the total number of clusters that the particle 
        has belonged to as its value.
    """
    dd = defaultdict(list)
    for i in range(len(clusters[0])):
        for key, value in clusters.items():
            dd[i].append(value[i])
    countsPerParticle = {}
    for key, values in dd.items():
        countsPerParticle[key] = len(np.unique(values))
    return countsPerParticle

