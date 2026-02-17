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

saveInterval = 5


def eval(density, n, radius, eventEffect, metric, type, noisePercentage=1, nsm=None, k=None, combo=None, evalInterval=1, tmax=15000, fontsize=20):
    startEval = time.time()
    if type == "global":
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, metric={metric.name}, type={type}") 
    else:
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, combo={combo}, eventEffect={eventEffect.val}, metric={metric.name}, type={type}")

    for initialStateString in ["ordered", "random"]:
        if type in ["nsmsw", "ksw"]:
            orderValue, disorderValue = combo
        if type == "nsmsw": 
            if initialStateString == "ordered":
                nsm = disorderValue
            else:
                nsm = orderValue
        elif type == "ksw": 
            if initialStateString == "ordered":
                k = orderValue
            else:
                k = disorderValue
        
        if type == "nosw":
            filePath = f"local_nosw_1ev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={nsm.value}_k={k}_ee={eventEffect.val}"
        elif type == "nsmsw":
            filePath = f"local_nsmsw_1ev_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_nsmCombo={disorderValue.value}-NeighbourSelectionMechanism.{orderValue.name}_k={k}_ee={eventEffect.val}"
        elif type == "ksw":
            filePath = f"local_ksw_1ev_{initialStateString}_st={k}_d={density}_n={n}_r={radius}_nsm={nsm.value}_kCombo={orderValue}-{disorderValue}_ee={eventEffect.val}"
        elif type == "global":
            filePath = f"global_nosw_noev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={nsm.value}_k={k}"
        baseFilename = f"{baseDataLocation}{levelDataLocation}{filePath}"
        
        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
        if type not in ["nosw", "global"]:
            for i in range(len(filenames)):
                modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValues = ServiceSavedModel.loadModel(filenames[i], loadSwitchValues=True)
                ServiceSavedModel.saveModel(simulationData=simulationDataDensity,
                                    colours=coloursDensity,
                                    path=f"E:/data/new/thinned/{filePath}_i.json",
                                    modelParams=modelParamsDensity,
                                    saveInterval=saveInterval,
                                    switchValues=switchTypeValues)
        else:
            for i in range(len(filenames)):
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(filenames[i], loadSwitchValues=False)

                ServiceSavedModel.saveModel(simulationData=simulationDataDensity,
                                    path=f"E:/data/new/thinned/{filePath}_i.json",
                                    colours=coloursDensity,
                                    modelParams=modelParamsDensity,
                                    saveInterval=saveInterval)




    endEval = time.time()
    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 


def getLabelsFromNoisePercentages(noisePercentages):
    return [f"{noisePercentage}% noise" for noisePercentage in noisePercentages]

def getLabelsFromKValues(ks):
    return [f"k={k}" for k in ks]

def getLabelsFromNeighbourSelectionModes(neighbourSelectionModes):
    return [neighbourSelectionMode.name for neighbourSelectionMode in neighbourSelectionModes]

def getLabelsFromEventEffects(eventEffects):
    return [eventEffect.label for eventEffect in eventEffects]

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
e2Start = 10000
e3Start = 15000

noisePercentages = [1,4] # to run again with other noise percentages, make sure to comment out anything that has fixed noise (esp. local)
densities = [0.01]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
ks = [1,5]

neighbourSelectionModes = [
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM
                           ]

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

saveLocation = f"results_big_font/"
iStart = 1
iStop = 11

baseDataLocation = "E:/data/new/"

densities = [0.09]
radii = [10]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ LOCAL ---------------------------------------------------------------
levelDataLocation = ""

data = {}

ks = [1, 5]

# K VS. START
metrics = [
           Metrics.ORDER
           ]
xAxisLabel = "timesteps"


startTime = time.time()

duration = 1000
tmax = 15000

radius = 10

for density in densities:
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for noisePercentage in noisePercentages:
        
        for nsm in neighbourSelectionModes:
            for k in ks:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=None, metric=metric, type="global", nsm=nsm, k=k, evalInterval=interval, tmax=tmax)
        
        ks = [1,5]
        for nsm in neighbourSelectionModes:
            for k in ks:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="nosw", nsm=nsm, k=k, evalInterval=interval, tmax=tmax)
        
        
        for nsmCombo in [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST]]:
            for k in [1]:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="nsmsw", k=k, combo=nsmCombo, evalInterval=interval, tmax=tmax)
        
        for nsm in [NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]:
            for kCombo in [[5,1]]:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="ksw", nsm=nsm, combo=kCombo, evalInterval=interval, tmax=tmax)

        # for nsm in neighbourSelectionModes:
        #     for k in ks:
        #             for metric in metrics:
        #                 eval(density=density, n=n, radius=radius, eventEffect=None, metric=metric, type="global", nsm=nsm, k=k, evalInterval=interval, tmax=tmax, noisePercentage=noisePercentage)
        
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

