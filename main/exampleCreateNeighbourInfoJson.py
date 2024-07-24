
import ServiceGeneral
import time
import ServicePreparation
import ServiceSavedModel
import ServiceNetwork

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumEventEffect import EventEffect
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

neighbourSelectionModes = [
                           NeighbourSelectionMode.ALL, 
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE
                           ]

orderNeighbourSelectionModes = [NeighbourSelectionMode.ALL,
                                NeighbourSelectionMode.RANDOM,
                                NeighbourSelectionMode.FARTHEST,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

disorderNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                                   NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

densities = [0.01, 0.05, 0.09]
radii = [5, 10]
ks = [1, 5]


iStart = 1
iStop = 2


for i in range(iStart, iStop):
    """
    for neighbourSelectionMode in neighbourSelectionModes:
        for a, density in enumerate(densities):
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            for b, radius in enumerate(radii):
                for j, k in enumerate(ks): 
                    startEval = time.time()
                    for start in ["ordered", "random"]:
                        
                        baseFilename = f"D:/vicsek-data2/adaptive_radius/global/global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}"
                        #filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(f"{baseFilename}_{i}.json", loadSwitchValues=False)
                        steps, positions, orientations = simulationDataDensity
                        savePath = f"D:/vicsek-data2/adaptive_radius/trackinginfo/global/trackinginfo_global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}_{i}.json"
                        ServiceSavedModel.saveConnectionTrackingInformation(ServiceNetwork.getConnectionTrackingInformation(positions=positions, orientations=orientations, radius=radius, neighbourSelectionMode=neighbourSelectionMode, k=k), path=savePath)
                        ServiceGeneral.logWithTime(f"Saved tracking info for nsm={neighbourSelectionMode.name}, d={density}, r={radius}, k={k}, start={start}, i={i}")
    
    """
    
    for a, density in enumerate(densities):
        for neighbourSelectionMode in neighbourSelectionModes:
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            for b, radius in enumerate(radii):
                for j, k in enumerate(ks): 
                    for eventEffect in eventEffects:
                        startEval = time.time()
                        for start in ["ordered", "random"]:
                            baseFilename = f"D:/vicsek-data2/adaptive_radius/local/switchingInactive/local_1e_nosw_{start}_st={neighbourSelectionMode.value}__d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-{eventEffect.val}"
                            #filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                            modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(f"{baseFilename}_{i}.json", loadSwitchValues=False)
                            steps, positions, orientations = simulationDataDensity
                            savePath = f"D:/vicsek-data2/adaptive_radius/trackinginfo/local/nosw/trackinginfo_local_1e_nosw_{start}_st={neighbourSelectionMode.value}__d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-{eventEffect.val}_{i}.json"
                            ServiceSavedModel.saveConnectionTrackingInformation(ServiceNetwork.getConnectionTrackingInformation(positions=positions, orientations=orientations, radius=radius, neighbourSelectionMode=neighbourSelectionMode, k=k), path=savePath)
                            ServiceGeneral.logWithTime(f"Saved tracking info for nsm={neighbourSelectionMode.name}, d={density}, r={radius}, k={k}, start={start}, i={i}")
    
    
    """
    for neighbourSelectionModeOrder in orderNeighbourSelectionModes:
        for neighbourSelectionModeDisorder in disorderNeighbourSelectionModes:
            for eventEffect in eventEffects:
                for a, density in enumerate(densities):
                    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                    for b, radius in enumerate(radii):
                        for j, k in enumerate(ks): 
                            startEval = time.time()
                            for start in ["ordered", "random"]:
                                if start == "ordered":
                                    startValue = neighbourSelectionModeOrder
                                else:
                                    startValue = neighbourSelectionModeDisorder
                                baseFilename = f"D:/vicsek-data2/adaptive_radius/local/switchingActive/d:\vicsek-data2\adaptive_radius\local\switchingActive\local_1e_switchType=MODE_{start}_st={startValue.value}_o={neighbourSelectionModeOrder.value}_do={neighbourSelectionModeDisorder.value}_d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-{eventEffect.val}"
                                #filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                                modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModel(f"{baseFilename}_{i}.json", loadSwitchValues=False)
                                steps, positions, orientations = simulationDataDensity
                                savePath = f"D:/vicsek-data2/adaptive_radius/trackinginfo/global/trackinginfo_global_noev_nosw_d={density}_r={radius}_{start}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}_{i}.json"
                                ServiceSavedModel.saveConnectionTrackingInformation(ServiceNetwork.getConnectionTrackingInformation(positions=positions, orientations=orientations, radius=radius, neighbourSelectionMode=neighbourSelectionMode, k=k), path=savePath)
                                ServiceGeneral.logWithTime(f"Saved tracking info for nsm={neighbourSelectionMode.name}, d={density}, r={radius}, k={k}, start={start}, i={i}")
    """
    
#neighbours, distances, localOrders, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformation(savePath)