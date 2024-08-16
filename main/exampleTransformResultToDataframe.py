import ServiceDataframe
import ServiceSavedModel

import EvaluatorMultiAvgComp

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

metric = Metrics.ORDER

nsms = [NeighbourSelectionMode.FARTHEST,
        NeighbourSelectionMode.NEAREST,
        NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

ks = [1, 2, 3, 4, 5]

initialStates = ["ordered", "random"]

density = 0.01
radius = 5
n = 25

startT = 1000
tmax = 30000

iStart = 1
iStop = 2

ks = [1]
nsms = [NeighbourSelectionMode.FARTHEST]
initialStates = ["ordered"]

for k in ks:
    for nsm in nsms:
        for initialStateString in initialStates:
            for i in range(iStart, iStop):
                filename = f"d:/data/visek-data2/adaptive_radius/data/global/tmax=30000/global_noev_nosw_d={density}_r={radius}_{initialStateString}_nsm={nsm.value}_k={k}_n={n}_noise=1_psteps=100_{i}.json"
                modelParams, simulationData, colours = ServiceSavedModel.loadModels(paths=[filename], loadSwitchValues=False)
                evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams=[modelParams],
                                                                        metric=metric,
                                                                        simulationData=[simulationData],
                                                                        evaluationTimestepInterval=1)
                results = evaluator.evaluate()
                df = ServiceDataframe.createDataframeOfResultsData(results)
                
                
