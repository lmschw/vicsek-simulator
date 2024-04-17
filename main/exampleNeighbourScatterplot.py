import ServiceImages
import ServiceSavedModel
import time

index = ["distance", "orientation difference"]

modelParams, simulationData, colours = ServiceSavedModel.loadModel("kswitching/switch_switchType=K_switches=0-3_1000-1_4000-3_tmax=5000_n=100_noise=1%_1.json")
timesteps, positions, orientations = simulationData

"""
ServiceImages.createNeighbourScatterplot(positions=positions, orientations=orientations,
                                         numberOfExampleParticles=10, selectRandomly=False, 
                                         numberOfSteps=10, radius=10, index=index,
                                         savePath="test_scatter_kswitching.svg")
"""
"""
ServiceImages.createNeighbourScatterplot(positions=positions, orientations=orientations,
                                         numberOfExampleParticles=5, selectRandomly=True, 
                                         steps=[0, 1000, 1100, 1200, 3800, 3900, 4000, 4100, 4200, 5000], radius=10, index=index,
                                         savePath="test_scatter_kswitching_focused.svg")
"""
"""
ServiceImages.createNeighbourScatterplot(positions=positions, orientations=orientations,
                                         numberOfExampleParticles=5, selectRandomly=True, 
                                         steps=[1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400], radius=10, index=index,
                                         savePath="test_scatter_kswitching_focused_diverging.svg")
"""

ServiceImages.createNeighbourScatterplotVideo(positions=positions, orientations=orientations,
                                              radius=10, ylim=(-1.1, 1.1),
                                              savePath="test_scatter_kswitching_video.mp4")
