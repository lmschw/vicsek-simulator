def findParticlesSwitchingValues(n, switchValues, startTime=0, endTime=None):
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
    switchers = findParticlesSwitchingValues(n, switchValues, startTime, endTime)
    maxSwitches = 0
    maxSwitchesIdx = 0
    for key, val in switchers.items():
        if len(val) > maxSwitches:
            maxSwitches = len(val)
            maxSwitchesIdx = key
    return maxSwitchesIdx, maxSwitches

def findNumberOfSwitchesForParticle(idx, n, switchValues, startTime=0, endTime=None):
    switchers = findParticlesSwitchingValues(n, switchValues, startTime, endTime)
    return idx, len(switchers.get(idx))