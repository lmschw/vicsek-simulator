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


def eval(density, n, radius, eventEffect, metric, type, nsm=None, k=None, combo=None, evalInterval=1, tmax=15000):
    xlim = (0, tmax)
    threshold = 0.01
    if metric in [Metrics.ORDER, Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE]:
        ylim = (0, 1.1)
    elif metric == Metrics.CLUSTER_NUMBER_WITH_RADIUS:
        ylim = (0, n)
        threshold = 0.995
    else:
        ylim = (0, 50)
   
    yAxisLabel = metric.label
    startEval = time.time()
    ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, metric={metric.name}, type={type}") 
    modelParams = []
    simulationData = []
    switchTypes = []

    for initialStateString in ["ordered", "random"]:
        baseFilename = f"{baseDataLocation}{levelDataLocation}global_nosw_noev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={nsm.value}_k={k}_noise={noisePercentage}_speed={speed}"
        
        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")

        modelParamsDensity, simulationDataDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False, fromCsv=False)
        modelParams.append(modelParamsDensity)
        simulationData.append(simulationDataDensity)

#paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
    threshold = 0.01
    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold, switchTypeValues=switchTypes, switchTypeOptions=combo)
    
    labels = ["ordered", "disordered"]
    if metric == Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
        labels = ["ordered - order", "ordered - percentage of order-inducing value", "disordered - order", "disordered - percentage of order-inducing value"]

    saveLocation = "results_noise_global/"
    savePath = f"{saveLocation}{metric.val}_d={density}_n={n}_r={radius}_global_nsm={nsm.value}_k={k}_th={threshold}_noise={noisePercentage}.svg"

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

baseDataLocation = "J:/noise_global/"

densities = [0.09]
radii = [10]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ LOCAL ---------------------------------------------------------------
levelDataLocation = ""

data = {}

ks = [1,5]

# K VS. START
metrics = [
           Metrics.ORDER
           ]
xAxisLabel = "timesteps"


startTime = time.time()

duration = 1000

for density in densities:
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for radius in radii:
        tmax = 3000
        iStop = 2
        for nsm in neighbourSelectionModes:
            for k in [1]:
                    for metric in metrics:
                        eval(density=density, n=n, radius=radius, eventEffect=None, metric=metric, type="global", nsm=nsm, k=k, evalInterval=interval, tmax=tmax)

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

