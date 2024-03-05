
import ServiceSavedModel
import Evaluator
import EnumMetrics
import ServiceMetric
import Animator2D
import AnimatorMatplotlib
import ServiceShowEval

"""
modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/general/LEAST_ORIENTATION_DIFFERENCE_tmax=100_n=100_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.ORDER, simulationData)
evaluator.evaluateAndVisualize(savePath="LOD_tmax=100_n=100_k=5_noise=0_radius=10.png", saveTimestepsResults="timesteps_results_LOD_tmax=100_k=5_noise=0_radius=10.json")
"""

modelParams, data = ServiceSavedModel.loadTimestepsResults("timesteps_results_LOD_tmax=100_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.ORDER)
evaluator.visualize(data, savePath="LOD_tmax=100_n=100_k=5_noise=0_radius=10.png")


#ServiceShowEval.visualiseClusters("examples/LEAST_ORIENTATION_DIFFERENCE_n=200_k=5_noise=0_radius=10.json", 50)
"""
modelParams, simulationData, colours = ServiceSavedModel.loadModel("LEAST_ORIENTATION_DIFFERENCE_tmax=20000_n=400_k=5_noise=0.1_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.CLUSTER_NUMBER, simulationData)
evaluator.evaluateAndVisualize(savePath="LEAST_ORIENTATION_DIFFERENCE_tmax=20000_n=500_k=5_noise=0_radius=10_CLUSTER_NUMBER_dislocation.png")
"""