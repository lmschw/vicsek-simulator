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


dataLocation = "J:/kstaggering_old/"
saveLocation = "results_stagger/"
iStart = 1
iStop = 11

def eval(density, n, k, radius, eventEffect, metrics, type, nsm=None, combo=None, evalInterval=1, tmax=15000, duration=1000, noisePercentage=1, enforceSplit=True, percentageFirstValue=0):

    startEval = time.time()
    ServiceGeneral.logWithTime(f"d={density}, r={radius}, nsm={nsm}, type={type}, enforceSplit={enforceSplit}") 

    modelParams = []
    simulationData = []
    colours = []
    switchTypes = []

    for initialStateString in ["ordered", "random"]:
        baseFilename = f"{dataLocation}local_noev_nosw_kstaggering_es={enforceSplit}_pk0={percentageFirstValue}_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_tmax={tmax}_k={k}_noise={noisePercentage}"

        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="csv")
        #filenames = [f"{name}.csv" for name in filenames]
        filenamesModelParams = [f"{'.'.join(name.split('.')[:-1])}_modelParams.csv" for name in filenames]

        modelParamsDensity, simulationDataDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False,  fromCsv=True, modelParamsPaths=filenamesModelParams)
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
        
        evaluator = EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold, switchType=None, switchTypeValues=switchTypes, switchTypeOptions=combo)
        
        labels = ["ordered"]
        if metric == Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
            labels = ["ordered - order", "ordered - percentage of order-inducing value", "disordered - order", "disordered - percentage of order-inducing value"]
            labels = ["order", "percentage of order-inducing value"]
        savePath = f"{saveLocation}{metric.val}local_noev_nosw_kstaggering_es={enforceSplit}_pk0={percentageFirstValue}_{initialStateString}_st={nsm.value}_d={density}_n={n}_r={radius}_tmax={tmax}_k={k}_noise={noisePercentage}"

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

ks = [1,5]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

nsmCombos = [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
             [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]

kCombos = [[1,5]]

densities = [0.09]
radii = [10]
initialConditions = ["ordered", "random"]

evaluationInterval = 1

# K VS. START
metrics = [
           Metrics.ORDER
           ]
xAxisLabel = "timesteps"

noisePercentages = [1, 2, 3, 4, 5]

percentageFirstValue = 0.5

startTime = time.time()
startNoswnoev = time.time()
ServiceGeneral.logWithTime("Starting eval for nosw noev")
for noisePercentage in noisePercentages:
    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
    # ------------------------ FIXED STRATEGIES ---------------------------------
    enforceSplit = True
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
        for radius in radii:
            for nsm in nsmsReduced:
                eval(density=density, n=n, k=1, radius=radius, eventEffect=None, metrics=metrics, type="enfsplit", nsm=nsm,  
                    combo=None, evalInterval=evaluationInterval, tmax=tmax, noisePercentage=noisePercentage, percentageFirstValue=percentageFirstValue, enforceSplit=enforceSplit)
endNoswnoev = time.time()
ServiceGeneral.logWithTime(f"Completed eval for enforceSplit={enforceSplit} in {ServiceGeneral.formatTime(endNoswnoev-startNoswnoev)}")

for noisePercentage in noisePercentages:
    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
    # ------------------------ FIXED STRATEGIES ---------------------------------
    enforceSplit = False
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
        for radius in radii:
            for nsm in nsmsReduced:
                eval(density=density, n=n, k=1, radius=radius, eventEffect=None, metrics=metrics, type="prob", nsm=nsm,  
                    combo=None, evalInterval=evaluationInterval, tmax=tmax, noisePercentage=noisePercentage,percentageFirstValue=percentageFirstValue, enforceSplit=enforceSplit)
endNoswnoev = time.time()
ServiceGeneral.logWithTime(f"Completed eval for enforceSplit={enforceSplit} in {ServiceGeneral.formatTime(endNoswnoev-startNoswnoev)}")

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
    

