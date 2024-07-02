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
e2Start = 10000
e3Start = 15000

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
iStop = 11

baseDataLocation = "D:/vicsek-data2/adaptive_radius"

densities = [0.01, 0.05]
radii = [5, 10, 20]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ GLOBAL ---------------------------------------------------------------
levelDataLocation = "global"

data = {}
density = 0.01
radius = 5
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))

# K VS. START
yLabels = ["ordered", "disordered"]
yAxisLabel = "starting condition"
xLabels = ks
xAxisLabel = "neighbourhood size"
index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

metric = Metrics.ORDER
startTime = time.time()
for i, k in enumerate(ks):
    for j, initialStateString in enumerate(["ordered", "random"]): 
            startEval = time.time()
            print(f"k={k}, density={density}")
            modelParams = []
            simulationData = []
            colours = []

            for neighbourSelectionMode in neighbourSelectionModes:
                baseFilename = f"{baseDataLocation}/{levelDataLocation}/global_noev_nosw_d={density}_r={radius}_{initialStateString}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)

        #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
            threshold = 0.01
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
            stepData = evaluator.evaluate()    
            data[f"{i}-{j}"] = stepData    
            endEval = time.time()
            print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_k-vs-density_ordered.svg", xlim=(0,1000), ylim=(0,1.1))
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
            
    
    
"""
    radius = ServicePreparation.getRadiusToSeeOnAverageNNeighbours(kMax, density)
    # GLOBAL - COMPARE K FOR MODES WITHOUT SWITCH
    tmax = 5000
    for metric in [Metrics.ORDER]:
        yLabel = metric.label
        for density in [0.01, 0.05]:
            n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
            for radius in [5, 10, 20]:
                for initialStateString in ["ordered", "random"]:
                    startRun = time.time()
                    #labels = getLabelsFromNeighbourSelectionModes([neighbourSelectionMode])
                    subtitle = f"d={density}, r={radius}"
                    modelParams = []
                    simulationData = []
                    colours = []
                    labels = []
                
                    if initialStateString == "random":
                        labelStr = "disordered"
                    else:
                        labelStr = "ordered"
                    for neighbourSelectionMode in neighbourSelectionModes:
                        for k in ks:
                            labels.append(f"nsm={neighbourSelectionMode.name}, k={k}, start={labelStr}")
                            baseFilename = f"{baseDataLocation}/{levelDataLocation}/global_noev_nosw_d={density}_r={radius}_{initialStateString}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)

                    savePath = f"global_{metric.label}_d={density}_r={radius}_{initialStateString}_n={n}_noise={noisePercentage}.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle,savePath=savePath)
                
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed 'GLOBAL - COMPARE K FOR MODES WITHOUT SWITCH', noise = {noisePercentage}%, nsm={neighbourSelectionMode.name}, init = {initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")
"""
