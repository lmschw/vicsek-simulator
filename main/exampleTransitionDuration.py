from EnumEventEffect import EventEffect
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumSwitchType import SwitchType

import ServiceAnalysis
import ServiceGeneral
import ServicePreparation
import ServiceSavedModel


neighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]
domainSize = (50, 50)
radius = 20

iStart = 1
iStop = 11

"""
switchType = SwitchType.K
disorderValue = 1
orderValue = 5
for density in [0.09]:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    for nsm in neighbourSelectionModes:
        for eventEffect in eventEffects:
            for initialCondition in ["ordered", "random"]:
                if initialCondition == "ordered":
                    startValue = orderValue
                else:
                    startValue = disorderValue
                baseFilename = f"d:/vicsek-data2/adaptive_radius/local/switchingActive/local_1e_switchType={switchType.value}_{initialCondition}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={nsm.value}_noise=1_drn=1000_5000-{eventEffect.val}"
                filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                modelParams, simulationData, colours, switchTypeValues = ServiceSavedModel.loadModels(paths=filenames, loadSwitchValues=True)
                minSpeed, avgSpeed, maxSpeed = ServiceAnalysis.getMinAvgMaxTransitionSpeedForMultipleRuns(simulationData=simulationData, eventStartTimestep=5000)
                ServiceGeneral.logWithTime(f"d={density}, nsm={nsm.value}, ee={eventEffect.value}, init={initialCondition}: min={minSpeed}, avg={avgSpeed}, max={maxSpeed}")
"""
switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
orderValue = NeighbourSelectionMode.FARTHEST
disorderValue = NeighbourSelectionMode.NEAREST
for density in [0.09]:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    for k in [1]:
        for eventEffect in eventEffects:
            for initialCondition in ["ordered", "random"]:
                if initialCondition == "ordered":
                    startValue = orderValue
                else:
                    startValue = disorderValue
                baseFilename = f"d:/vicsek-data2/adaptive_radius/local/switchingActive/local_1e_switchType={switchType.value}_{initialCondition}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-{eventEffect.val}"
                filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                modelParams, simulationData, colours, switchTypeValues = ServiceSavedModel.loadModels(paths=filenames, loadSwitchValues=True)
                minSpeed, avgSpeed, maxSpeed = ServiceAnalysis.getMinAvgMaxTransitionSpeedForMultipleRuns(simulationData=simulationData, eventStartTimestep=5000)
                ServiceGeneral.logWithTime(f"nsm: d={density}, nsm={startValue.value}, ee={eventEffect.value}, init={initialCondition}: min={minSpeed}, avg={avgSpeed}, max={maxSpeed}")


