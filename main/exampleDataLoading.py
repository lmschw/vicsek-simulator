import AnimatorMatplotlib
import SavedModelService
import Animator2D

n = 500
k1 = 2
k2 = 10
noise = 0
radius= 100

modelParams, simulationData = SavedModelService.loadModel("neighbour_selection_mode.json")

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k=k1, noise=noise, radius=radius)

# Display Animation
preparedAnimator.showAnimation()