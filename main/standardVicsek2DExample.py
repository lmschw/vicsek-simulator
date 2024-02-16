"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekModel
import MatplotlibAnimator
import Animator2D

import DefaultValues as dv

simulator = VicsekModel.VicsekModel(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D)
simulationData = simulator.simulate()

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (50,50,50))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())

# Display Animation
preparedAnimator.showAnimation()

# TODO evaluate result
