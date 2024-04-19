import ServiceGeneral
import ServiceSavedModel
import ServicePreparation

import EvaluatorMultiAvgComp

from EnumMetrics import Metrics
from EnumNeighbourSelectionMode import NeighbourSelectionMode

"""
metric = Metrics.ORDER
mode = NeighbourSelectionMode.NEAREST
density = 0.03
i = 1
tmax = 5000
noisePercentage=1
threshold = 0.7

filename = f"switch_individual_switchType=K_orderVal=5_disorderVal=1_tmax=5000_n=300_density=0.03_mode=NEAREST_noise=1%_orderthreshold={threshold}_1.json"

ServiceGeneral.logWithTime(f"k switching. mode={mode.name}. density={density}, i={i}")
modelParams, simulationData, colours = ServiceSavedModel.loadModel(filename)
timesteps, positions, orientations = simulationData 

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp([[modelParams]], metric, [[simulationData]], evaluationTimestepInterval=100)
evaluator.evaluateAndVisualize(labels=[mode.name], xLabel="density", yLabel="noise", savePath=f"order_kswitching_tmax={tmax}_mode={mode.name}_density={density}-noise={noisePercentage}_differencethreshold={threshold}_{i}.svg")

"""

tmax=5000
radius=10
domainSize=(100,100)
modes = [NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

metric=Metrics.ORDER
labels=["0", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"]
xLabel = "Timestep"
yLabel = "order"

density = 0.03
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
tmax = 5000
modelParams = []
simulationData = []
colours = []

mode = NeighbourSelectionMode.NEAREST
for orderthreshold in [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"switch_individual_switchType=K_orderVal=5_disorderVal=1_tmax={tmax}_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_orderthreshold={orderthreshold}_1.json",
                                                                                        ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, savePath=f"order-kswitching-density={density}-noise={noisePercentage}-tmax={tmax}.svg")

