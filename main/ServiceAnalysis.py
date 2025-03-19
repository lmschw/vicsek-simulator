
"""
Service containing static methods that can be used for analysis.
"""
import numpy as np
import ServiceMetric

def findParticlesSwitchingValues(n, switchValues, startTime=0, endTime=None):
    """
    Finds the indices of particles that switch values and the timesteps at which they switch.

    Params:
        - n (int): the total number of particles
        - switchValues (array of switchTypeValues): the switch type value of every particle at every timestep
        - startTime (int) [optional]: the first timestep to be included
        - endTime (int) [optional]: the last timestep to be included

    Returns:
        A dictionary containing the indices of particles as keys and a tuple of timesteps and the new corresponding value as its value.
    """
    if endTime == None:
        endTime = len(switchValues)
    switchers = {}
    for i in range(n):
        val = switchValues[0][i]
        for timestep in range(startTime, endTime):
            newVal = switchValues[timestep][i]
            if val != newVal:
                if i in switchers.keys():
                    switchers.get(i).append((timestep, newVal))
                else:
                    switchers[i] = [(timestep, newVal)]
                val = newVal
    return switchers

def findParticleWithMaxSwitches(n, switchValues, startTime=0, endTime=None):
    """
    Determines the index of the particle that has performed the highest number of switchTypeValue switches within the provided timeframe.

    Params:
        - n (int): the total number of particles
        - switchValues (array of switchTypeValues): the switch type value of every particle at every timestep
        - startTime (int) [optional]: the first timestep to be included
        - endTime (int) [optional]: the last timestep to be included

    Returns:
        Integer representing the index of the particle with the highest number of switchTypeValue switches 
        as well as the number of switches performed by that particle.
    """
    switchers = findParticlesSwitchingValues(n, switchValues, startTime, endTime)
    maxSwitches = 0
    maxSwitchesIdx = 0
    for key, val in switchers.items():
        if len(val) > maxSwitches:
            maxSwitches = len(val)
            maxSwitchesIdx = key
    return maxSwitchesIdx, maxSwitches

def findNumberOfSwitchesForParticle(idx, n, switchValues, startTime=0, endTime=None):
    """
    Determines how often a particle has switched its switchTypeValue within the given timeframe.

    Params:
        - idx (int): the index of the particle
        - n (int): the total number of particles
        - switchValues (array of arrays of switchTypeValues): the switch type values for all particles at every timestep
        - startTime (int) [optional]: the first timestep to be included
        - endTime (int) [optional]: the last timestep to be included

    Returns:
        Integer representing the index of the particle, integer representing the number of switches performed.
    """
    switchers = findParticlesSwitchingValues(n, switchValues, startTime, endTime)
    return idx, len(switchers.get(idx))


def isCloseToOrder(orderValue):
    return orderValue >= 0.9

def isCloseToDisorder(orderValue):
    return orderValue <= 0.1

def getMinAvgMaxTransitionSpeedForMultipleRuns(simulationData, eventStartTimestep):
    transitionDurations = []
    for i in range(len(simulationData)):
        _, _, orientations = simulationData[i]
        speed = measureTransitionSpeed(orientations=orientations, eventStartTimestep=eventStartTimestep)
        if speed == -1:
            print(f"orientations for i = {i} does not transition")
        else:
            transitionDurations.append(speed)
    if len(transitionDurations) == 0:
        return -1, -1, -1
    return np.min(transitionDurations), np.average(transitionDurations), np.max(transitionDurations)

def measureTransitionSpeed(orientations, eventStartTimestep):
    orderBeforeEvent = ServiceMetric.computeOrder(orientations=orientations[eventStartTimestep-1])
    goToOrder = orderBeforeEvent <= 0.5 # if we're closer to disorder, we expect the transition to go towards order
    for t in range(eventStartTimestep, len(orientations)):
        order = ServiceMetric.computeOrder(orientations=orientations[t])
        if (goToOrder and isCloseToOrder(order)) or (not goToOrder and isCloseToDisorder(order)):
            return t-eventStartTimestep
    return -1