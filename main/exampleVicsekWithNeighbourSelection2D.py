"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode

import DefaultValues as dv

n = 500
k = 5
noise = 0
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 1000

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
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
