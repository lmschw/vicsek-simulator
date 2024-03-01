
import numpy as np
import math
import EnumMetrics as metrics

def evaluateSingleTimestep(positions, orientations, metric, radius=None):
     """
        Radius is only relevant for certain metrics such as Clustering, therefore it can be None for the others.
     """
     n = len(positions)
     match metric:
        case metrics.Metrics.ORDER:
            sumOrientation = orientations[0]
            for j in range(1, n):
                sumOrientation += orientations[j]
            return np.sqrt(sumOrientation[0]**2 + sumOrientation[1]**2) / n
        case metrics.Metrics.CLUSTER_NUMBER:
            nClusters, _ = findClusters(positions, orientations, radius)
            return nClusters
        case metrics.Metrics.CLUSTER_SIZE:
            nClusters, clusters = findClusters(positions, orientations, radius)
            clusterSizes = computeClusterSizes(nClusters, clusters)
            return clusterSizes

         
def findClusters(positions, orientations, radius):
    """
    - depending on positions and orientations
    - to belong to a cluster, a particle needs to be within the radius of at least one other member of the same cluster
    - to belong to a cluster, the orientation has to be similar
    """
    if radius == None:
        print("ERROR: Radius needs to be provided for clustering.")

    n = len(positions)
    clusters = np.zeros(n)
    clusterMembers = np.zeros((n,n))
    for i in range(n):
        neighbourIndices = findNeighbours(i, positions, radius)
        for neighbourIdx in neighbourIndices:
            if cosAngle(orientations[i], orientations[neighbourIdx]) >= 0.99:
                clusterMembers[i][neighbourIdx] = 1
    
    clusterCounter = 1
    for i in range(n):
        if markClusters(i, clusterCounter, clusters, clusterMembers, n) == True:
            clusterCounter += 1

    return clusterCounter, clusters
       
            
def findNeighbours(i, positions, radius):
    return [idx for idx in range(len(positions)) if isNeighbour(radius, positions, i, idx) and idx != i]


def isNeighbour(radius, positions, targetIdx, candidateIdx):
    return ((positions[candidateIdx][0] - positions[targetIdx][0])**2 + (positions[candidateIdx][1] - positions[targetIdx][1])**2) <= radius **2 

def cosAngle(vec1, vec2):
    """
    If the cosAngle is close to 1, their directions are identical. If it is close to -1, they look in opposite directions
    """
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / math.sqrt((vec1[0]**2 + vec1[1]**2) * (vec2[0]**2 + vec2[1]**2))

def markClusters(currentIdx, clusterCounter, clusters, clusterMembers, n):
    if clusters[currentIdx] != 0:
        return False
    clusters[currentIdx] = clusterCounter
    for i in range(n):
        if clusterMembers[currentIdx][i] == 1:
            markClusters(i, clusterCounter, clusters, clusterMembers, n)
    return True

def computeClusterSizes(clusterCounter, clusters):
    clusterSizes = clusterCounter * [0]
    for cluster in clusters:
        clusterSizes[int(cluster)] += 1
    return clusterSizes

