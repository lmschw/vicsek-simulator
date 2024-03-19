import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0_radius=10.json")
modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/individualSwitches/model_switch_individuals_grouped_secondmost_changeAt=100_default=FARTHEST_tmax=2000_n=500_k=5_noise=0_radius=10.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=2000)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation('examples/individualSwitches/model_switch_individuals_grouped_secondmost_changeAt=100_default=FARTHEST_tmax=2000_n=500_k=5_noise=0_radius=10.mp4')

# Display Animation
preparedAnimator.showAnimation()