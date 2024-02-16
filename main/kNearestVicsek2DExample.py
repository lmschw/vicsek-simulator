"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithKNeighbours
import MatplotlibAnimator
import Animator2D

import DefaultValues as dv

simulator = VicsekWithKNeighbours.VicsekWithKNeighbours(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, numberOfParticles=500, k=2)
simulationData = simulator.simulate()

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (50,50,50))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())

# Display Animation
preparedAnimator.showAnimation()

# TODO evaluate result
