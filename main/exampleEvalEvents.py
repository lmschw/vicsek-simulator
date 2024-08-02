import time
import numpy as np

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

import EvaluatorMultiAvgComp
import ServiceSavedModel
import ServicePreparation
import ServiceGeneral
import ServiceImages
import ServiceMetric

import DefaultValues as dv
import AnimatorMatplotlib
import Animator2D


def getLabelsFromNoisePercentages(noisePercentages):
    return [f"{noisePercentage}% noise" for noisePercentage in noisePercentages]

def getLabelsFromKValues(ks):
    return [f"k={k}" for k in ks]

def getLabelsFromNeighbourSelectionModes(neighbourSelectionModes):
    return [neighbourSelectionMode.name for neighbourSelectionMode in neighbourSelectionModes]

def getLabelsFromEventEffects(eventEffects):
    return [eventEffect.label for eventEffect in eventEffects]

def getOrderDisorderValue(switchType):
    match switchType:
        case SwitchType.K:
            return 5, 1
        case SwitchType.NEIGHBOUR_SELECTION_MODE:
            return NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST


xLabel = "time steps"

speed = 1

angle = np.pi
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]


#domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.09, 100)
domainSize = (50, 50)

distTypeString = "lssmid"
distributionType = DistributionType.LOCAL_SINGLE_SITE
percentage = 100
movementPattern = MovementPattern.STATIC
e1Start = 5000


noisePercentages = [1] # to run again with other noise percentages, make sure to comment out anything that has fixed noise (esp. local)
densities = [0.01]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
ks = [1,5]

neighbourSelectionModes = [NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

orderNeighbourSelectionModes = [NeighbourSelectionMode.ALL,
                                NeighbourSelectionMode.RANDOM,
                                NeighbourSelectionMode.FARTHEST,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

disorderNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                                   NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

localNeighbourSelectionmodes = [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]

saveLocation = f""
iStart = 1
iStop = 2

baseDataLocation = "D:/vicsek-data2/adaptive_radius/"

densities = [0.05]
radii = [10]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ GLOBAL ---------------------------------------------------------------
levelDataLocation = "local/switchingActive/"

data = {}

ks = [1, 5]

# MODE
index = ["ordered", "disordered"]
duration = 1000
tmax = 15000
metric = Metrics.ORDER
startTime = time.time()

for a, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for b, radius in enumerate(radii):
        for nsmOrder in orderNeighbourSelectionModes:
            for nsmDisorder in disorderNeighbourSelectionModes:
                subdata = {}
                for k in k:
                    for eventEffect in eventEffects:
                        startEval = time.time()
                        print(f"d={density}, r={radius}, k={k}, init={initialStateString}")
                        modelParams = []
                        simulationData = []
                        colours = []

                        for initialStateString in ["ordered", "random"]:
                            if initialStateString == "ordered":
                                startValue = nsmOrder
                            else:
                                startValue = nsmDisorder
                            baseFilename = f"{baseDataLocation}{levelDataLocation}local_1e_switchType=MODE_{initialStateString}_st={startValue.value}_o={nsmOrder.value}_do={nsmDisorder.value}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{e1Start}-{eventEffect.val}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)

                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
                        savePath = f"order_event_nsmsw_d={density}_r={radius}_o={nsmOrder.value}_do={nsmDisorder.value}_k={k}.svg"
                        evaluator.evaluateAndVisualize(labels=["ordered", "disordered"], xLabel="timesteps", yLabel="order", colourBackgroundForTimesteps=(e1Start, e1Start+duration), savePath=savePath)    
                        endEval = time.time()
                        print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    
# K
index = ["ordered", "disordered"]
duration = 1000
tmax = 15000
metric = Metrics.ORDER
startTime = time.time()

for a, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for b, radius in enumerate(radii):
        for kOrder in [5]:
            for kDisorder in [1]:
                subdata = {}
                for nsm in neighbourSelectionModes:
                    for eventEffect in eventEffects:
                        startEval = time.time()
                        print(f"d={density}, r={radius}, k={k}, init={initialStateString}")
                        modelParams = []
                        simulationData = []
                        colours = []

                        for initialStateString in ["ordered", "random"]:
                            if initialStateString == "ordered":
                                startValue = kOrder
                            else:
                                startValue = kDisorder
                            baseFilename = f"{baseDataLocation}{levelDataLocation}local_1e_switchType=K_{initialStateString}_st={startValue}_o={kOrder}_do={kDisorder}_d={density}_n={n}_r={radius}_nsm={nsm.value}_noise={noisePercentage}_drn={duration}_{e1Start}-{eventEffect.val}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)

                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
                        savePath = f"order_event_ksw_d={density}_r={radius}_o={kOrder}_do={kDisorder}_nsm={nsm.value}.svg"
                        evaluator.evaluateAndVisualize(labels=["ordered", "disordered"], xLabel="timesteps", yLabel="order", colourBackgroundForTimesteps=(e1Start, e1Start+duration), savePath=savePath)    
                        endEval = time.time()
                        print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    
# No SWITCH
levelDataLocation = "local/switchingInactive/"
index = ["ordered", "disordered"]
duration = 1000
tmax = 15000
metric = Metrics.ORDER
startTime = time.time()

for a, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for b, radius in enumerate(radii):
        
        for nsm in neighbourSelectionModes:
                startValue = nsm
                for k in ks:
                    for eventEffect in eventEffects:
                        startEval = time.time()
                        print(f"d={density}, r={radius}, k={k}, init={initialStateString}")
                        modelParams = []
                        simulationData = []
                        colours = []

                        for initialStateString in ["ordered", "random"]:
                            baseFilename = f"{baseDataLocation}{levelDataLocation}local_1e_nosw_{initialStateString}_st={startValue.value}__d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{e1Start}-{eventEffect.val}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)

                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
                        savePath = f"order_event_nosw_d={density}_r={radius}_nsm={nsm.value}_k={k}.svg"
                        evaluator.evaluateAndVisualize(labels=["ordered", "disordered"], xLabel="timesteps", yLabel="order", colourBackgroundForTimesteps=(e1Start, e1Start+duration), savePath=savePath)    
                        endEval = time.time()
                        print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    