import collections
import numpy as np
import pandas as pd

import ServiceSavedModel
import ServiceGeneral
import ServiceMetric
import ServicePreparation
import EvaluatorMultiAvgComp

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumEventEffect import EventEffect

def printCounts(results):
    unique_elements, counts = np.unique(results, return_counts=True)
    for element, count in zip(unique_elements, counts):
        print(f"{element}: {count} times")

def getCount(counter, key):
    if key in counter.keys():
        return counter[key]
    return 0

nsms = [NeighbourSelectionMode.ALL,
        NeighbourSelectionMode.RANDOM,
        NeighbourSelectionMode.NEAREST,
        NeighbourSelectionMode.FARTHEST,
        NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
        NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

ks = [1, 5]

initialStates = ["ordered", "random"]
densities = [0.09, 0.05, 0.01]
radii = [20, 10, 5]
intervals = [50, 100, 150, 200]

domainSize = (50, 50)


dataLocationNoSw = "D:/vicsek-data2/adaptive_radius/local/switchingInactive/"
dataLocationSw = "D:/vicsek-data2/adaptive_radius/local/switchingActive/"

filenameNoSw = "local_1e_nosw_ordered_st=A__d=0.01_n=25_r=5_k=1_noise=1_drn=1000_5000-align_fixed_1.json"
filenameKSw = "local_1e_switchType=K_ordered_st=5_o=5_do=1_d=0.01_n=25_r=5_nsm=A_noise=1_drn=1000_5000-align_fixed_5.json"
filenameNsmSw = "local_1e_switchType=MODE_random_st=LOD_o=A_do=LOD_d=0.01_n=25_r=20_k=5_noise=1_drn=1000_5000-random_4.json"

eventEffect = EventEffect.ALIGN_TO_FIXED_ANGLE
startTimestep = 5000
duration = 1000
noisePercentage = 1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
fixedAngle = np.pi

iStart = 1
iStop = 11

intervalResults = {}
resultArray = []
for interval in intervals:
    overallResults = []
    
    ServiceGeneral.logWithTime(f"Starting interval {interval}")
    overallResults = []
    ServiceGeneral.logWithTime("STARTING NOSW")
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
        for radius in radii:
            results = []
            
            for initialState in initialStates:
                for nsm in nsms:
                    for k in ks:
                        for i in range(iStart, iStop):
                            filename = f"{dataLocationNoSw}local_1e_nosw_{initialState}_st={nsm.value}__d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{startTimestep}-{eventEffect.val}_{i}.json"
                            modelParams, simulationData, colours = ServiceSavedModel.loadModel(path=filename, loadSwitchValues=False)
                            times, positions, orientations = simulationData
                            result = ServiceMetric.checkTurnSuccess(orientations=orientations, fixedAngle=np.pi, noise=noise, eventStartTimestep=startTimestep, interval=interval)
                            #ServiceGeneral.logWithTime(f"turn success for d={density}, r={radius}, {initialState}, nsm={nsm.value}, k={k}, i={i}: {result}")
                            results.append(result)
                            resultArray.append([i, interval, 'nosw', density, radius, initialState, nsm.value, k, result])

            #print(results)
            overallResults.append(results)
            
            counter = collections.Counter(results)
            notNecessaryCount = getCount(counter, "not_necessary")
            turnedCount = getCount(counter, "turned")
            notTurnedCount = getCount(counter, "not_turned")

            ServiceGeneral.logWithTime(f"d={density}, r={radius}")
            ServiceGeneral.logWithTime(f"not_necessary: {notNecessaryCount}, not_turned: {notTurnedCount}, turned: {turnedCount}")
            
    """
    ServiceGeneral.logWithTime("STARTING KSW")
    kOrdered = 5
    kDisordered = 1
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
        for radius in radii:
            results = []
            for initialState in initialStates:
                if initialState == "ordered":
                    startVal = kOrdered
                else:
                    startVal = kDisordered
                for nsm in nsms:
                    for i in range(iStart, iStop):
                        #ServiceGeneral.logWithTime(f"evaluating turn success for d={density}, r={radius}, {initialState}, nsm={nsm.value}, k={k}, i={i}")
                        
                        filename = f"{dataLocationSw}local_1e_switchType=K_{initialState}_st={startVal}_o={kOrdered}_do={kDisordered}_d={density}_n={n}_r={radius}_nsm={nsm.value}_noise={noisePercentage}_drn={duration}_{startTimestep}-{eventEffect.val}_{i}.json"
                        modelParams, simulationData, colours = ServiceSavedModel.loadModel(path=filename, loadSwitchValues=False)
                        times, positions, orientations = simulationData
                        result = ServiceMetric.checkTurnSuccess(orientations=orientations, fixedAngle=np.pi, noise=noise, eventStartTimestep=startTimestep, interval=interval)
                        #ServiceGeneral.logWithTime(f"turn success for d={density}, r={radius}, {initialState}, nsm={nsm.value}, i={i}: {result}")
                        results.append(result)
                        resultArray.append([interval, 'ksw', density, radius, initialState, nsm.value, f"{kOrdered}-{kDisordered}", result])

            #print(results)
            overallResults.append(results)
            
            counter = collections.Counter(results)
            notNecessaryCount = getCount(counter, "not_necessary")
            turnedCount = getCount(counter, "turned")
            notTurnedCount = getCount(counter, "not_turned")

            ServiceGeneral.logWithTime(f"d={density}, r={radius}")
            ServiceGeneral.logWithTime(f"not_necessary: {notNecessaryCount}, not_turned: {notTurnedCount}, turned: {turnedCount}")
            

    
    
    ServiceGeneral.logWithTime("STARTING NSMSW")
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
        for radius in radii:
            results = []
            for nsmCombo in [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
                            [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]:
                orderVal, disorderVal = nsmCombo
                for initialState in initialStates:
                    if initialState == "ordered":
                        startVal = orderVal
                    else:
                        startVal = disorderVal
                    for k in ks:
                        for i in range(iStart, iStop):
                            #ServiceGeneral.logWithTime(f"evaluating turn success for d={density}, r={radius}, {initialState}, nsm={nsm.value}, k={k}, i={i}")
                            filename = f"{dataLocationSw}local_1e_switchType=MODE_{initialState}_st={startVal.value}_o={orderVal.value}_do={disorderVal.value}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{startTimestep}-{eventEffect.val}_{i}.json"
                            modelParams, simulationData, colours = ServiceSavedModel.loadModel(path=filename, loadSwitchValues=False)
                            times, positions, orientations = simulationData
                            result = ServiceMetric.checkTurnSuccess(orientations=orientations, fixedAngle=np.pi, noise=noise, eventStartTimestep=startTimestep, interval=interval)
                            #ServiceGeneral.logWithTime(f"turn success for d={density}, r={radius}, nsmCombo=({orderVal.value}, {disorderVal.value}) {initialState}, k={k}, i={i}: {result}")
                            results.append(result)
                            resultArray.append([interval, 'nsmsw', density, radius, initialState, f"{orderVal.value}-{disorderVal.value}", k, result])

            #print(results)
            overallResults.append(results)
    intervalResults[interval] = overallResults
"""    



df = pd.DataFrame(resultArray, columns=["i", "interval", "switchtype", "density", "radius", "initialState", "nsm", "k", "result"])
df.to_csv("turn_successes_nosw.csv")

for interval in intervals:
    ServiceGeneral.logWithTime(f"Overall results - {interval}:")
    printCounts(intervalResults[interval])