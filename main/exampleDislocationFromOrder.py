"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode
import ServicePreparation

import DefaultValues as dv

"""
n = 400
domainSize=(100,100)
k = 5
noise = 0.1
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 20000

initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

# Display Animation
preparedAnimator.showAnimation()
"""

"""
n = 500
k = 5
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 10000
domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.05, n)

noise = 0.4
i = 3
initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"examples/dislocationExamples/model_{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_{i}.json", simulator.getParameterSummary())
"""
"""
# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())
preparedAnimator.saveAnimation(f"examples/dislocationExamples/visualisation_mode={neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_{i}")
"""