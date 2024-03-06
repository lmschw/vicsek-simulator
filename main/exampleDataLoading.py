import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/general/LEAST_ORIENTATION_DIFFERENCE_n=200_k=5_noise=0_radius=20.json")
#modelParams, simulationData, colours = ServiceSavedModel.loadModel("LEAST_ORIENTATION_DIFFERENCE_tmax=20000_n=400_k=5_noise=0.1_radius=10.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=1000)
preparedAnimator.setParams(modelParams)

#preparedAnimator.saveAnimation('vicsek2.mp4')

# Display Animation
preparedAnimator.showAnimation()