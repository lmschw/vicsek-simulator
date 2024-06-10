import AnimatorHeatmap
import ServiceSavedModel
import ServiceMetric

#data = [0.1,0.2,0.3], [[[0.1,0.2],[0.1,0.3],[0.1,0.1]],[[0.2,0.2],[0.2,0.2],[0.2,0.2]],[[1,0.3],[0.3,0.3],[0.3,0.3]]]

datafileLocation = ""
filename = "switch-lssmid-drn=100_ind_avg_hst_random_st=K_o=5_do=1_s=1_d=0.09_n=100_r=10_LOD_noise=1_th=[0.1]_psteps=100_bs=-1_e-500-turn_fixed_1000-origin_away_1500-turn_fixed_1"
modelParams, simulationData, colours, switchValues = ServiceSavedModel.loadModel(f"{datafileLocation}{filename}.json", loadSwitchValues=True)

times, grid = ServiceMetric.getLocalOrderGrid(simulationData, domainSize=(33.333333333333336, 33.333333333333336))

animator = AnimatorHeatmap.Animator()
animator.prepareAnimation()
animator.setSimulationData((times, grid))
animator.showAnimation()