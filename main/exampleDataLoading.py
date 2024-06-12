import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

"""
--------------------------------------------------------------------------------
PURPOSE 
Loads a saved model and creates a video.
--------------------------------------------------------------------------------
"""

datafileLocation = ""
filename = ""
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=True)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=25)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation(f"{filename}.mp4")

# Display Animation
#preparedAnimator.showAnimation()