import MatplotlibAnimator
import SavedModelService
import Animator2D

n = 500
k1 = 2
k2 = 10
noise = 0
radius= 100
leavingAllowed = False

simulationData = SavedModelService.loadModel("sample.json")

# Initalise the animator
animator = MatplotlibAnimator.MatplotlibAnimator(simulationData, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D())
preparedAnimator.setParameters(n=n, k="k1={k1}, k2={k2}", noise=noise, radius=radius, particlesAllowedToLeave=leavingAllowed)

# Display Animation
preparedAnimator.showAnimation()