import EnumNeighbourSelectionMode
import EnumMetrics
import ServiceSavedModel
import EvaluatorMultiAvgComp
import ServicePreparation


"""
--------------------------------------------------------------------------------
PURPOSE 
Evaluates and visualises the results of multiple simulation runs.
--------------------------------------------------------------------------------
"""

"""
mode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
n = 500
k = 5
radius =10
tmax = 1000
noise = 0
metric = EnumMetrics.Metrics.ORDER
densities = [0.005, 0.01, 0.04, 0.05, 0.08, 0.1]
"""
"""
for density in densities:
    for i in range(1,10):
        domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)

        print(f"i={i}, n={n}, density={density}, domainSize={domainSize}")

        k = 5
        noise = 0
        radius= 10
        neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
        tmax = 1000

        simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                        domainSize=domainSize, 
                                                                        numberOfParticles=n, 
                                                                        k=k, 
                                                                        noise=noise, 
                                                                        radius=radius)
        simulationData, colours = simulator.simulate(tmax=tmax)

        # Save model values for future use
        ServiceSavedModel.saveModel(simulationData, colours, f"examples/densityExamples/{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_{i}.json", simulator.getParameterSummary())

"""
"""
mode = EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE
n = 500
k = 5
radius =10
tmax = 1000
noise = 0
metric = EnumMetrics.Metrics.ORDER
densities = [0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

modelParams = []
simulationData = []
colours = []

for density in densities:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_1.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_2.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_3.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_4.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_5.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_6.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_7.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_8.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_9.json",
                                                                        f"examples/densityExamples/HOD/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_density={density}_10.json"
                                                                        ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData)
evaluator.evaluateAndVisualize(labels=["density=0.005",  "density=0.01", "density=0.02", "density=0.03", "density=0.04", "density=0.05", "density=0.06", "density=0.07", "density=0.08", "density=0.09", "density=0.1"], subtitle=f"Comparing average density for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode.name}_n={n}_k={k}_noise={noise}_radius={radius}_density-comparison-fewer-comps.png")

"""
"""
n=500
k=5
mode=EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax=10000
radius=10

metric=EnumMetrics.Metrics.CLUSTER_SIZE
noises=[0.1, 0.2, 0.3, 0.4]
labels=["noise=0.1", "noise=0.2", "noise=0.3", "noise=0.4"]
#labels=["noise=0.1", "noise=0.2", "noise=0.3"]
#labels=["noise=0.1", "noise=0.2"]
#labels=["noise=0.1"]


modelParams = []
simulationData = []
colours = []

for noise in noises:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_1.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_2.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_3.json"])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=500)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing average cluster number for dislocation from order based on noise for {mode.name}, \nn={n}, k={k}, radius={radius}", savePath=f"{mode.name}_n={n}_k={k}_radius={radius}_dislocation-comparison-based-on-noise.png")
"""

"""
n=500
k=5
mode=EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax=10000
radius=10
noises=[0.1, 0.2, 0.3, 0.4]

metric=EnumMetrics.Metrics.CLUSTER_NUMBER
labels=["noise=0.1", "noise=0.2", "noise=0.3", "noise=0.4"]


modelParams = []
simulationData = []
colours = []

for noise in noises:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_1.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_2.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}_3.json"])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=500, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing average cluster number for dislocation from order for {mode.name}, \nn={n}, k={k}, noise={noise}, radius={radius}, threshold={threshold}", savePath=f"{mode.name}_n={n}_k={k}_radius={radius}_dislocation-noise=comp-0.1-0.2_hierarchical_clustering_threshold={threshold}.png")
"""

"""
n=500
k=5
mode=EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE
tmax=3000
radius=10
noises=[0.5, 1, 1.5, 2, 2.5, 3]

metric=EnumMetrics.Metrics.CLUSTER_SIZE
labels=["noisePercentage=0.5", "noisePercentage=1", "noisePercentage=1.5", "noisePercentage=2", "noisePercentage=2.5", "noisePercentage=3"]


modelParams = []
simulationData = []
colours = []

for noise in noises:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_1.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_2.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_3.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_4.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_5.json"
                                                                                            ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=300, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing average cluster size \nfor dislocation from order for {mode.name}, \nn={n}, k={k}, noise={noise}, radius={radius}, threshold={threshold}", savePath=f"{metric.name}_{mode.name}_n={n}_k={k}_radius={radius}_dislocation-noise=comp-small-percentages_hierarchical_clustering_threshold={threshold}.png")


"""
"""
n=500
k=5
noise=3
tmax=3000
radius=10
modes = [EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

metric=EnumMetrics.Metrics.CLUSTER_NUMBER
labels=["RANDOM", "NEAREST", "FARTHEST", "LEAST_ORIENTATION_DIFFERENCE", "HIGHEST_ORIENTATION_DIFFERENCE"]


modelParams = []
simulationData = []
colours = []

for mode in modes:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_1.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_2.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_3.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_4.json",
                                                                                            f"examples/dislocationExamples/model_{mode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noise}%_radius={radius}_5.json"
                                                                                            ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=300, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing average {metric.name} \nfor dislocation from order between modes, \nn={n}, k={k}, noise={noise}, radius={radius}, threshold={threshold}", savePath=f"{metric.name}_mode-comparision_n={n}_k={k}_radius={radius}_dislocation-noise={noise}%_hierarchical_clustering_threshold={threshold}.png")

"""

"""
n=50
k=1
noise=3
tmax=3000
radius=10
metric=EnumMetrics.Metrics.CLUSTER_CONSISTENCY_AVERAGE_STEPS
labels=["r=5", "r=10", "r=15"]


modelParams = []
simulationData = []
colours = []

modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                        f"switch_FARTHEST_switchType=SwitchType.NEIGHBOUR_SELECTION_MODE_switches=10-NEAREST_40-FARTHEST_tmax=50_n=50_k=1_noise=0.06283185307179587_radius=10.json",
                                                                                            ])
modelParams.append(modelParamsDensity)
simulationData.append(simulationDataDensity)
colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=1, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, subtitle=f"Comparing radius for dislocation from order, \nn={n}, noise={noise}, k={k}, threshold={threshold}", savePath=f"{metric.name}_n={n}_dislocation-noise={noise}%_hierarchical_clustering_threshold={threshold}.png")
"""

"""

tmax=1000
radius=10
domainSize=(100,100)
modes = [EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.ALL]

metric=EnumMetrics.Metrics.CLUSTER_NUMBER
labels=["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]
xLabel = "Timestep"
yLabel = "Number of clusters"

density = 0.05
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
k = 1
modelParams = []
simulationData = []
colours = []

for mode in modes:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_2.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_3.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_4.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_5.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_6.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_7.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_8.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_9.json",
                                                                                            f"D:/vicsek-data/density-vs-noise/model_density-vs-noise_{mode.name}_tmax=1000_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius=10_10.json",
                                                                                            ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, savePath=f"clusternumber_mode-comp_ordered_density=0.05_noise=1.svg")
"""

"""
tmax=100000
radius=10
domainSize=(100,100)
modes = [EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

metric=EnumMetrics.Metrics.ORDER
labels=["NEAREST", "LEAST ORIENTATION DIFFERENCE"]
xLabel = "Timestep"
yLabel = "Number of clusters"

density = 0.01
noisePercentage = 0
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
k = 3
tmax = 100000
modelParams = []
simulationData = []
colours = []

for mode in modes:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"main/longer_runs/model_density-vs-noise_random-start_{mode.name}_tmax={tmax}_density=0.01_n=100_k=3_noisePercentage={noisePercentage}%_radius=10_1.json",
                                                                                            ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, savePath=f"order-random-start-k=3-noise={noisePercentage}-tmax={tmax}.svg")
"""
tmax=5000
radius=10
domainSize=(100,100)
modes = [EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

metric=EnumMetrics.Metrics.ORDER
labels=["NEAREST", "LEAST ORIENTATION DIFFERENCE"]
xLabel = "Timestep"
yLabel = "order"

density = 0.01
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
tmax = 5000
modelParams = []
simulationData = []
colours = []

for mode in modes:
    modelParamsDensity, simulationDataDensity, coloursDensity = ServiceSavedModel.loadModels([
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_1.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_2.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_3.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_4.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_5.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_6.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_7.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_8.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_9.json",
                                                                                            f"D:/vicsek-data/kswitching/switch_switchType=K_switches=0-5_1000-1_4000-5_tmax=5000_n={n}_density={density}_mode={mode.name}_noise={noisePercentage}%_10.json",
                                                                                            ])
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)


threshold = 0.01
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, threshold=threshold)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, savePath=f"order-kswitching-density={density}-noise={noisePercentage}-tmax={tmax}.svg")




