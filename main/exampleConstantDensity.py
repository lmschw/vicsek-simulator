"""
Contains a simulation for the standard 2D Vicsek model with constant density
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode
import ServicePreparation

import DefaultValues as dv


n = 300
density = ServicePreparation.getDensity((100,100), 500)
domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)

print(f"n={n}, density={density}, domainSize={domainSize}")

k = 5
noise = 0
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 100

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

# Display Animation
preparedAnimator.showAnimation()
