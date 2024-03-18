
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
"""
modelParams, data = ServiceSavedModel.loadTimestepsResults("timesteps_results_LOD_tmax=100_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.ORDER)
evaluator.visualize(data, savePath="LOD_tmax=100_n=100_k=5_noise=0_radius=10.png")
"""

#ServiceShowEval.visualiseClusters("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0.3_radius=10_3.json", threshold=0.01)
#ServiceShowEval.visualiseClusters("LEAST_ORIENTATION_DIFFERENCE_tmax=20000_n=400_k=5_noise=0.1_radius=10.json", threshold=1, savePathVisualisation="visualisation_LOD_tmax=20000_n=400_k=5_noise=0.1_radius=10_cluster_visualisation_threshold=1.mp4")



modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/general/LEAST_ORIENTATION_DIFFERENCE_n=500_k=5_noise=0_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME, simulationData, evaluationTimestepInterval=5)
evaluator.evaluateAndVisualize(savePath="LEAST_ORIENTATION_DIFFERENCE_tmax=1000_n=500_k=5_noise=0_radius=10_CLUSTER_NUMBER_OVER_LIFETIME.png")
