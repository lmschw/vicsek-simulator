import math
import numpy as np

import ServiceMetric
import ServiceVicsekHelper

from EnumSwitchType import SwitchType

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

def getMinAvgMaxNumberOfNeighboursFromTrackingInfoSingleRun(neighbours):
    timestepInfoMin = []
    timestepInfoAvg = []
    timestepInfoMax = []
    for val in neighbours.values():
        numNeighbours = [len(value) for value in val.values()] # this is a dict and needs values()
        timestepInfoMin.append(np.min(numNeighbours))
        timestepInfoAvg.append(np.average(numNeighbours))
        timestepInfoMax.append(np.max(numNeighbours))
    
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
    