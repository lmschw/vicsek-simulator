import AnimatorMatplotlib
import SavedModelService
import Animator2D

modelParams, simulationData = SavedModelService.loadModel("RANDOM_n=100_k=1_noise=0_radius=20.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParams(modelParams)

# Display Animation
preparedAnimator.showAnimation()