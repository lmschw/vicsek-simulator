import AnimatorMatplotlib
import ServiceSavedModel
import Animator2D

#modelParams, simulationData, colours = ServiceSavedModel.loadModel("examples/dislocationExamples/model_LEAST_ORIENTATION_DIFFERENCE_tmax=10000_n=500_k=5_noise=0_radius=10.json")
#modelParams, simulationData, colours = ServiceSavedModel.loadModel("D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=100_density=0.01_mode=NEAREST_noise=1.5%_2.json")
for filename in [
            "avg_double_ind_ordered_st=K_order=5_disorder=1_start=5_d=0.01_LOD_noise=1_ot=[0.3, 0.7]_psteps=10000_events-t2000eorigin_top30a180dtLSSa[(20, 20, 10)]_t6000eorigin_top30a180dtLSSa[(20, 20, 10)]_2",
            "avg_double_ind_ordered_st=K_order=5_disorder=1_start=5_d=0.01_LOD_noise=1_ot=[0.5, 0.7]_psteps=10000_events-t2000eorigin_top30a180dtLSSa[(20, 20, 10)]_t6000eorigin_top30a180dtLSSa[(20, 20, 10)]_2",
        ]:
    modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"d:/vicsek-data/ind-single-with-previous-steps/{filename}.json", loadSwitchValues=True)

    # Initalise the animator
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=10000)
    preparedAnimator.setParams(modelParams)

    preparedAnimator.saveAnimation(f"{filename}.mp4")

    # Display Animation
    #preparedAnimator.showAnimation()