
import ServiceGeneral
import time
import ServicePreparation
import ServiceSavedModel
import ServiceNetwork

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
import EvaluatorMultiAvgComp

modelParams = []
simulationData = []
colours = []
index = []

domainSize = (50, 50)
noisePercentage = 1
psteps = 100
interval = 1

neighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                           ]
densities = [0.01]
radii = [20]
ks = [1]

metric = Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS

iStart = 1
iStop = 2


for neighbourSelectionMode in neighbourSelectionModes:
    for a, density in enumerate(densities):
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        for b, radius in enumerate(radii):
            subdata = {}
            for i, s in enumerate([""]):
                for j, k in enumerate(ks): 
                    startEval = time.time()

                    for start in ["ordered"]:
                        baseFilename = f"D:/vicsek-data2/adaptive_radius/global/global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                        #filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(f"{baseFilename}_1.json", loadSwitchValues=False)
                        steps, positions, orientations = simulationDataDensity
                        savePath = "test_tracking_info.json"
                        ServiceSavedModel.saveConnectionTrackingInformation(ServiceNetwork.getConnectionTrackingInformation(positions=positions, orientations=orientations, radius=radius, neighbourSelectionMode=neighbourSelectionMode, k=k), path=savePath)
                        ServiceGeneral.logWithTime(f"Saved tracking info for nsm={neighbourSelectionMode.name}, d={density}, r={radius}, k={k}, start={start}")

neighbours, distances, localOrders, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformation(savePath)
print(f"n[0][0]={neighbours['0']['0']}")
print(f"d[0][0]={distances['0']['0']}")
print(f"lo[0][0]={localOrders['0']['0']}")
print(f"ods[0][0]={orientationDifferences['0']['0']}")
print(f"selected[0][0]={selected['0']['0']}")