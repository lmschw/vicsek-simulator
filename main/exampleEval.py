
import SavedModelService
import Evaluator
import EnumMetrics

modelParams, simulationData = SavedModelService.loadModel("neighbour_selection_mode.json")

evaluator = Evaluator.Evaluator(simulationData, modelParams, EnumMetrics.Metrics.ORDER)
evaluator.evaluateAndVisualize()
