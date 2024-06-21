import ServiceImages
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates scatterplot images/videos for existing data.
--------------------------------------------------------------------------------
"""

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

orderModes = [NeighbourSelectionMode.RANDOM,
              NeighbourSelectionMode.FARTHEST,
              NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
              NeighbourSelectionMode.ALL]

disorderModes = [NeighbourSelectionMode.NEAREST,
                 NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

densities = [0.01, 0.09]

radius = 10
tmax = 1000
domainSize = (100,100)

noisePercentage = 1
k=1

metric = Metrics.ORDER
"""
for density in densities:
    for i in range(1,6):
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)

        for mode in modes:
            ServiceGeneral.logWithTime(f"Starting mode={mode.name}, density={density}, i={i}")
            modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_{i}.json")
            timesteps, positions, orientations = simulationData
            
            ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                                                        startTime=0, endTime=tmax,  
                                                        title=f"{mode.name} - k={k}, n={n}, density={density},noise={noisePercentage}%",
                                                        numberOfExampleParticles=7, selectRandomly=True,
                                                        radius=radius, ylim=(-1.5, 1.5),
                                                        savePath=f"scatter_from-order_tmax={tmax}_mode={mode.name}_density={density}_noise={noisePercentage}_{i}.mp4")
            
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp([[modelParams]], metric, [[simulationData]], evaluationTimestepInterval=100)
            evaluator.evaluateAndVisualize(labels=[mode.name], xLabel="density", yLabel="noise", savePath=f"order_from-order_tmax={tmax}_mode={mode.name}_density={density}-noise={noisePercentage}_{i}.svg")

for density in densities:
    for i in range(1,6):
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)

        for mode in modes:
            ServiceGeneral.logWithTime(f"Random start. Starting mode={mode.name}, density={density}, i={i}")
            modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"D:/vicsek-data/density-vs-noise_random-start/model_density-vs-noise_random-start_{mode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_{i}.json")
            timesteps, positions, orientations = simulationData
            
            ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                                                        startTime=0, endTime=tmax,  
                                                        title=f"{mode.name} - k={k}, n={n}, density={density},noise={noisePercentage}%",
                                                        numberOfExampleParticles=7, selectRandomly=True,
                                                        radius=radius, ylim=(-1.5, 1.5),
                                                        savePath=f"scatter_from-random_tmax={tmax}_mode={mode.name}_density={density}_noise={noisePercentage}_{i}.mp4")
            
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp([[modelParams]], metric, [[simulationData]], evaluationTimestepInterval=100)
            evaluator.evaluateAndVisualize(labels=[mode.name], xLabel="density", yLabel="noise", savePath=f"order_from-random_tmax={tmax}_mode={mode.name}_density={density}-noise={noisePercentage}_{i}.svg")
"""
"""
tmax = 5000
for density in densities:
    for i in range(6,11):
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)

        for orderMode in orderModes:
            for disorderMode in disorderModes:
                ServiceGeneral.logWithTime(f"mode switching. order mode={orderMode.name}, disorder mode={disorderMode.name}. density={density}, i={i}")
                modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"D:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-{orderMode.name}_1000-{disorderMode.name}_4000-{orderMode.name}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json")
                timesteps, positions, orientations = simulationData
                
                
                #ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                #                                            startTime=0, endTime=tmax,  
                #                                            title=f"{orderMode.name}-{disorderMode.name} - k={k}, n={n}, density={density},noise={noisePercentage}%",
                #                                            numberOfExampleParticles=7, selectRandomly=True,
                #                                            radius=radius, ylim=(-1.5, 1.5),
                #                                            savePath=f"scatter_mode-switching_tmax={tmax}_ordermode={orderMode.name}_disordermode={disorderMode.name}_density={density}_noise={noisePercentage}_{i}.mp4")
                
                evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp([[modelParams]], metric, [[simulationData]], evaluationTimestepInterval=100)
                evaluator.evaluateAndVisualize(labels=[f"{orderMode.name}-{disorderMode.name}"], xLabel="density", yLabel="noise", savePath=f"order_mode-switching_tmax={tmax}_ordermode={orderMode.name}_disordermode={disorderMode.name}_density={density}-noise={noisePercentage}_{i}.svg")
"""
"""
tmax = 5000
for density in densities:
    for i in range(1,5):
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)

        orderK = 5
        disorderK = 1
        for mode in disorderModes:
            ServiceGeneral.logWithTime(f"k switching. mode={mode.name}. density={density}, i={i}")
            modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-{orderK}_1000-{disorderK}_4000-{orderK}_tmax={tmax}_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_{i}.json")
            timesteps, positions, orientations = simulationData 
            
            #ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
            #                                            startTime=0, endTime=tmax,  
            #                                            title=f"{mode.name} - k={k}, n={n}, density={density},noise={noisePercentage}%",
            #                                            numberOfExampleParticles=7, selectRandomly=True,
            #                                            radius=radius, ylim=(-1.5, 1.5),
            #                                            savePath=f"scatter_kswitching_tmax={tmax}_mode={mode.name}_density={density}_noise={noisePercentage}_{i}.mp4")
            
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp([[modelParams]], metric, [[simulationData]], evaluationTimestepInterval=100)
            evaluator.evaluateAndVisualize(labels=[mode.name], xLabel="density", yLabel="noise", savePath=f"order_kswitching_tmax={tmax}_mode={mode.name}_density={density}-noise={noisePercentage}_{i}.svg")
"""

files = {"d:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=100_density=0.01_mode=NEAREST_noise=1%_3.json": ["NEAREST", "scatter_kswitching_tmax=5000_mode=NEAREST_density=0.01_noise=1_3.mp4"],
         "d:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=900_density=0.09_mode=NEAREST_noise=1%_4.json": ["NEAREST", "scatter_kswitching_tmax=5000_mode=NEAREST_density=0.09_noise=1_4.mp4"],
         "d:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=100_density=0.01_mode=LEAST_ORIENTATION_DIFFERENCE_noise=1%_4.json": ["LEAST ORIENTATION DIFFERENCE", "scatter_kswitching_tmax=5000_mode=LEAST_ORIENTATION_DIFFERENCE_density=0.01_noise=1_4.mp4"],
         "d:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n=900_density=0.09_mode=LEAST_ORIENTATION_DIFFERENCE_noise=1%_4.json": ["LEAST ORIENTATION DIFFERENCE", "scatter_kswitching_tmax=5000_mode=LEAST_ORIENTATION_DIFFERENCE_density=0.09_noise=1_4.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-RANDOM_1000-NEAREST_4000-RANDOM_tmax=5000_n=100_k=1_noise=1%_8.json": ["RANDOM-NEAREST", "scatter_switching_tmax=5000_modes=RANDOM-NEAREST_density=0.01_noise=1_8.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-RANDOM_1000-NEAREST_4000-RANDOM_tmax=5000_n=900_k=1_noise=1%_1.json": ["RANDOM-NEAREST", "scatter_switching_tmax=5000_modes=RANDOM-NEAREST_density=0.09_noise=1_1.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-RANDOM_1000-LEAST_ORIENTATION_DIFFERENCE_4000-RANDOM_tmax=5000_n=100_k=1_noise=1%_7.json": ["RANDOM-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=RANDOM-LEAST_ORIENTATION_DIFFERENCE_density=0.01_noise=1_7.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-RANDOM_1000-LEAST_ORIENTATION_DIFFERENCE_4000-RANDOM_tmax=5000_n=900_k=1_noise=1%_1.json": ["RANDOM-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=RANDOM-LEAST_ORIENTATION_DIFFERENCE_density=0.09_noise=1_1.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-HIGHEST_ORIENTATION_DIFFERENCE_1000-NEAREST_4000-HIGHEST_ORIENTATION_DIFFERENCE_tmax=5000_n=100_k=1_noise=1%_6.json": ["HIGHEST ORIENTATION DIFFERENCE-NEAREST", "scatter_switching_tmax=5000_modes=HIGHEST_ORIENTATION_DIFFERENCE-NEAREST_density=0.01_noise=1_6.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-HIGHEST_ORIENTATION_DIFFERENCE_1000-NEAREST_4000-HIGHEST_ORIENTATION_DIFFERENCE_tmax=5000_n=900_k=1_noise=1%_6.json": ["HIGHEST ORIENTATION DIFFERENCE-NEAREST", "scatter_switching_tmax=5000_modes=HIGHEST_ORIENTATION_DIFFERENCE-NEAREST_density=0.09_noise=1_6.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-HIGHEST_ORIENTATION_DIFFERENCE_1000-LEAST_ORIENTATION_DIFFERENCE_4000-HIGHEST_ORIENTATION_DIFFERENCE_tmax=5000_n=100_k=1_noise=1%_6.json": ["HIGHEST ORIENTATION DIFFERENCE-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=HIGHEST_ORIENTATION_DIFFERENCE-LEAST_ORIENTATION_DIFFERENCE_density=0.01_noise=1_6.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-HIGHEST_ORIENTATION_DIFFERENCE_1000-LEAST_ORIENTATION_DIFFERENCE_4000-HIGHEST_ORIENTATION_DIFFERENCE_tmax=5000_n=900_k=1_noise=1%_1.json": ["HIGHEST ORIENTATION DIFFERENCE-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=HIGHEST_ORIENTATION_DIFFERENCE-LEAST_ORIENTATION_DIFFERENCE_density=0.09_noise=1_1.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-FARTHEST_1000-NEAREST_4000-FARTHEST_tmax=5000_n=100_k=1_noise=1%_9.json": ["FARTHEST-NEAREST", "scatter_switching_tmax=5000_modes=FARTHEST-NEAREST_density=0.01_noise=1_9.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-FARTHEST_1000-NEAREST_4000-FARTHEST_tmax=5000_n=900_k=1_noise=1%_6.json": ["FARTHEST-NEAREST", "scatter_switching_tmax=5000_modes=FARTHEST-NEAREST_density=0.09_noise=1_6.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-FARTHEST_1000-LEAST_ORIENTATION_DIFFERENCE_4000-FARTHEST_tmax=5000_n=100_k=1_noise=1%_8.json": ["FARTHEST-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=FARTHEST-LEAST_ORIENTATION_DIFFERENCE_density=0.01_noise=1_8.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-FARTHEST_1000-LEAST_ORIENTATION_DIFFERENCE_4000-FARTHEST_tmax=5000_n=900_k=1_noise=1%_1.json": ["FARTHEST-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=FARTHEST-LEAST_ORIENTATION_DIFFERENCE_density=0.09_noise=1_1.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-ALL_1000-NEAREST_4000-ALL_tmax=5000_n=100_k=1_noise=1%_6.json": ["ALL-NEAREST", "scatter_switching_tmax=5000_modes=ALL-NEAREST_density=0.01_noise=1_6.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-ALL_1000-NEAREST_4000-ALL_tmax=5000_n=900_k=1_noise=1%_2.json": ["ALL-NEAREST", "scatter_switching_tmax=5000_modes=ALL-NEAREST_density=0.09_noise=1_2.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-ALL_1000-LEAST_ORIENTATION_DIFFERENCE_4000-ALL_tmax=5000_n=100_k=1_noise=1%_9.json": ["ALL-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=ALL-LEAST_ORIENTATION_DIFFERENCE_density=0.01_noise=1_9.mp4"],
         "d:/vicsek-data/switching/switch_switchType=NEIGHBOUR_SELECTION_MODE_switches=0-ALL_1000-LEAST_ORIENTATION_DIFFERENCE_4000-ALL_tmax=5000_n=900_k=1_noise=1%_2.json": ["ALL-LEAST ORIENTATION DIFFERENCE", "scatter_switching_tmax=5000_modes=ALL-LEAST_ORIENTATION_DIFFERENCE_density=0.09_noise=1_2.mp4"],
         }

for key, val in files.items():
    modelParams, simulationData, colours = ServiceSavedModel.loadModel(key)
    timesteps, positions, orientations = simulationData 

    ServiceImages.createNeighbourScatterplotVideoMulti(positions=positions, orientations=orientations,
                                                startTime=0, endTime=tmax,  
                                                title=f"{val[0]}, noise={noisePercentage}%",
                                                numberOfExampleParticles=7, selectRandomly=True,
                                                radius=radius, ylim=(-1.5, 1.5),
                                                savePath=val[1])



