from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect

import ServiceSavedModel
import EvaluatorMultiAvgComp
import VicsekWithNeighbourSelection
import ServicePreparation
import ServiceGeneral

import DefaultValues as dv
import AnimatorMatplotlib
import Animator2D

tmax=5000
radius=10
domainSize=(100,100)

#orderThresholds = [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]
#percentages = [1, 5, 10, 30, 50]
#angles = [45, 90, 180, 270]

orderThresholds = [0.1, 0.3, 0.5, 0.7]
percentages = [1, 5, 10, 30, 50]
angles = [45, 90, 180]

orderThresholdLabels = ["0.1", "0.3", "0.5", "0.7"]
percentagesLabels = ["1", "5", "10", "30", "50"]
anglesLabels = ["45", "90", "180"]

mode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
metric=Metrics.SWITCH_VALUE_DISTRIBUTION
xLabel = "Timestep"
yLabel = "number of particles"

density = 0.01
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
tmax = 5000
i =1

eventTimestep = 1000

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = orderValue

angle = 180
eventPercentage = 10
orderThreshold = 0.3
distributionType = DistributionType.GLOBAL
area = None

modelParams = []
simulationData = []
colours = []
switchTypeValues = []

"""
labels = anglesLabels
subtitle = "Angle comparison"
for angle in angles:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-angle_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = percentagesLabels
subtitle = "Percentage comparison"
for eventPercentage in percentages:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-percentage_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = orderThresholdLabels
subtitle = "Order threshold comparison"
for orderThreshold in orderThresholds:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""

# LOCAL
area = "[[20, 20, 10]]"
distributionType = DistributionType.LOCAL_SINGLE_SITE

"""
labels = anglesLabels
subtitle = "Angle comparison - local"
for angle in angles:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-angle_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = percentagesLabels
subtitle = "Percentage comparison - local"
for eventPercentage in percentages:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-percentage_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = orderThresholdLabels
subtitle = "Order threshold comparison - local"
for orderThreshold in orderThresholds:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
# DISORDER VALUES NUMBERS

"""
labels = anglesLabels
subtitle = "Angle comparison"
for angle in angles:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-angle_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = percentagesLabels
subtitle = "Percentage comparison"
for eventPercentage in percentages:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-percentage_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = orderThresholdLabels
subtitle = "Order threshold comparison"
for orderThreshold in orderThresholds:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""

# LOCAL
area = "[[20, 20, 10]]"
distributionType = DistributionType.LOCAL_SINGLE_SITE

"""
labels = anglesLabels
subtitle = "Angle comparison - local"
xLabel = "number of particles with disorder value"
for angle in angles:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-angle_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = percentagesLabels
subtitle = "Percentage comparison - local"
for eventPercentage in percentages:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-percentage_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""
"""
labels = orderThresholdLabels
subtitle = "Order threshold comparison - local"
for orderThreshold in orderThresholds:
    modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                            f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{mode.value}_noise={noisePercentage}_ot={orderThreshold}_events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}_{i}.json.json",
                                                                                            ], loadSwitchValues=True)
    modelParams.append(modelParamsDensity)
    simulationData.append(simulationDataDensity)
    colours.append(coloursDensity)
    switchTypeValues.append(switchTypeValuesDensity)

evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues)
evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=f"numdisorder-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg")
"""

eventTimestep = 1500
eventPercentage = 30
angle = 180
orderThreshold = 0.05
distributionType = DistributionType.GLOBAL
area = None
switchTypeOptions = (orderValue, disorderValue)

startValue = disorderValue

tmax = 10000
lowerThresholds = [0.1, 0.2, 0.3, 0.4, 0.5]
upperThresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
lowerThresholdLabels = ["0.1", "0.2", "0.3", "0.4", "0.5"]
upperThresholdLabels = ["0.5", "0.6", "0.7", "0.8", "0.9"]

for eventEffect in [EventEffect.ALIGN_TO_FIRST_PARTICLE, EventEffect.ALIGN_TO_FIXED_ANGLE]:
    for metric in [Metrics.ORDER, Metrics.SWITCH_VALUE_DISTRIBUTION]:
        if metric == Metrics.ORDER:
            yLabel = "order"
        else:
            yLabel = "number of particles"
        labels = lowerThresholdLabels
        for upperThreshold in upperThresholds:
            subtitle = f"Global - lower threshold comparison with \nupper threshold = {upperThreshold} - events at 2000 and 6000"
            modelParams = []
            simulationData = []
            colours = []
            switchTypeValues = []
            for lowerThreshold in lowerThresholds:
                modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_1.json",
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_2.json",
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_3.json"

                                                                                                        ], loadSwitchValues=True)
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)
                switchTypeValues.append(switchTypeValuesDensity)

            #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
            savePath = f"{metric.value}_lt-comp_ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone.svg"
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
            evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
            ServiceGeneral.logWithTime(f"created lt comp graph for ut = {upperThreshold} and metric {metric.name}")

        labels = upperThresholdLabels
        for lowerThreshold in lowerThresholds:
            subtitle = f"Global - upper threshold comparison \nwith lower threshold = {lowerThreshold} - events at 2000 and 6000"
            modelParams = []
            simulationData = []
            colours = []
            switchTypeValues = []
            for upperThreshold in upperThresholds:
                modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_1.json",
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_2.json",
                                                                                                        f"ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_ut={upperThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone_3.json"

                                                                                                        ], loadSwitchValues=True)
                modelParams.append(modelParamsDensity)
                simulationData.append(simulationDataDensity)
                colours.append(coloursDensity)
                switchTypeValues.append(switchTypeValuesDensity)

            #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
            savePath = f"{metric.value}_ut-comp_ind_random_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_events-t2000e{eventEffect.value}p30a180dtGaNone_t6000e{eventEffect.value}p30a180dtGaNone.svg"
            evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
            evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
            ServiceGeneral.logWithTime(f"created ut comp graph for lt = {lowerThreshold} and metric {metric.name}")
