"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithKNeighboursWithModes
import MatplotlibAnimator
import Animator2D
import SavedModelService

import DefaultValues as dv

n = 500
k1 = 2
k2 = 10
noise = 0
radius= 100
leavingAllowed = False

simulator = VicsekWithKNeighboursWithModes.VicsekWithKNeighboursWithModes(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, numberOfParticles=n, k1=k1, k2=k2, noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)
simulationData = simulator.simulate(tmax=6000)

# Save model values for future use
SavedModelService.saveModel(simulationData, "modes_n=500,radius=100,tmax=6000.json")

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k="k1={k1}, k2={k2}", noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)

# Display Animation
preparedAnimator.showAnimation()

# TODO save values after simulation + option to read existing values

# TODO evaluate result
