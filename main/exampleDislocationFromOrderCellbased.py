"""
Contains a simulation for the standard 2D Vicsek model
"""

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

radius=10
tmax=100
k=1
domainSize=(100,100)
noisePercentage=0
density=0.09
neighbourSelectionMode = NeighbourSelectionMode.NEAREST

start = time.time()
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
initialStateCopy = copy.deepcopy(initialState)
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
print(f"mode={neighbourSelectionMode.name}, noisePercentage={noisePercentage}, density={density}")

simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)
end = time.time()
startStd = time.time()
# Save model values for future use
#ServiceSavedModel.saveModel(simulationData, colours, f"test.json", simulator.getParameterSummary())
simulator = VicsekWithNeighbourSelectionSwitching.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationDataStandard, coloursStandard = simulator.simulate(tmax=tmax, initialState=initialStateCopy)
endStd = time.time()
print(f"new: {end-start}s, standard: {endStd-startStd}")

steps, positions, orientations = simulationData
stepsStd, positionsStd, orientationsStd = simulationDataStandard

for i in range(20):
    step = random.randint(0, tmax)
    part = random.randint(0, n)
    print(f"time: {steps[step] == stepsStd[step]}, \npositions for {step}-{part}: {positions[step][part] == positionsStd[step][part]}\norientations for {step}-{part}: {orientations[step][part] == orientationsStd[step][part]}")