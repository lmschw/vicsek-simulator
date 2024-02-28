
import ServiceSavedModel
import Evaluator
import EnumMetrics

modelParams, simulationData = ServiceSavedModel.loadModel("examples/LEAST_ORIENTATION_DIFFERENCE_tmax=100'000_n=500_k=5_noise=0_radius=10.json")

print("Data loading complete.")
evaluator = Evaluator.Evaluator(simulationData, modelParams, EnumMetrics.Metrics.ORDER)
evaluator.evaluateAndVisualize(savePath="LOD_tmax=100000_n=500_k=5_noise=0_radius=10.png")
