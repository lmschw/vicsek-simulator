import time
import numpy as np

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect

from EvaluatorMultiAvgComp import EvaluatorMultiAvgComp
import ServiceSavedModel as ServiceSavedModel
import ServicePreparation as ServicePreparation
import ServiceGeneral as ServiceGeneral


dataLocation = "J:/noise2/"
saveLocation = "results_noise/"
iStart = 1
iStop = 11

def eval(density, n, radius, eventEffect, metrics, type, nsm=None, k=None, combo=None, evalInterval=1, tmax=15000, duration=1000, noisePercentage=1):

    startEval = time.time()
    if type in ["noswnoev", "nsmswnoev", "kswnoev"]:
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, type={type}") 
    else:
        ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, k={k}, combo={combo}, eventEffect={eventEffect.val}, type={type}")
    modelParams = []
    simulationData = []
    colours = []
    switchTypes = []

    for initialStateString in ["ordered", "random"]:
        if type in ["nsmswnoev", "nsmsw", "kswnoev", "ksw"]:
            orderValue, disorderValue = combo
        if type in ["nsmswnoev", "nsmsw"]: 
            if initialStateString == "ordered":
                nsm = orderValue
            else:
                nsm = disorderValue
        elif type in ["kswnoev", "ksw"]: 
            if initialStateString == "ordered":
                k = orderValue
            else:
                k = disorderValue

        if type == "noswnoev":
            baseFilename = f"{dataLocation}global_noev_nosw_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_tmax={tmax}_k={k}_noise={noisePercentage}"
            sTypes = []
        elif type == "nosw":
            baseFilename = f"{dataLocation}local_nosw_1ev_d={density}_r={radius}_{initialStateString}_nsm={nsm.value}_k={k}_ee={eventEffect.val}"
            sTypes = []
        elif type == "nsmswnoev":
            baseFilename = f"{dataLocation}local_nsmsw_noev_d={density}_r={radius}_{initialStateString}_st={nsm.value}_nsmCombo={combo[0].value}-{combo[1].value}_k={k}"
            sTypes = [SwitchType.NEIGHBOUR_SELECTION_MODE]
        elif type == "nsmsw":
            baseFilename = f"{dataLocation}local_nsmsw_1ev_d={density}_r={radius}_{initialStateString}_st={nsm.value}_nsmCombo={combo[0].value}-{combo[1].value}_k={k}_ee={eventEffect.val}"
            sTypes = [SwitchType.NEIGHBOUR_SELECTION_MODE]
        elif type == "kswnoev":
            baseFilename = f"{dataLocation}local_ksw_noev_d={density}_r={radius}_{initialStateString}_st={k}_nsm={nsm.value}_kCombo={combo[0]}-{combo[1]}"
            sTypes = [SwitchType.K]
        elif type == "ksw":
            baseFilename = f"{dataLocation}local_ksw_1ev_d={density}_r={radius}_{initialStateString}_st={k}_nsm={nsm.value}_kCombo={combo[0]}-{combo[1]}_ee={eventEffect.val}"
            sTypes = [SwitchType.K]

        
        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="csv")
        filenamesModelParams = [f"{'.'.join(name.split('.')[:-1])}_modelParams.csv" for name in filenames]
        if type not in ["nosw", "noswnoev"]:
            modelParamsDensity, simulationDataDensity, switchTypeValues = ServiceSavedModel.loadModels(filenames, modelParamsPaths=filenamesModelParams, loadSwitchValues=True, fromCsv=True)
            switchTypes.append([switchTypeValues[0][sTypes[0].switchTypeValueKey]])
        else:
            modelParamsDensity, simulationDataDensity = ServiceSavedModel.loadModels(filenames,modelParamsPaths=filenamesModelParams, loadSwitchValues=False, fromCsv=True)
        modelParams.append(modelParamsDensity)
        simulationData.append(simulationDataDensity)

#paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
    
    for metric in metrics:
        ServiceGeneral.logWithTime(f"Starting metric = {metric.val}")
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
        threshold = 0.01

        if len(sTypes) > 0:
            sType = sTypes[0]
        else:
            sType = None
        
        evaluator = EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold, switchTypeValues=switchTypes, switchTypeOptions=combo)
        
        labels = ["ordered", "random"]
        if metric == Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
            labels = ["ordered - order", "ordered - percentage of order-inducing value", "disordered - order", "disordered - percentage of order-inducing value"]
            labels = ["order", "percentage of order-inducing value"]
        if type == "noswnoev":
            savePath = f"{saveLocation}{metric.val}_local_nosw_noev_d={density}_r={radius}_nsm={nsm.value}_k={k}_noise={noisePercentage}.svg"
        elif type == "nosw":
            savePath = f"{saveLocation}{metric.val}_local_nosw_1ev_d={density}_r={radius}_nsm={nsm.value}_k={k}_ee={eventEffect.val}.svg"
        elif type == "nsmswnoev":
            savePath = f"{saveLocation}{metric.val}_local_nsmsw_noev_d={density}_r={radius}_st={nsm.value}_nsmCombo={combo[0].value}-{combo[1].value}_k={k}.svg"
        elif type == "nsmsw":
            savePath = f"{saveLocation}{metric.val}_local_nsmsw_1ev_d={density}_r={radius}_st={nsm.value}_nsmCombo={combo[0].value}-{combo[1].value}_k={k}_ee={eventEffect.val}.svg"
        elif type == "kswnoev":
            savePath = f"{saveLocation}{metric.val}_local_ksw_noev_d={density}_r={radius}_st={k}_nsm={nsm.value}_kCombo={combo[0]}-{combo[1]}.svg"
        elif type == "ksw":
            savePath = f"{saveLocation}{metric.val}_local_ksw_1ev_d={density}_r={radius}_st={k}_nsm={nsm.value}_kCombo={combo[0]}-{combo[1]}_ee={eventEffect.val}.svg"

        evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, colourBackgroundForTimesteps=[eventStart, eventStart+duration], showVariance=True, xlim=xlim, ylim=ylim, savePath=savePath)    
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
# GENERAL
domainSize = (50, 50)
noisePercentage = 1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
speed = 1
initialAngleX = 0.5
initialAngleY = 0.5
colourType = None
degreesOfVision = 2 * np.pi

tmax = 15000

# SWITCHING
threshold = [0.1]
numberOfPreviousSteps = 100
updateIfNoNeighbours = False

# EVENT
eventStart = 5000
eventDuration = 100
eventDistributionType = DistributionType.LOCAL_SINGLE_SITE
eventAngle = np.pi
eventNumberAffected = None

# TEST VALS
nsms = [NeighbourSelectionMode.ALL,
        NeighbourSelectionMode.RANDOM,
        NeighbourSelectionMode.NEAREST,
        NeighbourSelectionMode.FARTHEST,
        NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
        NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

nsmsReduced = [NeighbourSelectionMode.NEAREST,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

ks = [1]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

nsmCombos = [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
             [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]

kCombos = [[1,5]]

densities = [0.09, 0.01, 0.12]
radii = [10]
initialConditions = ["ordered", "random"]

evaluationInterval = 1

# K VS. START
metrics = [
           Metrics.ORDER
           ]
xAxisLabel = "timesteps"

noisePercentages = [1,4]

startTime = time.time()
startNoswnoev = time.time()
ServiceGeneral.logWithTime("Starting eval for nosw noev")
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    for radius in radii:
        for noisePercentage in noisePercentages:
            for nsm in nsmsReduced:
                for k in ks:
                    eval(density=density, n=n, radius=radius, eventEffect=None, metrics=metrics, type="noswnoev", nsm=nsm, k=k, 
                        combo=None, evalInterval=evaluationInterval, tmax=tmax, noisePercentage=noisePercentage)
endNoswnoev = time.time()
ServiceGeneral.logWithTime(f"Completed eval for nosw noev in {ServiceGeneral.formatTime(endNoswnoev-startNoswnoev)}")

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

