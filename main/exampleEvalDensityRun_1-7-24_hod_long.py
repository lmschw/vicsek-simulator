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
    if type in ["global", "nsmswnoev", "kswnoev"]:
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, metric={metric.name}, type={type}") 
    else:
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, combo={combo}, eventEffect={eventEffect.val}, metric={metric.name}, type={type}")
    modelParams = []
    simulationData = []
    colours = []
    switchTypes = []

    for initialStateString in ["random"]:
        if type in ["nsmsw", "nsmswnoev", "ksw", "kswnoev"]:
            disorderValue, orderValue = combo
        if type == "nsmsw" or type == "nsmswnoev": 
            if initialStateString == "ordered":
                nsm = orderValue
            else:
                nsm = disorderValue
        elif type == "ksw" or type == "kswnoev": 
            if initialStateString == "ordered":
                k = orderValue
            else:
                k = disorderValue
        
        if type == "nosw":
            baseFilename = f"{baseDataLocation}local_nosw_1ev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={nsm.value}_k={k}_ee={eventEffect.val}"
        elif type == "nsmsw":
            baseFilename = f"{baseDataLocation}local_nsmsw_1ev_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_nsmCombo={disorderValue.value}-{orderValue.value}_k={k}_ee={eventEffect.val}"
        elif type == "nsmswnoev":
            baseFilename = f"{baseDataLocation}local_nsmsw_noev_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_nsmCombo={disorderValue.value}-{orderValue}_k={k}"
        elif type == "ksw":
            baseFilename = f"{baseDataLocation}local_ksw_1ev_{initialStateString}_st={k}_d={density}_n={n}_r={radius}_nsm={nsm.value}_kCombo={disorderValue}-{orderValue}_ee={eventEffect.val}"
        elif type == "kswnoev":
            baseFilename = f"{baseDataLocation}local_ksw_noev_{initialStateString}_st={k}_d={density}_n={n}_r={radius}_nsm={nsm.value}_kCombo={orderValue}-{disorderValue}"
        elif type == "global":
            baseFilename = f"{baseDataLocation}global_nosw_noev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={nsm.value}_k={k}_tmax=10000000"
        
        baseFilename = baseFilename.replace("NeighbourSelectionMode", "NeighbourSelectionMechanism")
        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="csv")
        #if type not in ["nosw", "global"]:
            #modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValues = ServiceSavedModel.loadModels(filenames, loadSwitchValues=True)
            #switchTypes.append(switchTypeValues)
        #else:
        modelParamsPaths = [f"{name}_modelParams.csv" for name in filenames]
        filenames = [f"{name}.csv" for name in filenames]
        
        modelParamsDensity, simulationDataDensity = ServiceSavedModel.loadModels(filenames, modelParamsPaths=modelParamsPaths, loadSwitchValues=False, fromCsv=True)
        modelParams.append(modelParamsDensity)
        simulationData.append(simulationDataDensity)

#paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
    threshold = 0.01
    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold, switchTypeValues=switchTypes, switchTypeOptions=combo)
    
    saveLocationPlot = ""
    labels = ["ordered"]
    if metric == Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
        labels = ["ordered - order", "ordered - percentage of order-inducing value", "disordered - order", "disordered - percentage of order-inducing value"]

    savePath = f"{saveLocationPlot}hod_long_d={density}_n={n}_r={radius}_k={k}"
    evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, colourBackgroundForTimesteps=[e1Start, e1Start+duration], showVariance=False, xlim=xlim, ylim=ylim, savePath=savePath)    
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
densities = [0.025]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
ks = [1]

neighbourSelectionModes = [

                            NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,

                           ]
reducedNeighbourSelectionModes = [
                                NeighbourSelectionMode.NEAREST,
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
iStop = 3

baseDataLocation = "G:/hod_long/"

densities = [0.09]
radii = [10]
interval = 1000
kMax = 5
noisePercentage = 1

# ------------------------------------------------ LOCAL ---------------------------------------------------------------
levelDataLocation = ""

data = {}

ks = [1]

# K VS. START
metrics = [
           Metrics.ORDER,
           ]
xAxisLabel = "timesteps"


startTime = time.time()

duration = 1000

for density in densities:
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for radius in radii:
        
        
        tmax = 10_000_000
        for nsm in neighbourSelectionModes:
            for k in ks:
                for metric in metrics:
                    eval(density=density, n=n, radius=radius, eventEffect=None, metric=metric, type="global", nsm=nsm, k=k, evalInterval=interval, tmax=tmax)
        
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

