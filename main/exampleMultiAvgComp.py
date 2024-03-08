import EnumNeighbourSelectionMode
import EnumMetrics
import ServiceSavedModel
import EvaluatorMultiAvgComp
import VicsekWithNeighbourSelection
import ServicePreparation

import DefaultValues as dv
import AnimatorMatplotlib
import Animator2D

"""
mode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
n = 500
k = 5
radius =10
tmax = 1000
noise = 0
metric = EnumMetrics.Metrics.ORDER
densities = [0.005, 0.01, 0.04, 0.05, 0.08, 0.1]
"""
"""
for density in densities:
    for i in range(1,10):
        domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)

        print(f"i={i}, n={n}, density={density}, domainSize={domainSize}")

        k = 5
        noise = 0
        radius= 10
        neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
        tmax = 1000

        simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                        domainSize=domainSize, 
                                                                        numberOfParticles=n, 
                                                                        k=k, 
                                                                        noise=noise, 
                                                                        radius=radius)
        simulationData, colours = simulator.simulate(tmax=tmax)

        # Save model values for future use
        ServiceSavedModel.saveModel(simulationData, colours, f"examples/densityExamples/{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_{i}.json", simulator.getParameterSummary())

"""
"""
modelParams = []
simulationData = []
colours = []

for density in densities:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_1.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_2.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_3.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_4.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_5.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_6.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_7.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_8.json",
                                                                        f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_9.json"])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData)
evaluator.evaluateAndVisualize(labels=["density=0.005",  "density=0.01", "density=0.04", "density=0.05", "density=0.08", "density=0.1"], subtitle=f"Comparing average density for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode.name}_n={n}_k={k}_noise={noise}_radius={radius}_density-comparison_fewer-comps.png")
"""

n=500
k=5
mode=EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax=10000
radius=10

metric=EnumMetrics.Metrics.CLUSTER_SIZE
noises=[0.1, 0.2, 0.3, 0.4]
labels=["noise=0.1", "noise=0.2", "noise=0.3", "noise=0.4"]
#labels=["noise=0.1", "noise=0.2", "noise=0.3"]
#labels=["noise=0.1", "noise=0.2"]
#labels=["noise=0.1"]


modelParams = []
simulationData = []
colours = []

for noise in noises:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_1.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_2.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_3.json"])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=500)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing average cluster number for dislocation from order based on noise for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode.name}_n={n}_k={k}_radius={radius}_dislocation-comparison-based-on-noise.png")
