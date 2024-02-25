
import SavedModelService
import Evaluator
import EnumMetrics

modelParams, simulationData = SavedModelService.loadModel("examples/FARTHEST_n=100_k=1_noise=0_radius=10.json")

evaluator = Evaluator.Evaluator(simulationData, modelParams, EnumMetrics.Metrics.ORDER)
evaluator.evaluateAndVisualize()
