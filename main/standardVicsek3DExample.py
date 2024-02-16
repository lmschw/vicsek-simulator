"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekModel
import MatplotlibAnimator
import Animator3D

import DefaultValues as dv

simulator = VicsekModel.VicsekModel(domainSize=dv.DEFAULT_DOMAIN_SIZE_3D)
simulationData = simulator.simulate()

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (50,50,50))

# prepare the animator
preparedAnimator = animator.prepare(Animator3D.Animator3D())

# Display Animation
preparedAnimator.showAnimation()

# TODO evaluate result
