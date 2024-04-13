import time

import VicsekWithNeighbourSelectionSwitchingCellBased
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral

import EnumSwitchType

# TASK 1: missing density=0.09 for regular k switching
# TASK 2: regular k switching for HOD & ALL
# TASK 3: mode switching density > 0.03 for k = 1
# TASK 4: mode switching k = 5
# TASK 5: mode switching k = 3
# TASK 6: long mode switching
# TASK 7: long k switching
def formatTime(timeInSecs):
    mins = int(timeInSecs / 60)
    secs = timeInSecs % 60

    if mins >= 60:
        hours = int(mins / 60)
        mins = mins % 60
        return f"{hours}h {mins}min {secs:.1f}s"
    return f"{mins}min {secs:.1f}s"


modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]

densities = [0.01, 0.03, 0.05, 0.07, 0.09]

swarmSizes = [100, 300, 500, 700, 900]
baseDomain = (100, 100)
baseSwarmSize = 500

ks = [1, 3, 5]

noisePercentages = [0, 0.5, 1, 1.5, 2] # also run with 0 noise as baseline

disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]



#density = 0.01
radius = 10
#noisePercentage = 1
#k = 1
#neighbourSelectionMode = NeighbourSelectionMode.NEAREST
tmax = 5000
#i = 1

orderK = 5
disorderK = 1

startTotal = time.time()
for k in [1]:
    startK = time.time()
    for noisePercentage in noisePercentages:
        startNoise = time.time()
        for density in [0.05, 0.07, 0.09]:
            startDensity = time.time()
            for orderState in orderStates:
                for disorderState in disorderStates:
                    for i in range(7,17):
                        ServiceGeneral.logWithTime(f"Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()
                        domainSize = baseDomain
                        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
            endDensity = time.time()
            ServiceGeneral.logWithTime(f"Duration for density = {density}: {formatTime(endDensity-startDensity)}")
        endNoise = time.time()
        ServiceGeneral.logWithTime(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
    endK = time.time()
    ServiceGeneral.logWithTime(f"Duration for k = {k}: {formatTime(endK-startK)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Duration for total: {formatTime(endTotal-startTotal)}")