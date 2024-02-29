
import ServiceSavedModel
import Evaluator
import EnumMetrics
import ServiceMetric
import Animator2D
import AnimatorMatplotlib
import ServiceShowEval

"""
modelParams, simulationData, colours = ServiceSavedModel.loadModel("LEAST_ORIENTATION_DIFFERENCE_tmax=100_n=100_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(simulationData, modelParams, EnumMetrics.Metrics.ORDER)
evaluator.evaluateAndVisualize(savePath="LOD_tmax=100_n=100_k=5_noise=0_radius=10.png")
"""

#ServiceShowEval.visualiseClusters("examples/LEAST_ORIENTATION_DIFFERENCE_n=200_k=5_noise=0_radius=10.json", 50)

modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/LEAST_ORIENTATION_DIFFERENCE_n=200_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(simulationData, modelParams, EnumMetrics.Metrics.CLUSTER_NUMBER)
evaluator.evaluateAndVisualize(savePath="LOD_n=200_k=5_noise=0_radius=10_CLUSTER.png")
