"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import SavedModelService
import EnumNeighbourSelectionMode

import DefaultValues as dv

n = 500
k = 3
noise = 0
radius= 20
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                      domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                      numberOfParticles=n, 
                                                                      k=k, 
                                                                      noise=noise, 
                                                                      radius=radius)
simulationData = simulator.simulate(tmax=500)

# Save model values for future use
SavedModelService.saveModel(simulationData, "neighbour_selection_mode.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k=k, noise=noise, radius=radius)

# Display Animation
preparedAnimator.showAnimation()

# TODO evaluate result
