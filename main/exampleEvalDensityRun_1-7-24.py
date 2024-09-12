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


def eval(density, n, radius, eventEffect, metric, type, nsm=None, k=None, combo=None, evalInterval=1):
    xlim = (0, 15000)
    if metric in [Metrics.ORDER, Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE]:
        ylim = (0, 1.1)
    elif metric == Metrics.CLUSTER_NUMBER_WITH_RADIUS:
        ylim = (0, n)
    else:
        ylim = (0, 50)
   
    yAxisLabel = metric.label
    startEval = time.time()
    ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, combo={combo}, eventEffect={eventEffect.val}, metric={metric.name}, type={type}")
    modelParams = []
    simulationData = []
    colours = []
    switchTypes = []

    for initialStateString in ["ordered", "random"]:
        if type in ["nsmsw", "ksw"]:
            orderValue, disorderValue = combo
        if type == "nsmsw": 
            if initialStateString == "ordered":
                nsm = orderValue
            else:
                nsm = disorderValue
        elif type == "ksw": 
            if initialStateString == "ordered":
                k = orderValue
            else:
                k = disorderValue
        
        if type == "nosw":
            baseFilename = f"{baseDataLocation}local/switchingInactive/local_1e_nosw_{initialStateString}_st={nsm.value}__d={density}_n={n}_r={radius}_k={k}_noise=1_drn={duration}_{e1Start}-{eventEffect.val}"
        elif type == "nsmsw":
            baseFilename = f"{baseDataLocation}{levelDataLocation}local_1e_switchType=MODE_{initialStateString}_st={nsm.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{e1Start}-{eventEffect.val}"
        elif type == "ksw":
            baseFilename = f"{baseDataLocation}{levelDataLocation}local_1e_switchType=K_{initialStateString}_st={k}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={nsm.value}_noise={noisePercentage}_drn={duration}_{e1Start}-{eventEffect.val}"
        elif type == "global":
            baseFilename = f"E:/data/visek-data2/adaptive_radius/data/global/global_noev_nosw_d={density}_r={radius}_{initialStateString}_nsm={nsm.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
        
        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
        if type != "nosw":
            modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValues = ServiceSavedModel.loadModels(filenames, loadSwitchValues=True)
            switchTypes.append(switchTypeValues)
        else:
            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
        modelParams.append(modelParamsDensity)
        simulationData.append(simulationDataDensity)
        colours.append(coloursDensity)

#paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
    threshold = 0.01
    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold, switchTypeValues=switchTypes, switchTypeOptions=combo)
    
    labels = ["ordered", "disordered"]
    if metric == Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
        labels = ["ordered - order", "ordered - percentage of order-inducing value", "disordered - order", "disordered - percentage of order-inducing value"]
    if type == "nosw":
        savePath = f"{metric.val}_d={density}_n={n}_r={radius}_nosw_nsm={nsm.value}_k={k}_ee={eventEffect.val}.svg"
    elif type == "nsmsw":
        savePath = f"{metric.val}_d={density}_n={n}_r={radius}_swt=MODE_o={orderValue.value}_do={disorderValue.value}_k={k}_ee={eventEffect.val}.svg"
    elif type == "ksw":
        savePath = f"{metric.val}_d={density}_n={n}_r={radius}_swt=K_o={orderValue}_do={disorderValue}_nsm={nsm.value}_ee={eventEffect.val}.svg"
    elif type == "global":
        savePath = f"{metric.val}_d={density}_n={n}_r={radius}_global_nsm={nsm.value}_k={k}.svg"

    evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, colourBackgroundForTimesteps=[e1Start, e1Start+duration], showVariance=True, xlim=xlim, ylim=ylim, savePath=savePath)    
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
e2Start = 10000
e3Start = 15000

noisePercentages = [1] # to run again with other noise percentages, make sure to comment out anything that has fixed noise (esp. local)
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

saveLocation = f""
iStart = 1
iStop = 11

baseDataLocation = "D:/vicsek-data2/adaptive_radius/"

densities = [0.09, 0.05, 0.01]
radii = [20, 10, 5]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ LOCAL ---------------------------------------------------------------
levelDataLocation = "local/switchingActive/"

data = {}

ks = [1, 5]

# K VS. START
metrics = [
           Metrics.CLUSTER_NUMBER_WITH_RADIUS
           ]
xAxisLabel = "timesteps"
tmax = 15000

startTime = time.time()

duration = 1000

for density in densities:
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for radius in radii:
        for nsm in neighbourSelectionModes:
            for k in ks:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="global", nsm=nsm, k=k, evalInterval=interval)

        for nsm in neighbourSelectionModes:
            for k in ks:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="nosw", nsm=nsm, k=k, evalInterval=interval)

        
        for nsmCombo in [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
                         [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]:
            for k in ks:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="nsmsw", k=k, combo=nsmCombo, evalInterval=interval)
        
        for nsm in neighbourSelectionModes:
            for kCombo in [[5,1]]:
                for eventEffect in eventEffects:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=eventEffect, metric=metric, type="ksw", nsm=nsm, combo=kCombo, evalInterval=interval)
        
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

