import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0_radius=10.json")
modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/switch/switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=5_noise=0.031415926535897934_radius=10.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=5000)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation('examples/switch/switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=1000-NEAREST_4000-FARTHEST_tmax=5000_n=500_k=5_noise=0.031415926535897934_radius=10.mp4')

# Display Animation
preparedAnimator.showAnimation()