import time
import codecs, json
import numpy as np

import EvaluatorMultiAvgComp

import ServiceSavedModel
import ServiceGeneral
import ServicePreparation

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

neighbourSelectionModes = [
                           NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]
#labels = ["Experiment", "All", "Random", "Nearest", "Farthest", "LOD", "HOD"]

"""
neighbourSelectionModes = [None, NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST]
labels = ["Experiment", "Farthest", "Nearest"]
"""
xAxisLabel = "timesteps"

startEval = time.time()

expId = 11
metric = Metrics.ORDER
yAxisLabel = metric.label

#eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)
# eventNoise = None
# noise = 0
# turnBy = 1
# k = 2
ks = [0, 1, 2, 3, 4]
noisePercentages = [0]
eventNoisePercentages = noisePercentages
turnByValues = [0.1, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]

"""
ks = [1]
noisePercentages = [0.1]
eventNoisePercentages = [0.01]
turnByValues = [np.pi]
"""

iStart = 1
iStop = 11


for k in ks:
    for noisePercentage in noisePercentages:
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
        for eventNoisePercentage in eventNoisePercentages:
            eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
            for turnBy in turnByValues:
                for mode in neighbourSelectionModes:
                    ServiceGeneral.logWithTime(f"k={k}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}")
                    labels= ["Experiment", mode.value]
                    modelParams = []
                    simulationData = []
                    colours = []
                    for nsm in [None, mode]:
                        if nsm == None:
                            baseFilename = f"lei_2020_expId={expId}.json"
                            filenames = [baseFilename] * (iStop-iStart) 
                        else:
                            baseFilename = f"test_lei_2020_expId={expId}-start_nosw_{nsm.value}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                    threshold = 0.01
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=1, threshold=threshold)
                    savePath = f"{metric.val}_lei_2020_expId={expId}_nosw_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}_nsm={mode.value}.svg"
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, savePath=savePath)    
                    endEval = time.time()
                    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}")


for k in ks:
    for noisePercentage in noisePercentages:
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
        for eventNoisePercentage in eventNoisePercentages:
            eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
            for turnBy in turnByValues:
                    ServiceGeneral.logWithTime(f"k={k}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}")
                    labels= ["Experiment", "F-N", "HOD-LOD"]
                    modelParams = []
                    simulationData = []
                    colours = []
                    for nsm in [None, [NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST], [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]:
                        if nsm == None:
                            baseFilename = f"lei_2020_expId={expId}.json"
                            filenames = [baseFilename] * (iStop-iStart) 
                        else:
                            baseFilename = f"test_lei_2020_expId={expId}-start_nsmsw_o={nsm[0].value}_do={nsm[1].value}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                    threshold = 0.01
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=1, threshold=threshold)
                    savePath = f"{metric.val}_lei_2020_expId={expId}_nsmsw_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}_nsm={mode.value}.svg"
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, savePath=savePath)    
                    endEval = time.time()
                    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}")


for nsm in neighbourSelectionModes:
    for noisePercentage in noisePercentages:
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
        for eventNoisePercentage in eventNoisePercentages:
            eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
            for turnBy in turnByValues:
                    ServiceGeneral.logWithTime(f"nsm={nsm.value}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}")
                    labels= ["Experiment", "k=[5,1]"]
                    modelParams = []
                    simulationData = []
                    colours = []
                    for kCombo in [None, [5, 1]]:
                        if kCombo == None:
                            baseFilename = f"lei_2020_expId={expId}.json"
                            filenames = [baseFilename] * (iStop-iStart) 
                        else:
                            baseFilename = f"test_lei_2020_expId={expId}-start_ksw_o={kCombo[0]}_do={kCombo[1]}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_nsm={nsm.value}"
                            filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                    threshold = 0.01
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=1, threshold=threshold)
                    savePath = f"{metric.val}_lei_2020_expId={expId}_ksw_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_nsm={nsm.value}.svg"
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, savePath=savePath)    
                    endEval = time.time()
                    print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}")
