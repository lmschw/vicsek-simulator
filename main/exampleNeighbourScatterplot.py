import ServiceImages
import ServiceSavedModel
import ServicePreparation
import ServiceGeneral
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import time

index = ["distance", "orientation difference"]

"""
modelParams, simulationData, colours = ServiceSavedModel.loadModel("kswitching/switch_switchType=K_switches=0-3_1000-1_4000-3_tmax=5000_n=100_noise=1%_1.json")
timesteps, positions, orientations = simulationData
"""

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
"""
ServiceImages.createNeighbourScatterplotVideo(positions=positions, orientations=orientations,
                                              startTime=1000, endTime=2000,
                                              radius=10, ylim=(-1.1, 1.1),
                                              savePath="test_scatter_kswitching_video.mp4")
"""
"""
ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                                              startTime=0, endTime=5000, 
                                              numberOfExampleParticles=5, selectRandomly=True,
                                              radius=10, ylim=(-1.5, 1.5),
                                              savePath="test_scatter_kswitching_video_multi.mp4")

"""

modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]

densities = [0.01, 0.09]

radius = 10
tmax = 1000
domainSize = (100,100)

noisePercentage = 1
k=1

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)

    for mode in [NeighbourSelectionMode.NEAREST']:
        ServiceGeneral.logWithTime(f"Starting mode={mode.name}, density={density}")
        modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json")
        timesteps, positions, orientations = simulationData
        ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                                                    startTime=0, endTime=tmax,  
                                                    title=f"{mode.name} - k={k}, n={n}, density={density},noise={noisePercentage}%",
                                                    numberOfExampleParticles=5, selectRandomly=True,
                                                    radius=radius, ylim=(-1.5, 1.5),
                                                    savePath=f"scatter_from-order_tmax={tmax}_mode={mode.name}_density={density}_noise={noisePercentage}_1.mp4")