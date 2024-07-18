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

    print(f"n[0][0]={neighbours[0][0]}")
    print(f"d[0][0]={distances[0][0]}")
    print(f"lo[0][0]={localOrders[0][0]}")
    print(f"ods[0][0]={orientationDifferences[0][0]}")
    print(f"selected[0][0]={selected[0][0]}")


    return {
        "neighbours": neighbours,
        "distances": distances,
        "localOrders": localOrders,
        "orientationDifferences": orientationDifferences,
        "selected": selected
    }