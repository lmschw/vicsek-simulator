"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelectionSwitchingCellBased
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
density=0.01
neighbourSelectionMode = NeighbourSelectionMode.NEAREST

n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
print(f"mode={neighbourSelectionMode.name}, noisePercentage={noisePercentage}, density={density}")

simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"test.json", simulator.getParameterSummary())