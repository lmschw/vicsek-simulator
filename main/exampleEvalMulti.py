import ServiceEvaluationMethod
import ServiceSavedModel
import EvaluatorMulti
import EnumNeighbourSelectionMode
import EnumMetrics

# All by MODE 
#ServiceEvaluationMethod.evaluateAllModes(n=500, k=5, noise=0.3, radius=10, metric=EnumMetrics.Metrics.CLUSTER_NUMBER)


# mode by N 
#ServiceEvaluationMethod.evaluateN(EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST, k=3, noise=0, radius=20)

# mode by K
#ServiceEvaluationMethod.evaluateK(EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, n=500, noise=0.3, radius=10)

# mode by noise
#ServiceEvaluationMethod.evaluateNoise(EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM, n=200, k=3, radius=20)

# mode by radius
#ServiceEvaluationMethod.evaluateRadius(EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, n=500, k=5, noise=0)
"""
mode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
n = 500
k = 5
radius =10
metric = EnumMetrics.Metrics.ORDER
modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.01_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.05_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.1_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.15_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.2_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.25_radius={radius}.json",
                                                            f"noiseExamples/{mode.name}_tmax=10000_n={n}_k={k}_noise=0.3_radius={radius}.json"])


evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
evaluator.evaluateAndVisualize(labels=["noise=0", "noise=0.01", "noise=0.05", "noise=0.1", "noise=0.15", "noise=0.2", "noise=0.25", "noise=0.3"], subtitle=f"Comparing noise for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode}_n={n}_k={k}_all-noise_radius={radius}.png")
"""

"""
mode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
n = 500
k = 5
radius =10
tmax = 1000
noise = 0
metric = EnumMetrics.Metrics.ORDER
modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.005.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.01.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.03.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.05.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.07.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.09.json",
                                                                     f"examples/densityExamples/{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density=0.1.json"])

evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
evaluator.evaluateAndVisualize(labels=["density=0.005", "density=0.0075", "density=0.01", "density=0.02", "density=0.03", "density=0.04", "density=0.05", "density=0.06", "density=0.07", "density=0.08", "density=0.09", "density=0.1"], subtitle=f"Comparing density for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode.name}_n={n}_k={k}_noise={noise}_radius={radius}_density-comparison_fewer-comps.png")
"""