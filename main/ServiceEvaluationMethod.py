import ServiceSavedModel
import EvaluatorMulti
import EnumMetrics

"""
Service contains static methods for comparative model visualisations.
"""

def evaluateAllModes(n, k, noise, radius, metric=EnumMetrics.Metrics.ORDER):
    """
    Compares the results for each of the neighbour selection modes for the same values of n, k, noise, radius and the same metric.
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/RANDOM_n={n}_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/NEAREST_n={n}_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/FARTHEST_n={n}_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/LEAST_ORIENTATION_DIFFERENCE_n={n}_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/HIGHEST_ORIENTATION_DIFFERENCE_n={n}_k={k}_noise={noise}_radius={radius}.json"])


    evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
    evaluator.evaluateAndVisualize(labels=["RANDOM", "NEAREST", "FARTHEST", "LEAST_ORIENTATION_DIFFERENCE", "HIGHEST_ORIENTATION_DIFFERENCE"], subtitle=f"Comparing all modes, n={n}_k={k}_noise={noise}_radius={radius}", savePath=f"all_n={n}_k={k}_noise={noise}_radius={radius}.png")

def evaluateN(mode, k, noise, radius, metric=EnumMetrics.Metrics.ORDER):
    """
    Compares the results for each value of n for the same values of k, noise, radius, the same neighbour selection mode and the same metric.
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/{mode.name}_n=100_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n=200_k={k}_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n=500_k={k}_noise={noise}_radius={radius}.json"])


    evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
    evaluator.evaluateAndVisualize(labels=["n=100", "n=200", "n=500"], subtitle=f"Comparing n for {mode.name}, \nn=500, k={k}_noise={noise}_radius={radius}", savePath=f"{mode}_all-n_k={k}_noise={noise}_radius={radius}.png")

def evaluateK(mode, n, noise, radius, metric=EnumMetrics.Metrics.ORDER):
    """
    Compares the results for each value of k for the same values of n, noise, radius, the same neighbour selection mode and the same metric.
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/{mode.name}_n={n}_k=1_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n={n}_k=2_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n={n}_k=3_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n={n}_k=4_noise={noise}_radius={radius}.json",
                                                            f"examples/{mode.name}_n={n}_k=5_noise={noise}_radius={radius}.json"])


    evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
    evaluator.evaluateAndVisualize(labels=["k=1", "k=2", "k=3", "k=4", "k=5"], subtitle=f"Comparing k for {mode.name},\nn={n}_noise={noise}_radius={radius}", savePath=f"{mode}_n={n}_all-k_noise={noise}_radius={radius}.png")

def evaluateNoise(mode, n, k, radius, metric=EnumMetrics.Metrics.ORDER):
    """
    Compares the results for each value of noise for the same values of n, k, radius, the same neighbour selection mode and the same metric.
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/{mode.name}_n={n}_k={k}_noise=0_radius={radius}.json",
                                                            f"examples/{mode.name}_n={n}_k={k}_noise=0.3_radius={radius}.json"])


    evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
    evaluator.evaluateAndVisualize(labels=["noise=0", "noise=0.3"], subtitle=f"Comparing noise for {mode.name}, \nn={n}_k={k}_radius={radius}", savePath=f"{mode}_n={n}_k={k}_all-noise_radius={radius}.png")

def evaluateRadius(mode, n, k, noise, metric=EnumMetrics.Metrics.ORDER):
    """
    Compares the results for each value of radius for the same values of n, k, noise, the same neighbour selection mode and the same metric.
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModels([f"examples/{mode.name}_n={n}_k={k}_noise={noise}_radius=10.json",
                                                            f"examples/{mode.name}_n={n}_k={k}_noise={noise}_radius=20.json",
                                                            f"examples/{mode.name}_n={n}_k={k}_noise={noise}_radius=50.json"])


    evaluator = EvaluatorMulti.EvaluatorMulti(simulationData, modelParams, metric)
    evaluator.evaluateAndVisualize(labels=["r=10", "r=20", "r=50"], subtitle=f"Comparing radius for {mode.name}, \nn={n}, k={k}_noise={noise}", savePath=f"{mode}_n={n}_k={k}_noise={noise}_all-radius.png")

