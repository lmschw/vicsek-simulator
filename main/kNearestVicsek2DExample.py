"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithKNeighbours
import MatplotlibAnimator
import Animator2D

import DefaultValues as dv

n = 50
k = 5
noise = 0
radius= 50
leavingAllowed = False

simulator = VicsekWithKNeighbours.VicsekWithKNeighbours(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, numberOfParticles=n, k=k, noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)
simulationData = simulator.simulate()

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k=k, noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)

# Display Animation
preparedAnimator.showAnimation()

# TODO save values after simulation + option to read existing values

# TODO evaluate result
