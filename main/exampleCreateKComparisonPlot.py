import time

import ServiceImages
import ServiceGeneral
import ServiceSavedModel
import ServicePreparation

import EvaluatorMultiAvgComp

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

domainSize = (50, 50)
psteps = 100

ks = [0, 1, 2, 3, 4, 5, 10]
nsms = [NeighbourSelectionMode.ALL,
        NeighbourSelectionMode.RANDOM,
        NeighbourSelectionMode.NEAREST,
        NeighbourSelectionMode.FARTHEST,
        NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
        NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

xAxisLabel = "k"
xLabels = ks
yAxisLabel = "neighbour selection mechanism"
yLabels = ['All', 'Random', 'Nearest', 'Farthest', 'Least Orientation Difference', 'Highest Orientation Difference']

saveLocation = "E:/data/visek-data2/adaptive_radius/data/global/"
iStart = 1
iStop = 11

metric = Metrics.ORDER
data = {}
for density in [0.01]:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
    for radius in [5, 10]:
        for noisePercentage in [0, 0.5, 1, 1.5, 2, 2.5, 3]:
            title = f"{noisePercentage}% noise"
            index = ["ordered", "disordered"]
            for i, nsm in enumerate(nsms):
                for j, k in enumerate(ks):
                    startEval = time.time()
                    ServiceGeneral.logWithTime(f"density={density}, r={radius}, noiseP={noisePercentage}")
                    modelParams = []
                    simulationData = []
                    colours = []
                    for initialState in ["ordered", "random"]:
                        baseFilename = f"{saveLocation}global_noev_nosw_d={density}_r={radius}_{initialState}_nsm={nsm.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(f"{baseFilename}_{i}.json", loadSwitchValues=False)
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
                    ServiceGeneral.logWithTime(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}")    


            savePath = f"{metric.val}_global_noev_nosw_k-comp_d={density}_r={radius}_noiseP={noisePercentage}.svg"
            ServiceImages.createMultiPlotFromScratch(xLabels=xLabels, yLabels=yLabels, data=data, 
                                                    index=index, title=title, xAxisLabel=xAxisLabel,
                                                    yAxisLabel=yAxisLabel, savePath=savePath,
                                                    ylim=(0,1.1), fontsize=13)
