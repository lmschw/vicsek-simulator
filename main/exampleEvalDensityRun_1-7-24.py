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
iStop = 2

baseDataLocation = "D:/vicsek-data2/adaptive_radius"

densities = [0.05]
radii = [10]
interval = 1
kMax = 5
noisePercentage = 1

# ------------------------------------------------ GLOBAL ---------------------------------------------------------------
levelDataLocation = "global"

data = {}

ks = [0, 1, 2, 3, 4, 5, 10]

# K VS. START

xLabelPlot = "time steps"
yLabelPlot = "order"

xLabelsOuter = radii
xAxisLabelOuter = "radius" 

xLabelsInner = ["ordered", "disordered"]
xAxisLabelInner = "starting condition"

yLabelsOuter = densities
yAxisLabelOuter = "density"

yLabelsInner = getLabelsFromKValues(ks)
yAxisLabelInner = "neighbourhood size"

index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)


tmax = 3000
metric = Metrics.ORDER
startTime = time.time()

for a, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for b, radius in enumerate(radii):
        subdata = {}
        for i, k in enumerate(ks):
            for j, initialStateString in enumerate(["ordered", "random"]): 
                    startEval = time.time()
                    print(f"d={density}, r={radius}, k={k}, init={initialStateString}")
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
                    subdata[f"{i}-{j}"] = stepData    
                    endEval = time.time()
                    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
        data[f"{a}-{b}"] = subdata   

ServiceImages.createMatrixOfPlotsFromScratch(
                                             xLabelPlot=xLabelPlot,
                                             yLabelPlot=yLabelPlot,
                                             xLabelOuter=xLabelsOuter,
                                             xLabelInner=xLabelsInner,
                                             yLabelOuter=yLabelsOuter, 
                                             yLabelInner=yLabelsInner, 
                                             data=data, index=index, 
                                             xAxisLabelOuter=xAxisLabelOuter, 
                                             xAxisLabelInner=xAxisLabelInner,
                                             yAxisLabelOuter=yAxisLabelOuter,
                                             yAxisLabelInner=yAxisLabelInner, 
                                             savePath="order_k-comp.svg", xlim=(0,tmax), ylim=(0,1.1))
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
            
# -------------- LOCAL ------------------
levelDataLocation = "global"

data = {}

# K VS. START

xLabelPlot = "time steps"
yLabelPlot = "order"

xLabelsOuter = radii
xAxisLabelOuter = "radius" 

xLabelsInner = ["ordered", "disordered"]
xAxisLabelInner = "starting condition"

yLabelsOuter = densities
yAxisLabelOuter = "density"

yLabelsInner = getLabelsFromKValues(ks)
yAxisLabelInner = ""

index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

tmax = 3000
metric = Metrics.ORDER
startTime = time.time()

for a, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for b, radius in enumerate(radii):
        subdata = {}
        for i, k in enumerate(ks):
            for j, initialStateString in enumerate(["ordered", "random"]): 
                    startEval = time.time()
                    print(f"d={density}, r={radius}, k={k}, init={initialStateString}")
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
                    subdata[f"{i}-{j}"] = stepData    
                    endEval = time.time()
                    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
        data[f"{a}-{b}"] = subdata   

ServiceImages.createMatrixOfPlotsFromScratch(
                                             xLabelPlot=xLabelPlot,
                                             yLabelPlot=yLabelPlot,
                                             xLabelOuter=xLabelsOuter,
                                             xLabelInner=xLabelsInner,
                                             yLabelOuter=yLabelsOuter, 
                                             yLabelInner=yLabelsInner, 
                                             data=data, index=index, 
                                             xAxisLabelOuter=xAxisLabelOuter, 
                                             xAxisLabelInner=xAxisLabelInner,
                                             yAxisLabelOuter=yAxisLabelOuter,
                                             yAxisLabelInner=yAxisLabelInner, 
                                             savePath="order_k-comp.svg", xlim=(0,tmax), ylim=(0,1.1))
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
            
    
   
    

