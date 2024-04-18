
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
ServiceShowEval.visualiseClusters("switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=1_noise=0.06283185307179587_radius=10.json", savePathVisualisation="visualisation_clusters_switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=1_noise=0.06283185307179587_radius=10.mp4")


"""
modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/switch/switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=5_noise=0.09424777960769379_radius=10.json")
print("Data loading complete.")
evaluator = Evaluator.Evaluator(modelParams, EnumMetrics.Metrics.ORDER, simulationData, evaluationTimestepInterval=500)
evaluator.evaluateAndVisualize(savePath="switch_ORDER_NEIGHBOUR_SELECTION_MODE_FARTHEST_1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=5_noise=1.5%_radius=10.png")
"""