import AnimatorMatplotlib
import SavedModelService
import Animator2D

modelParams, simulationData = SavedModelService.loadModel("neighbour_selection_mode.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParams(modelParams)

# Display Animation
preparedAnimator.showAnimation()