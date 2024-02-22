"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import SavedModelService
import EnumNeighbourSelectionMode

import DefaultValues as dv

n = 200
k = 3
noise = 0
radius= 20
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                      domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                      numberOfParticles=n, 
                                                                      k=k, 
                                                                      noise=noise, 
                                                                      radius=radius)
simulationData = simulator.simulate()

"""
simulator2 = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(NeighbourSelectionModeEnum.NeighbourSelectionModeEnum.FARTHEST, 
                                                                      domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                      numberOfParticles=n, 
                                                                      k=k, 
                                                                      noise=noise, 
                                                                      radius=radius)
simulationData2 = simulator2.simulate()
"""

# Save model values for future use
#SavedModelService.saveModel(simulationData, "neighbour_selection_mode_n=20.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k=k, noise=noise, radius=radius)

# Display Animation
preparedAnimator.showAnimation()

# TODO save values after simulation + option to read existing values

# TODO evaluate result
