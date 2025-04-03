
import ServiceGeneral
import ServiceSavedModel
import main.ServiceTrackingInformation as ServiceTrackingInformation

import EvaluatorTrackingInfoMultiAvgComp

from EnumMetricsTrackingInfo import Metrics

"""
iStart = 1
iStop = 3
baseFilename = f"test_tracking_info"
filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
neighbours, distances, localOrders, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformations(filenames)

print(neighbours)
print(ServiceNetwork.getMinAvgMaxNeighbourDistanceFromTrackingInfoMultipleRuns(neighbours, distances))
"""
numModels = 2
numRuns = 1
tmax = 3000
metric = Metrics.AVG_DISTANCE_NEIGHBOURS

neighbours = []
distances = []
localOrders = []
orientationDifferences = []
selected = []
#filenames = ["test_tracking_info.json"]
for start in ["ordered", "random"]:
    filenames = [f"c:/Users/Lilly/Downloads/trackinginfo_global_noev_nosw_d=0.05_r=5_random_nsm=N_k=1_n=125_noise=1_psteps=100_1/trackinginfo_global_noev_nosw_d=0.05_r=5_{start}_nsm=N_k=1_n=125_noise=1_psteps=100_1.json"]

    neighboursM, distancesM, localOrdersM, orientationDifferencesM, selectedM = ServiceSavedModel.loadConnectionTrackingInformations(filenames)
    neighbours.append(neighboursM)
    distances.append(distancesM)
    localOrders.append(localOrdersM)
    orientationDifferences.append(orientationDifferencesM)
    selected.append(selectedM)
evaluator = EvaluatorTrackingInfoMultiAvgComp.EvaluatorTrackingInfoMultiAvgComp(metric=metric, tmax=tmax,
                                                                                numberOfRuns=numRuns, 
                                                                                numberOfModels=numModels,
                                                                                neighbours=neighbours,
                                                                                distances=distances,
                                                                                localOrders=localOrders,
                                                                                orientationDifferences=orientationDifferences,
                                                                                selected=selected,
                                                                                evaluationTimestepInterval=1)
evaluator.evaluateAndVisualize(["ordered", "disordered"], "timesteps", "average neighbour distance", savePath=f"test_trackinginfo_metric_{metric.val}.svg")

