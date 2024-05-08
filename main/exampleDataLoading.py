import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0_radius=10.json")
#modelParams, simulationData, colours = ServiceSavedModel.loadModel("D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=100_density=0.01_mode=NEAREST_noise=1.5%_2.json")
#datafileLocation = "d:/vicsek-data/ind-single-with-previous-steps/"
datafileLocation = ""
filename = ""
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=True)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=10000)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation(f"{filename}.mp4")

# Display Animation
#preparedAnimator.showAnimation()