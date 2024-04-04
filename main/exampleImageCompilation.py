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
numX = 5
numY = 5

title = "Density vs. noise - ORDER"

rowLabels = ["0.01", "0.03", "0.05", "0.07", "0.09"]
colLabels = ["0%", "0.5%", "1%", "1.5%", "2%"]
xLabel = "Noise"
yLabel = "Density"

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
densities = [0.01, 0.03, 0.05, 0.07, 0.09]
densitiesShort = [0.01, 0.03]
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

ServiceImages.createMultiPlotFromScratch(title, numX, numY, rowLabels, colLabels, data, xLabel, yLabel, savePath="order_density-vs-noise_partial.svg")
end = time.time()
print(f"Total duration: {formatTime(end-start)}")