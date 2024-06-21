import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

"""
--------------------------------------------------------------------------------
PURPOSE 
Loads a saved model and creates a video.
--------------------------------------------------------------------------------
"""

datafileLocation = ""
filename = "test-speed=1_1e_360°_TURN-lssmid-drn=500_ind_avg_hst_random_st=K_o=5_do=1_s=1_d=0.09_n=100_r=10_LOD_noise=1_th=[0.1]_psteps=100_bs=-1_e-500-turn_fixed_10000-turn_fixed_15000-turn_fixed_1"
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=True)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=25)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation(f"{filename}.mp4")

# Display Animation
#preparedAnimator.showAnimation()