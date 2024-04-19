import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0_radius=10.json")
#modelParams, simulationData, colours = ServiceSavedModel.loadModel("D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=100_density=0.01_mode=NEAREST_noise=1.5%_2.json")
filename = "switch_individual_switchType=K_orderVal=5_disorderVal=1_tmax=5000_n=300_density=0.03_mode=NEAREST_noise=1%_orderthreshold=0.7_1.json"
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(filename, loadSwitchValues=True)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=5000)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation('switch_individual_switchType=K_orderVal=5_disorderVal=1_tmax=5000_n=300_noise=1%_orderthreshold=0.7_1.mp4')

# Display Animation
preparedAnimator.showAnimation()