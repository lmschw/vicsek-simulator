# density-vs-noise
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
import math
import time

import ServicePreparation
import EvaluatorMultiAvgComp
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

import ServiceImages

def formatTime(timeInSecs):
    mins = int(timeInSecs / 60)
    secs = timeInSecs % 60

    if mins >= 60:
        hours = int(mins / 60)
        mins = mins % 60
        return f"{hours}h {mins}min {secs:.1f}s"
    return f"{mins}min {secs:.1f}s"


# density on x, noise on y
#numX = 5
#numY = 5

"""
# DENSITY VS. NOISE - ORDERED START
title = "Density vs. noise - ORDER"

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01"]
yLabelsShort = ["0.03", "0.01"]
xLabels = ["0%","0.1%", "0.5%", "1%", "1.5%", "2%"]
xLabelsShort = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.ORDER

# DENSITY-VS-NOISE
modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01]
densitiesShort = [0.03, 0.01]
noisePs = [0, 0.1, 0.5, 1, 1.5, 2]
noisePsShort = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePsShort):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                                        ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabelsShort, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_density-vs-noise_ordered_partial.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")

"""
"""
# DENSITY VS. NOISE - ORDERED START - LOW DENSITY

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01", "0.005", "0.001", "0.0008", "0.0005", "0.0003"]
xLabels = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01, 0.005, 0.001, 0.0008, 0.0005, 0.0003]
noisePs = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePs):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                           ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_density-vs-noise_ordered_full.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# DENSITY VS. NOISE - HOD - ORDERED START
title = "Density vs. noise - ORDER"

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01"]
xLabels = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["HIGHEST ORIENTATION DIFFERENCE"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.ORDER

# DENSITY-VS-NOISE
modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01]
noisePs = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePs):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                                        ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_density-vs-noise_hod_ordered_partial.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# K VS. NOISE - ORDERED START
yLabels = ["5", "3", "1"]
xLabels = ["0%","0.1%", "0.5%", "1%", "1.5%", "2%"]
xLabelsShort = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Number of neighbours k"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
ks = [5, 3, 1]
density = 0.01
noisePs = [0, 0.1, 0.5, 1, 1.5, 2]
noisePsShort = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, k in enumerate(ks):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePsShort):
            startEval = time.time()
            print(f"k={k}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                                        ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabelsShort, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_k-vs-noise_ordered_partial.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# K VS. DENSITY - ORDERED START
yLabels = ["5", "3", "1"]
xLabels = ["0.01", "0.03", "0.05", "0.07", "0.09"]
xAxisLabel = "Density"
yAxisLabel = "Number of neighbours k"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
ks = [5, 3, 1]
noisePercentage = 1
densities = [0.01, 0.03, 0.05, 0.07, 0.09]

start = time.time()
for i, k in enumerate(ks):
    for j, density in enumerate(densities):
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            startEval = time.time()
            print(f"k={k}, density={density}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                                        ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_k-vs-density_ordered.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# DENSITY VS. NOISE - RANDOM START

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01"]
yLabelsShort = ["0.03", "0.01"]
xLabels = ["0%","0.1%", "0.5%", "1%", "1.5%", "2%"]
xLabelsShort = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.CLUSTER_NUMBER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01]
densitiesShort = [0.03, 0.01]
noisePs = [0, 0.1, 0.5, 1, 1.5, 2]
noisePsShort = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePsShort):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                           ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabelsShort, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="clusternumber_density-vs-noise_random_partial.svg", xlim=(0,1000))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# DENSITY VS. NOISE - RANDOM START - LOW DENSITY

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01", "0.005", "0.001", "0.0008", "0.0005", "0.0003"]
xLabels = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01, 0.005, 0.001, 0.0008, 0.0005, 0.0003]
noisePs = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePs):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                           ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_density-vs-noise_random_full.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
# DENSITY VS. NOISE - HOD - RANDOM START
title = "Density vs. noise - ORDER"

yLabels = ["0.09", "0.07", "0.05", "0.03", "0.01"]
xLabels = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Density"
index = ["HIGHEST ORIENTATION DIFFERENCE"]

#paths = []
domainSize = (100, 100)
radius=10
k=1
metric = Metrics.ORDER

# DENSITY-VS-NOISE
modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
densities = [0.09, 0.07, 0.05, 0.03, 0.01]
noisePs = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, density in enumerate(densities):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePs):
            startEval = time.time()
            print(f"density={density}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                                        ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_density-vs-noise_hod_random_partial.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")



"""
# K VS. NOISE - RANDOM START
yLabels = ["5", "3", "1"]
xLabels = ["0%","0.1%", "0.5%", "1%", "1.5%", "2%"]
xLabelsShort = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Number of neighbours k"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
ks = [5, 3, 1]
density = 0.01
noisePs = [0, 0.1, 0.5, 1, 1.5, 2]
noisePsShort = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, k in enumerate(ks):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePsShort):
            startEval = time.time()
            print(f"k={k}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                           ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabelsShort, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_k-vs-noise_random_partial.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
"""
# K VS. DENSITY - RANDOM START
yLabels = ["5", "3", "1"]
xLabels = ["0.01", "0.03", "0.05", "0.07", "0.09"]
xAxisLabel = "Density"
yAxisLabel = "Number of neighbours k"
index = ["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]
data = {}
ks = [5, 3, 1]
noisePercentage = 1
densities = [0.01, 0.03, 0.05, 0.07, 0.09]

start = time.time()
for i, k in enumerate(ks):
    for j, density in enumerate(densities):
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            startEval = time.time()
            print(f"k={k}, density={density}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                           ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_k-vs-density_random.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""

"""
# MODES SEPARATE
xLabels = ["ALL", "RANDOM", "NEAREST", "FARTHEST", "LEAST \nORIENTATION \nDIFFERENCE", "HIGHEST \nORIENTATION \nDIFFERENCE"]
yLabels = [""]
xAxisLabel = "neighbour selection mode"
yAxisLabel = "order metric"
index = ["k=1, ordered start", "k=1, random start", "k=3, ordered start", "k=3, random start", "k=5, ordered start", "k=5, random start"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.ALL,
         NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]
data = {}
ks = [1, 3, 5]
noisePercentage = 1
densities = [0.01, 0.03, 0.05, 0.07, 0.09]
density = 0.01

start = time.time()
for i, mode in enumerate(modes):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        startEval = time.time()
        modelParams = []
        simulationData = []
        colours = []

        for k in ks:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                        ])
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                                        f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json"
                                                                                        ])
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)

        #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
        #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
        threshold = 0.01
        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
        stepData = evaluator.evaluate()    
        data[f"{0}-{i}"] = stepData    
        endEval = time.time()
        print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="horizontal_mode_comparison_ordered-random_all-ks.svg", xlim=(0,1000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""


# ----------------------- SWITCHING --------------------------------------------------------------------
"""
# ORDER VS DISORDER STATES
yLabels = ["NEAREST", "LEAST ORIENTATION \nDIFFERENCE"]
xLabels = ["RANDOM", "FARTHEST", "HIGHEST ORIENTATION \nDIFFERENCE", "ALL"]
xAxisLabel = "Disorder neighbour selection modes"
yAxisLabel = "Order neighbour selection modes"
index = ["1% noise"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]

data = {}
noisePercentage = 1
k = 1
density = 0.01

tmax = 5000

start = time.time()
for i, disorderedState in enumerate(disorderStates):
    for j, orderedState in enumerate(orderStates):
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            startEval = time.time()
            print(f"orderedState={orderedState.name}, disorderedState={disorderedState.name}")
            modelParams = []
            simulationData = []
            colours = []

            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_7.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_8.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_9.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_10.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_11.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_12.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_13.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_14.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_15.json",
                                                                                                    f"D:/vicsek-data/switching/i=7-16/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_16.json",
                                                                                                   ])
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
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_switching_order-comp.svg", xlim=(0,5000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")

"""
"""
# ORDER VS DISORDER STATES
yLabels = ["NEAREST", "LEAST \nORIENTATION \nDIFFERENCE"]
xLabels = ["RANDOM", "FARTHEST", "HIGHEST \nORIENTATION \nDIFFERENCE", "ALL"]
xAxisLabel = "Disorder neighbour selection modes"
yAxisLabel = "Order neighbour selection modes"
index = ["0% noise", "0.5% noise", "1% noise", "1.5% noise", "2% noise"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]

noisePercentages = [0, 0.5, 1, 1.5, 2]

data = {}
k = 1
density = 0.01
tmax = 5000

start = time.time()
for i, disorderedState in enumerate(disorderStates):
    for j, orderedState in enumerate(orderStates):
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                startEval = time.time()
                print(f"orderedState={orderedState.name}, disorderedState={disorderedState.name}")
                modelParams = []
                simulationData = []
                colours = []

                for noisePercentage in noisePercentages:
                    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_7.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_8.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_9.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_10.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_11.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_12.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_13.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_14.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_15.json",
                                                                                                            f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderedState.name}_1000-{disorderedState.name}_4000-{orderedState.name}_tmax=5000_n={n}_k={k}_noise={noisePercentage}%_16.json",
                                                                                                        ])
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
                print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_switching_noise-comp.svg", xlim=(0,5000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""

"""
yLabels = ["3"]
xLabels = ["0%","0.1%", "0.5%", "1%", "1.5%", "2%"]
xLabelsShort = ["0%", "0.5%", "1%", "1.5%", "2%"]
xAxisLabel = "Noise"
yAxisLabel = "Number of neighbours k"
index = ["NEAREST", "LEAST ORIENTATION DIFFERENCE"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

modes = [NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
data = {}
ks = [3]
density = 0.01
noisePsShort = [0, 0.5, 1, 1.5, 2]
start = time.time()
for i, k in enumerate(ks):
    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
    for j, noisePercentage in enumerate(noisePsShort):
            startEval = time.time()
            print(f"k={k}, noiseP={noisePercentage}")
            modelParams = []
            simulationData = []
            colours = []

            for mode in modes:
                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                        f"model_density-vs-noise_random-start_{mode.name}_tmax=100000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json"
                                                                                                          ])
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)

        #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
            threshold = 0.01
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=500, threshold=threshold)
            stepData = evaluator.evaluate()    
            data[f"{i}-{j}"] = stepData    
            endEval = time.time()
            print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabelsShort, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="clusternumber_k=3_tmax=100000.svg", xlim=(0,100000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""
# K-SWITCHING
"""
xLabels = ["NEAREST", "LEAST \nORIENTATION \nDIFFERENCE"]
yLabels = [""]
xAxisLabel = "Neighbour selection mode"
yAxisLabel = "Order metric"
index = ["0% noise", "0.5% noise", "1% noise", "1.5% noise", "2% noise"]

#paths = []
domainSize = (100, 100)
radius=10

metric = Metrics.ORDER

disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]

noisePercentages = [0, 0.5, 1, 1.5, 2]

data = {}
density = 0.01
tmax = 5000

orderK = 5
disorderK = 1

start = time.time()
for i, mode in enumerate(disorderStates):
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                startEval = time.time()
                modelParams = []
                simulationData = []
                colours = []

                for noisePercentage in noisePercentages:
                    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_1.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_2.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_3.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_4.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_5.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_6.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_7.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_8.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_9.json",
                                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_10.json",

                                                                                                        ])
                    modelParams.append(modelParamsDensity)
                    simulationData.append(simulationDataDensity)
                    colours.append(coloursDensity)

            #paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
    #createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
                threshold = 0.01
                evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
                stepData = evaluator.evaluate()    
                data[f"{0}-{i}"] = stepData    
                endEval = time.time()
                print(f"Duration eval {formatTime(endEval-startEval)}")    

ServiceImages.createMultiPlotFromScratch(xLabels, yLabels, data, index, xAxisLabel=xAxisLabel, yAxisLabel=yAxisLabel, savePath="order_kswitching_noise-comp.svg", xlim=(0,5000), ylim=(0,1.1))
end = time.time()
print(f"Total duration: {formatTime(end-start)}")
"""