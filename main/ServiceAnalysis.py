
"""
Service containing static methods that can be used for analysis.
"""

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