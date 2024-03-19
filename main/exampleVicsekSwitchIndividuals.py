"""
Contains a simulation for the standard 2D Vicsek model
"""

import random

import VicsekWithNeighbourSelectionSwitchingIndividuals
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode

import DefaultValues as dv

n = 500
k = 5
noise = 0
radius= 10
defaultNeighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST
tmax = 2000

"""
modeOptions = [EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM,
               EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
               EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST,
               EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
               EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]
initialModeDist = [random.choice(modeOptions) for i in range(n)]
"""

initialModeDist = n * [defaultNeighbourSelectionMode]
#initialModeDist[random.randint(0, n)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST

simulator = VicsekWithNeighbourSelectionSwitchingIndividuals.VicsekWithNeighbourSelection(defaultNeighbourSelectionMode, 
                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours, modes = simulator.simulate(tmax=tmax, initialModeDistribution=initialModeDist)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"model_switch_individuals_grouped_changeAt=100_default={defaultNeighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}.json", simulator.getParameterSummary(), modes=modes)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

# Display Animation
preparedAnimator.showAnimation()
