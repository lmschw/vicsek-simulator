import math
import numpy as np

import ServiceMetric
import ServiceVicsekHelper

from EnumSwitchType import SwitchType
from EnumMetricsTrackingInfo import Metrics

def getConnectionTrackingInformation(positions, orientations, radius, switchTypeValues=None, switchType=None, k=None, neighbourSelectionMode=None):
    
    n = len(positions[0])

    if switchType == SwitchType.NEIGHBOUR_SELECTION_MODE and k == None:
        raise Exception("Need to provide k for switchType NEIGHBOUR_SELECTION_MODE")
    if switchType == SwitchType.K and neighbourSelectionMode == None:
        raise Exception("Need to provide neighbourSelectionMode for switchType K")

    neighbours = {}
    distances = {}
    localOrders = {}
    orientationDifferences = {}
    selected = {}

    for t in range(len(positions)):
        neighboursT = {}
        distancesT = {}
        localOrdersT = {}
        orientationDifferencesT = {}
        selectedT = {}

        positionsT = positions[t]
        orientationsT = orientations[t]
        for i in range(n):
            # neighbours
            neighboursI = ServiceMetric.findNeighbours(i, positionsT, radius)
            neighboursT[i] = neighboursI

            # distances
            distancesI = [math.dist(positionsT[i], positionsT[candidateIdx]) for candidateIdx in range(n)]
            distancesT[i] = distancesI

            # localOrder
            neighbourOrientations = [orientationsT[neighbourIdx] for neighbourIdx in neighboursI]
            localOrdersI = ServiceMetric.computeOrder(neighbourOrientations)
            localOrdersT[i] = localOrdersI

            # orientationDifferences
            orientationDifferencesI = [ServiceMetric.computeOrder([orientationsT[i], orientationsT[candIdx]]) for candIdx in range(n)]
            orientationDifferencesT[i] = orientationDifferencesI

            # selected
            if switchType != None:
                switchTypeValuesT = switchTypeValues[t]
                if switchType == SwitchType.NEIGHBOUR_SELECTION_MODE:
                    neighbourSelectionMode = switchTypeValuesT[i]
                elif switchType == SwitchType.K:
                    k = switchTypeValuesT[i]
            selectedI = ServiceVicsekHelper.pickNeighbours(neighbourSelectionMode=neighbourSelectionMode, k=k, candidates=neighboursI, currentParticlePosition=positionsT[i], currentParticleOrientation=orientationsT[i], positions=positionsT, orientations=orientationsT)
            selectedT[i] = selectedI
        neighbours[t] = neighboursT
        distances[t] = distancesT
        localOrders[t] = localOrdersT
        orientationDifferences[t] = orientationDifferencesT
        selected[t] = selectedT

    return {
        "neighbours": neighbours,
        "distances": distances,
        "localOrders": localOrders,
        "orientationDifferences": orientationDifferences,
        "selected": selected
    }

def evaluateSingleTimestep(metric, neighbours=None, distances=None, 
                 localOrders=None, orientationDifferences=None, selected=None, 
                 threshold=0.01):
     """
        Evaluates the simulation data for a single timestep according to the selected metric.

        Parameters:
            - positions (array): the position of every particle at this timestep
            - orientations (array): the orientation of every particle at this timestep
            - metric (EnumMetrics): the metric for evaluating the data
            - radius (int) [optional]: the perception radius of every particle. Radius is only relevant for certain metrics such as Clustering, therefore it can be None for the others.
            - threshold (float) [optional]: the threshold for the agglomerative clustering
            - switchTypeValues (array) [optional]: the switch type values for individual switching
            - switchTypeOptions (tuple) [optional]: contains the orderValue and the disorderValue respectively
        Returns:
            An array of the results according to the metric.
     """
     match metric:
        case Metrics.AVERAGE_NUMBER_NEIGHBOURS:
            _, avg, _ = getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleTimestep(neighbours)
            return avg
        case Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS:
            return getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleTimestep(neighbours)
        case Metrics.AVG_DISTANCE_NEIGHBOURS:
            _, avg, _ = getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleTimestep(neighbours, distances)
            return avg
        case Metrics.MIN_AVG_MAX_DISTANCE_NEIGHBOURS:
            return getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleTimestep(neighbours, distances)
         
def getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleTimestep(neighbours):
    numNeighbours = [len(value) for value in neighbours.values()]
    return np.min(numNeighbours), np.average(numNeighbours), np.max(numNeighbours)

def getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleRun(neighbours):
    timestepInfoMin = []
    timestepInfoAvg = []
    timestepInfoMax = []
    for timestepData in neighbours.values():
        minT, avgT, maxT = getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleTimestep(timestepData)
        timestepInfoMin.append(minT)
        timestepInfoAvg.append(avgT)
        timestepInfoMax.append(maxT)
    return np.min(timestepInfoMin), np.average(timestepInfoAvg), np.max(timestepInfoMax)

def getMinAvgMaxNumberOfNeighboursFromTrackingInfoMultipleRuns(neighbours):
    runInfoMin = []
    runInfoAvg = []
    runInfoMax = []
    for i in range(len(neighbours)):
        minR, avgR, maxR = getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleRun(neighbours[i])
        runInfoMin.append(minR)
        runInfoAvg.append(avgR)
        runInfoMax.append(maxR)
    return np.min(runInfoMin), np.average(runInfoAvg), np.max(runInfoMax)

def getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleTimestep(neighbours, distances):
    distNeighbours = []
    for key in neighbours.keys():
        for value in neighbours[key]:
            distNeighbours.append(distances[key][value])
    return np.min(distNeighbours), np.average(distNeighbours), np.max(distNeighbours)
    
def getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleRun(neighbours, distances):
    timestepInfoMin = []
    timestepInfoAvg = []
    timestepInfoMax = []
    for timestep, timestepData in neighbours.items():
        minT, avgT, maxT = getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleTimestep(neighbours=timestepData, distances=distances[timestep])
        timestepInfoMin.append(minT)
        timestepInfoAvg.append(avgT)
        timestepInfoMax.append(maxT)
    
    return np.min(timestepInfoMin), np.average(timestepInfoAvg), np.max(timestepInfoMax)

def getMinAvgMaxNeighbourDistanceFromTrackingInfoMultipleRuns(neighbours, distances):
    runInfoMin = []
    runInfoAvg = []
    runInfoMax = []
    for i in range(len(neighbours)):
        minR, avgR, maxR = getMinAvgMaxNeighbourDistanceFromTrackingInfoSingleRun(neighbours[i], distances[i])
        runInfoMin.append(minR)
        runInfoAvg.append(avgR)
        runInfoMax.append(maxR)
    
    return np.min(runInfoMin), np.average(runInfoAvg), np.max(runInfoMax)
    