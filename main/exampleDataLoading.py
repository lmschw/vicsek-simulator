import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData = SavedModelService.loadModel("examples/HIGHEST_ORIENTATION_DIFFERENCE_n=200_k=5_noise=0_radius=20.json")
modelParams, simulationData = ServiceSavedModel.loadModel("examples/LEAST_ORIENTATION_DIFFERENCE_n=500_k=5_noise=0_radius=10.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParams(modelParams)

# Display Animation
preparedAnimator.showAnimation()