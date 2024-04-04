import time
import random
import copy
from datetime import datetime

import VicsekWithNeighbourSelectionSwitchingCellBased
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation

import EnumSwitchType


import DefaultValues as dv

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

noisePercentages = [0, 0.1, 0.5, 1, 1.5, 2] # also run with 0 noise as baseline

radius = 10
tmax = 1000

startTotal = time.time()
for i in range(4, 6):
    startI = time.time()
    for neighbourSelectionMode in modes:
        startMode = time.time()
        for k in ks:
            for density in densities:
                for noisePercentage in noisePercentages:
                    domainSize = baseDomain
                    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                    start = time.time()
                    print(f"Executing density-vs-noise with random start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, density={density}, noisePercentage={noisePercentage}")
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_random-start_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")
        endMode = time.time()
        print(f"Duration for mode {neighbourSelectionMode.name}: {formatTime(endMode-startMode)}")
    endI = time.time()
    print(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
print(f"Duration total: {formatTime(endTotal-startTotal)}")



disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]


radius = 10
tmax = 5000

ksSwitching = [1,5]

startTotal = time.time()
for i in range(1,6):
    startI = time.time()
    for k in ksSwitching:
        startK = time.time()
        for noisePercentage in noisePercentages:
            startNoise = time.time()
            for density in densities:
                startDensity = time.time()
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
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
                        print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
                endDensity = time.time()
                print(f"Duration for density = {density}: {formatTime(endDensity-startDensity)}")
            endNoise = time.time()
            print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        print(f"Duration for k = {k}: {formatTime(endK-startK)}")
    endI = time.time()
    print(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
print(f"Duration for total: {formatTime(endTotal-startTotal)}")



