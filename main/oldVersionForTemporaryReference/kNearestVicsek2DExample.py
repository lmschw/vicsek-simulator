"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithKNeighbours
import main.AnimatorMatplotlib as AnimatorMatplotlib
import Animator2D

import DefaultValues as dv

n = 200
k = 2
noise = 0
radius= 20
leavingAllowed = False

simulator = VicsekWithKNeighbours.VicsekWithKNeighbours(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, numberOfParticles=n, k=k, noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)
simulationData = simulator.simulate()

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k=k, noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)

# Display Animation
preparedAnimator.showAnimation()

# TODO save values after simulation + option to read existing values

# TODO evaluate result
