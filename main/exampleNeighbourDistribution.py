import ServiceImages
import ServiceSavedModel

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates a plot for the neighbour distances.
--------------------------------------------------------------------------------
"""

radius = 10
tmax = 5000
noisePercentage = 0
filename = "ind_random_st=K_order=5_disorder=1_start=5_d=0.01_LEAST_ORIENTATION_DIFFERENCE_noise=0_ot=0.1_events-t1000p1a45dtGaNone_1.json.json"
modeName = "NEAREST"
savePath = "scatter_kswitching_tmax=5000_mode=NEAREST_density=0.01_noise=1_3.mp4"

modelParams, simulationData, colours = ServiceSavedModel.loadModel(filename)
timesteps, positions, orientations = simulationData 

ServiceImages.createNeighourDistributionPlotDistance(positions=positions, orientations=orientations,
                                            startTime=0, endTime=100,  
                                            title=f"{modeName}, noise={noisePercentage}%",
                                            numberOfExampleParticles=7, selectRandomly=True,
                                            radius=radius, savePath=savePath)