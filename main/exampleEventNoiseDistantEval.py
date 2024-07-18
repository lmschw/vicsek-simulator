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

nsmLabels = {NeighbourSelectionMode.ALL: "All",
             NeighbourSelectionMode.RANDOM: "Random",
             NeighbourSelectionMode.NEAREST: "Nearest",
             NeighbourSelectionMode.FARTHEST: "Farthest",
             NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE: "Least Orientation Difference",
             NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE: "Highest Orientation Difference"}

eventLabels = {EventEffect.ALIGN_TO_FIXED_ANGLE: "Distant",
               EventEffect.AWAY_FROM_ORIGIN: "Predator",
               EventEffect.RANDOM: "Random"}

def getLabelsFromNoisePercentages(noisePercentages):
    return [f"{noisePercentage}% noise" for noisePercentage in noisePercentages]

def getLabelsFromKValues(ks):
    return [f"k={k}" for k in ks]

def getLabelsFromNeighbourSelectionModes(neighbourSelectionModes):
    return [nsmLabels.get(neighbourSelectionMode) for neighbourSelectionMode in neighbourSelectionModes]

def getLabelsFromEventEffects(eventEffects):
    return [eventLabels.get(eventEffect) for eventEffect in eventEffects]

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
ks = [1]

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
iStop = 2 # here

baseDataLocation = "D:/vicsek-data2/adaptive_radius"

densities = [0.01, 0.05]
radii = [5, 10, 20]
interval = 1
kMax = 5
noisePercentage = 1

fontsize = 13


# ------------------------------------------------ GLOBAL ---------------------------------------------------------------
levelDataLocation = "global"
tmax = 3000
data = {}

"""
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

metric = Metrics.ORDER
startTime = time.time()



# density-vs-radius matrix including k-vs-start
# ALL NSMs TOGETHER

for start in ["ordered"]:
    states = [start]
    if start == "random":
        xLabelsInner = ["disordered"]
    else:
        xLabelsInner = [start]

    for a, density in enumerate(densities):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate(radii):
            subdata = {}
            for i, k in enumerate(ks):
                for j, initialStateString in enumerate(states): 
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
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
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
                                                fontsize=fontsize,
                                                savePath=f"order_k-vs-density_ordered_complex_start={start}_fontsize={fontsize}.svg", xlim=(0,tmax), ylim=(0,1.1))
    endTime = time.time()
    print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
"""
   
""" 
# SINGLE k vs. start   
density = 0.01
radius = 5
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
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
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
            stepData = evaluator.evaluate()    
            data[f"{i}-{j}"] = stepData    
            endEval = time.time()
            print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

ServiceImages.createMultiPlotFromScratch(
                                             xLabels=xLabelsInner, 
                                             yLabels=yLabelsInner, 
                                             data=data, index=index, 
                                             xAxisLabel=xAxisLabelInner, 
                                             yAxisLabel=yAxisLabelInner,
                                             fontsize=fontsize,
                                             savePath="order_k-vs-density_ordered_simple_fontsize=11.svg", xlim=(0, tmax), ylim=(0,1.1))
endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
            
    
"""

""" 
data = {}

# K VS. START - appendix FIG1 (fig6). by nsm

xLabelPlot = "time steps"
yLabelPlot = "global order \nparameter"

xLabelsOuter = radii
xAxisLabelOuter = "radius" 

xLabelsInner = getLabelsFromKValues(ks)
xAxisLabelInner = "neighbourhood size"

yLabelsOuter = densities
yAxisLabelOuter = "density"

yLabelsInner = [""]
yAxisLabelInner = ""

index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

metric = Metrics.ORDER
startTime = time.time()

for neighbourSelectionMode in neighbourSelectionModes:
    title = getLabelsFromNeighbourSelectionModes([neighbourSelectionMode])[0]
    for a, density in enumerate(densities):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate(radii):
            subdata = {}
            for i, s in enumerate([""]):
                for j, k in enumerate(ks): 
                    startEval = time.time()
                    print(f"d={density}, r={radius}, k={k}")
                    modelParams = []
                    simulationData = []
                    colours = []
                    index = ["ordered start", "disordered start"]

                    for start in ["ordered", "random"]:
                        baseFilename = f"{baseDataLocation}/{levelDataLocation}/global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)

                    #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
            #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
                        stepData = evaluator.evaluate()    
                        subdata[f"{i}-{j}"] = stepData    
                        endEval = time.time()
                        print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
            data[f"{a}-{b}"] = subdata   

    ServiceImages.createMatrixOfPlotsFromScratch(
                                                title=title,
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
                                                fontsize=fontsize,
                                                savePath=f"order_r-vs-d_nsm={neighbourSelectionMode.value}_fontsize={fontsize}.svg", xlim=(0,tmax), ylim=(0,1.1))

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")

 """


"""
data = {}

# K VS. START - appendix FIG2 (single)

xLabelPlot = "time steps"
yLabelPlot = "global order \nparameter"

xLabelsOuter = [5]
xAxisLabelOuter = "radius" 

xLabelsInner = getLabelsFromKValues(ks)
xAxisLabelInner = "neighbourhood size"

yLabelsOuter = [0.01]
yAxisLabelOuter = "density"

yLabelsInner = [""]
yAxisLabelInner = ""

index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

metric = Metrics.ORDER
startTime = time.time()

for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.FARTHEST]:
    title = getLabelsFromNeighbourSelectionModes([neighbourSelectionMode])[0]
    for a, density in enumerate([0.01]):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate([5]):
            subdata = {}
            for i, s in enumerate([""]):
                for j, k in enumerate([1]): 
                    startEval = time.time()
                    print(f"d={density}, r={radius}, k={k}")
                    modelParams = []
                    simulationData = []
                    colours = []
                    index = getLabelsFromNeighbourSelectionModes([neighbourSelectionMode])

                    for start in ["ordered"]:
                        baseFilename = f"{baseDataLocation}/{levelDataLocation}/global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)

                    #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
            #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
                        stepData = evaluator.evaluate()    
                        subdata[f"{i}-{j}"] = stepData    
                        endEval = time.time()
                        print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
            data[f"{a}-{b}"] = subdata   

    ServiceImages.createMatrixOfPlotsFromScratch(
                                                title=title,
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
                                                fontsize=fontsize,
                                                savePath=f"order_fig1_nsm={neighbourSelectionMode.value}_i={iStart}-{iStop}_fontsize={fontsize}.svg", xlim=(0,tmax), ylim=(0,1.1))

endTime = time.time()
print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
"""
levelDataLocation = "local/switchingActive"
tmax = 10000
data = {}

# K VS. START - appendix FIG2 (single)

ds = [0.01, 0.05, 0.09]
rs = [5, 10, 20]

xLabelPlot = "time steps"
yLabelPlot = "global order \nparameter"

xLabelsOuter = rs
xAxisLabelOuter = "radius" 

xLabelsInner = getLabelsFromKValues(ks)
xAxisLabelInner = ""

yLabelsOuter = ds
yAxisLabelOuter = "density"

durations = [1000]

noises = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#noises = ["0", "5", "10", "20", "30"]
#noiseLabels = ["0%", "5%", "10%", "20%", "30%"]
yLabelsInner = durations
yAxisLabelInner = "durations"

index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

metric = Metrics.ORDER
startTime = time.time()

switchType = SwitchType.NEIGHBOUR_SELECTION_MODE

eventStart = 2000


neighbourSelectionModeOrder = NeighbourSelectionMode.FARTHEST
neighbourSelectionModeDisorder = NeighbourSelectionMode.NEAREST
comboInfo = f"{getLabelsFromNeighbourSelectionModes([neighbourSelectionModeOrder])[0]}-{getLabelsFromNeighbourSelectionModes([neighbourSelectionModeDisorder])[0]}"

index = ["Farthest-Nearest"]
#for duration in [1, 1000]:
duration = 1000
k = 1
for eventNoise in noises:
    title = f" {eventNoise}%"
    for a, density in enumerate(ds):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate(rs):
        
            startEval = time.time()
            print(f"d={density}, r={radius}")
            modelParams = []
            simulationData = []
            colours = []
            index = []

            for start in ["ordered", "random"]:
                if start == "random":
                    index.append(f"disordered")
                else:
                    index.append(f"ordered")
                    
                if start == "ordered":
                    startValue = neighbourSelectionModeOrder
                else:
                    startValue = neighbourSelectionModeDisorder
                baseFilename = f"test_event_noise={eventNoise}_{start}_o=F_do=N_d={density}_n={n}_r={radius}_k={k}_noise=1_drn={duration}_2000-align_noise"
                filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)

            threshold = 0.01
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
            stepData = evaluator.evaluate()    
            endEval = time.time()
            print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
            data[f"{a}-{b}"] = stepData   

    ServiceImages.createMultiPlotFromScratch(
                                                title=title,
                                                xAxisLabel=xAxisLabelInner,
                                                yAxisLabel=yAxisLabelInner,
                                                data=data,
                                                index=index, 
                                                xLabels=xLabelsOuter, 
                                                yLabels=yLabelsOuter,
                                                fontsize=fontsize,
                                                colourBackgroundForTimesteps=[eventStart, eventStart + duration],
                                                savePath=f"order_test_evNoise={eventNoise}_duration={duration}_nsms={neighbourSelectionModeOrder.value}-{neighbourSelectionModeDisorder.value}_i={iStart}-{iStop}_fontsize={fontsize}.svg", xlim=(0,tmax), ylim=(0,1.1))

    endTime = time.time()
    print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")

"""
# K switching
levelDataLocation = "local/switchingActive/"
tmax = 3000
data = {}

# K VS. START
index = getLabelsFromNeighbourSelectionModes(neighbourSelectionModes)

metric = Metrics.ORDER
startTime = time.time()

# density-vs-radius matrix including k-vs-start

densities = [0.01]
yLabelsOuter = densities
duration = 1000
orderValue = 5
disorderValue = 1
for start in ["ordered", "random"]:
    states = [start]
    if start == "random":
        xLabelsInner = ["disordered"]
        startValue = disorderValue
    else:
        xLabelsInner = [start]
        startValue = orderValue

    for a, density in enumerate(densities):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate(radii):
            subdata = {}
            for i, k in enumerate(ks):
                for j, eventEffect in enumerate(eventEffects): 
                        startEval = time.time()
                        print(f"d={density}, r={radius}, k={k}, init={start}, eventEffect={eventEffect.name}")
                        modelParams = []
                        simulationData = []
                        colours = []

                        for neighbourSelectionMode in neighbourSelectionModes:
                            baseFilename = f"{baseDataLocation}/{levelDataLocation}/local_1e_switchType=K_{start}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_noise={noisePercentage}_drn={duration}_5000-{eventEffect.val}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)

                    #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
            #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                        threshold = 0.01
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
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
                                                fontsize=fontsize,
                                                savePath=f"order_k-switch_complex_start={start}_fontsize={fontsize}.svg", xlim=(0,tmax), ylim=(0,1.1))
    endTime = time.time()
    print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
"""

"""
# SINGLE for K-switch
tmax = 15000
# SINGLE k vs. start  
levelDataLocation = "local/switchingActive/"
 
xLabelsInner = getLabelsFromEventEffects(eventEffects)
xAxisLabelInner = "event effect"
density = 0.01
radius = 20
duration = 1000
orderValue = 5
disorderValue = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
for initialStateString in ["ordered", "random"]:
    if initialStateString == "random":
        startValue = disorderValue
    else:
        startValue = orderValue
    for i, k in enumerate(ks):
        for j, eventEffect in enumerate(eventEffects): 
                startEval = time.time()
                print(f"d={density}, r={radius}, k={k}, init={initialStateString}, eventEffect={eventEffect.name}")
                modelParams = []
                simulationData = []
                colours = []

                for neighbourSelectionMode in neighbourSelectionModes:
                    baseFilename = f"{baseDataLocation}/{levelDataLocation}/local_1e_switchType=K_{initialStateString}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_noise={noisePercentage}_drn={duration}_5000-{eventEffect.val}"
                    filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                    modelParams.append(modelParamsDensity)
                    simulationData.append(simulationDataDensity)
                    colours.append(coloursDensity)

            #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
    #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                threshold = 0.01
                evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
                stepData = evaluator.evaluate()    
                data[f"{i}-{j}"] = stepData    
                endEval = time.time()
                print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

    ServiceImages.createMultiPlotFromScratch(
                                                xLabels=xLabelsInner, 
                                                yLabels=yLabelsInner, 
                                                data=data, index=index, 
                                                xAxisLabel=xAxisLabelInner, 
                                                yAxisLabel=yAxisLabelInner,
                                                fontsize=fontsize,
                                                savePath=f"order_k-switch_simple_d={density}_r={radius}_fontsize=11.svg", xlim=(0, tmax), ylim=(0,1.1))
    endTime = time.time()
    print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
      
"""

"""
# SINGLE for nsm-switch
tmax = 15000
# SINGLE k vs. start  
levelDataLocation = "local/switchingActive/"
 
xLabelsInner = getLabelsFromEventEffects(eventEffects)
xAxisLabelInner = "event effect"
density = 0.01
radius = 20
duration = 1000
orderValue = NeighbourSelectionMode.FARTHEST.value
disorderValue = NeighbourSelectionMode.NEAREST.value
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
for initialStateString in ["ordered", "random"]:
    if initialStateString == "random":
        startValue = disorderValue
    else:
        startValue = orderValue
    for i, k in enumerate(ks):
        for j, eventEffect in enumerate(eventEffects): 
                startEval = time.time()
                print(f"d={density}, r={radius}, k={k}, init={initialStateString}, eventEffect={eventEffect.name}")
                modelParams = []
                simulationData = []
                colours = []

                for neighbourSelectionMode in neighbourSelectionModes:
                    baseFilename = f"{baseDataLocation}/{levelDataLocation}/local_1e_switchType=MODE_{initialStateString}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_5000-{eventEffect.val}"
                    filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                    modelParams.append(modelParamsDensity)
                    simulationData.append(simulationDataDensity)
                    colours.append(coloursDensity)

            #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
    #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                threshold = 0.01
                evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=interval, threshold=threshold)
                stepData = evaluator.evaluate()    
                data[f"{i}-{j}"] = stepData    
                endEval = time.time()
                print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 

    ServiceImages.createMultiPlotFromScratch(
                                                xLabels=xLabelsInner, 
                                                yLabels=yLabelsInner, 
                                                data=data, index=index, 
                                                xAxisLabel=xAxisLabelInner, 
                                                yAxisLabel=yAxisLabelInner,
                                                fontsize=fontsize,
                                                savePath=f"order_nsm-switch_simple_d={density}_r={radius}_fontsize=11.svg", xlim=(0, tmax), ylim=(0,1.1))
    endTime = time.time()
    print(f"Total duration: {ServiceGeneral.formatTime(endTime-startTime)}")
 """ 


"""
for density in densities:
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
