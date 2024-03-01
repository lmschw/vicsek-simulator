"""
Contains a simulation for the standard 2D Vicsek model
"""

import main.oldVersionForTemporaryReference.VicsekStandardModel as VicsekStandardModel
import main.AnimatorMatplotlib as AnimatorMatplotlib
import Animator2D

import DefaultValues as dv

simulator = VicsekStandardModel.VicsekModel(domainSize=dv.DEFAULT_DOMAIN_SIZE_2D)
simulationData = simulator.simulate()

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (50,50,50))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())

# Display Animation
preparedAnimator.showAnimation()

# TODO evaluate result