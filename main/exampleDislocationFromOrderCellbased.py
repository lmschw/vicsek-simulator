import time
import random
import copy

import VicsekWithNeighbourSelectionSwitchingCellBased
import VicsekWithNeighbourSelectionSwitching
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation

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
baseNoise = 1

radius = 10
tmax = 1000

startTotal = time.time()
for i in range(6, 11):
    startI = time.time()
    for neighbourSelectionMode in modes:
        startMode = time.time()
        for k in ks:
            for density in densities:
                for noisePercentage in noisePercentages:
                    domainSize = baseDomain
                    n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
                    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                    start = time.time()
                    print(f"Executing density-vs-noise run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}, k={k}, density={density}, noisePercentage={noisePercentage}")
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")
        endMode = time.time()
        print(f"Duration for mode {neighbourSelectionMode.name}: {formatTime(endMode-startMode)}")
    endI = time.time()
    print(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
print(f"Duration total: {formatTime(endTotal-startTotal)}")

startTotal = time.time()
for i in range(6, 11):
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

"""
for i in range(2, 6):
    for neighbourSelectionMode in modes:
        for k in ks:
            for density in densities:
                for n in swarmSizes:
                    domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, baseSwarmSize)
                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
                    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(baseNoise)

                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-swarmsize_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={baseNoise}%_radius={radius}_{i}.json", simulator.getParameterSummary())
"""