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

xAxisLabel = "timesteps"
domainSize = (50, 50)
density = 0.01
radius = 20
metric = Metrics.ORDER
tmax = 10000
n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
iStart = 1
iStop = 2
evalInterval = 1000

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
ServiceGeneral.logWithTime(f"start") 
modelParams = []
simulationData = []
colours = []
switchTypes = []

for initialStateString in ["ordered"]:
    #baseFilename = f"test_global_noev_nosw_ordered_st=N_d=0.01_n=25_r=20_tmax=10000_k=1_noise=1"
    baseFilename = f"local_1e_nosw_ordered_d=0.06_n=150_r=20_nsm=F_k=1_noise=1_drn=1000_5000-origin_away"
    filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
    filenamesParam = [f"{path[:-4]}_modelParams{path[-4:]}" for path in filenames]

    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=False, fromCsv=False)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)

#paths.append(f"density-vs-noise_ORDER_mode-comparision_n={n}_k=1_radius=10_density={density}_noise={noisePercentage}%_hierarchical_clustering_threshold=0.01.png")
#createMultiPlotFromImages(title, numX, numY, rowLabels, colLabels, paths)
threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=evalInterval, threshold=threshold)

labels = ["ordered", "disordered"]

savePath = f"{metric.val}_test_interval.svg"

evaluator.evaluateAndVisualize(labels=labels, xLabel=xAxisLabel, yLabel=yAxisLabel, showVariance=True, xlim=xlim, ylim=ylim, savePath=savePath)    
endEval = time.time()
print(f"Duration eval {ServiceGeneral.formatTime(endEval-startEval)}") 
