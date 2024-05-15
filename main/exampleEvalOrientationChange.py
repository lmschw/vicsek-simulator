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
metric=Metrics.ORDER_VALUE_PERCENTAGE
xLabel = "Timestep"
yLabel = "number of particles"

density = 0.01
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
tmax = 10000

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = orderValue

angle = 180
eventPercentage = 10

modelParams = []
simulationData = []
colours = []
switchTypeValues = []

# LOCAL
#distributionType = DistributionType.LOCAL_SINGLE_SITE
#area = "[(20, 20, 10)]"
#distributionType = DistributionType.GLOBAL
#area = None

eventPercentage = 30
angle = 180

switchTypeOptions = (orderValue, disorderValue)

differenceThresholds = [0.1,0.3,0.5,0.7,0.9]
previousSteps = [1, 2, 5, 10, 50, 100, 10000]
differenceThresholdLabels = ["0.1", "0.3", "0.5", "0.7", "0.9"]
previousStepsLabels = ["1", "2", "5", "10", "50", "100", "10000"]

threshold = 0.1
percentage = 50

for metric in [Metrics.ORDER, Metrics.ORDER_VALUE_PERCENTAGE]:
    if metric == Metrics.ORDER:
        yLabel = "order"
    else:
        yLabel = "percentage of particles with order value"
    for distributionType in [DistributionType.GLOBAL]:
        if distributionType == DistributionType.GLOBAL:
            area = None
            dist = "Global"
        else:
            area = "[(20, 20, 10)]"
            dist = "Local"
        for initialState in ["random"]:
            if initialState == "random":
                startValue = disorderValue
                targetSwitchValue=orderValue

            else:
                startValue = orderValue
                targetSwitchValue=disorderValue

            labels = [EventEffect.TURN_BY_FIXED_ANGLE.label,
                    EventEffect.ALIGN_TO_FIXED_ANGLE.label,
                    EventEffect.ALIGN_TO_FIRST_PARTICLE.label,
                    EventEffect.AWAY_FROM_ORIGIN.label,
                    EventEffect.TOWARDS_ORIGIN.label]
            for blockSteps in [5, 10, 20, 50, 100]:

                    subtitle = f"{dist} - event effect comparison with \nthreshold = {threshold} and number of blocked steps = {blockSteps} - event at 5000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIRST_PARTICLE,
                                    EventEffect.AWAY_FROM_ORIGIN,
                                    EventEffect.TOWARDS_ORIGIN]:
                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_1.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_2.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_3.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_4.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_5.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_6.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_7.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_8.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_9.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_10.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    #savePath = f"{metric.value}_ps-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_ot=[{singleThreshold}]_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    savePath = f"avg_{metric.value}_effect-comp_bs={blockSteps}_ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created effect comp graph for percentage={percentage}, sth = {threshold} and metric {metric.name}")

            labels = ["5", "10", "20", "50", "100"]
            for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIRST_PARTICLE,
                            EventEffect.AWAY_FROM_ORIGIN,
                            EventEffect.TOWARDS_ORIGIN]:
                    subtitle = f"{dist} - block steps comparison with \nthreshold = {threshold} and effect = {eventEffect.label} - event at 5000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for blockSteps in [5, 10, 20, 50, 100]:


                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_1.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_2.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_3.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_4.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_5.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_6.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_7.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_8.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_9.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_bs={blockSteps}_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_10.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    #savePath = f"{metric.value}_ps-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_ot=[{singleThreshold}]_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    savePath = f"avg_{metric.value}_bs-comp_eventEffect={eventEffect.val}_ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created bs comp graph for effect={eventEffect.name}, sth = {threshold} and metric {metric.name}")
"""
for metric in [Metrics.ORDER, Metrics.ORDER_VALUE_PERCENTAGE]:
    if metric == Metrics.ORDER:
        yLabel = "order"
    else:
        yLabel = "percentage of particles with order value"
    for distributionType in [DistributionType.GLOBAL]:
        if distributionType == DistributionType.GLOBAL:
            area = None
            dist = "Global"
        else:
            area = "[(20, 20, 10)]"
            dist = "Local"
        for initialState in ["ordered", "random"]:
            if initialState == "random":
                startValue = disorderValue
                targetSwitchValue=orderValue

            else:
                startValue = orderValue
                targetSwitchValue=disorderValue


            threshold = 0.1

            labels = [EventEffect.TURN_BY_FIXED_ANGLE.label,
                    EventEffect.ALIGN_TO_FIXED_ANGLE.label,
                    EventEffect.ALIGN_TO_FIRST_PARTICLE.label,
                    EventEffect.AWAY_FROM_ORIGIN.label,
                    EventEffect.TOWARDS_ORIGIN.label]
            for percentage in [10, 30, 50, 70, 100]:

                    subtitle = f"{dist} - event effect comparison with \nthreshold = {threshold} and percentage = {percentage} - events at 5000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIRST_PARTICLE,
                                    EventEffect.AWAY_FROM_ORIGIN,
                                    EventEffect.TOWARDS_ORIGIN]:
                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_1.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_2.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_3.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_4.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_5.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_6.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_7.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_8.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_9.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_10.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    #savePath = f"{metric.value}_ps-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_ot=[{singleThreshold}]_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    savePath = f"avg_{metric.value}_effect-comp_p={percentage}_ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created effect comp graph for percentage={percentage}, sth = {threshold} and metric {metric.name}")

            labels = ["10", "30", "50", "70", "100"]
            for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIRST_PARTICLE,
                            EventEffect.AWAY_FROM_ORIGIN,
                            EventEffect.TOWARDS_ORIGIN]:
                    subtitle = f"{dist} - percentage comparison with \nthreshold = {threshold} and effect = {eventEffect.label} - events at 5000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for percentage in [10, 30, 50, 70, 100]:


                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_1.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_2.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_3.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_4.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_5.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_6.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_7.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_8.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_9.json",
                                                                                                                f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_10.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    #savePath = f"{metric.value}_ps-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_ot=[{singleThreshold}]_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    savePath = f"avg_{metric.value}_p-comp_eventEffect={eventEffect.val}_ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[{threshold}]_psteps=100.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created p comp graph for effect={eventEffect.name}, sth = {threshold} and metric {metric.name}")
"""

"""
for metric in [Metrics.ORDER, Metrics.ORDER_VALUE_PERCENTAGE]:
    if metric == Metrics.ORDER:
        yLabel = "order"
    else:
        yLabel = "percentage of particles with order value"
    for distributionType in [DistributionType.LOCAL_SINGLE_SITE]:
        if distributionType == DistributionType.GLOBAL:
            area = None
            dist = "Global"
        else:
            area = "[(20, 20, 10)]"
            dist = "Local"
        for initialState in ["ordered", "random"]:
            if initialState == "random":
                startValue = disorderValue
            else:
                startValue = orderValue

            for eventEffect in [EventEffect.AWAY_FROM_ORIGIN,
                                EventEffect.TOWARDS_ORIGIN]:

                labels = previousStepsLabels
                for singleThreshold in differenceThresholds:
                    subtitle = f"{dist} - number of previous steps comparison with \ndifference threshold = {singleThreshold} - events at 2000 and 6000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for previousStep in previousSteps:
                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_1.json",
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_2.json",
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_3.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    savePath = f"{metric.value}_ps-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_ot=[{singleThreshold}]_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created ps comp graph for effect={eventEffect.name}, sth = {singleThreshold} and metric {metric.name}")

                labels = differenceThresholdLabels
                for previousStep in previousSteps:
                    subtitle = f"{dist} - difference threshold comparison with \nnumber of previous steps = {previousStep} - events at 2000 and 6000"
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for singleThreshold in differenceThresholds:
                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_1.json",
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_2.json",
                                                                                                                f"D:/vicsek-data/ind-single-with-previous-steps/avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_sth={singleThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_3.json",

                                                                                                                ], loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                    savePath = f"{metric.value}_th-comp_avg_and_single_ind_{initialState}_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d=0.01_LOD_noise=1_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created sth comp graph for for effect={eventEffect.name}, ps = {previousStep} and metric {metric.name}")
"""
"""
mode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
xLabel = "Timestep"

domainSize = (100, 100)
density = 0.01
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
i =1

eventTimestep = 1000

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = orderValue

eventPercentage = 30
angle = 180
orderThreshold = 0.05
distributionType = DistributionType.GLOBAL
switchTypeOptions = (orderValue, disorderValue)

startValue = disorderValue

tmax = 10000
previousSteps = [1, 2, 5, 10, 50, 100, tmax]
lowerThresholds = [0.1, 0.3, 0.5]
upperThresholds = [0.5, 0.7, 0.9]
lowerThresholdLabels = ["0.1", "0.3", "0.5"]
upperThresholdLabels = ["0.5", "0.7", "0.9"]

for metric in [Metrics.ORDER, Metrics.ORDER_VALUE_PERCENTAGE]:
    if metric == Metrics.ORDER:
        yLabel = "order"
    else:
        yLabel = "percentage of particles with order value"
    for distributionType in [DistributionType.LOCAL_SINGLE_SITE]:
        if distributionType == DistributionType.GLOBAL:
            area = None
            dist = "Global"
        else:
            area = "[(20, 20, 10)]"
            dist = "Local"
        for initialState in ["ordered", "random"]:
            if initialState == "random":
                startValue = disorderValue
            else:
                startValue = orderValue

            for eventEffect in [EventEffect.AWAY_FROM_ORIGIN,
                                EventEffect.TOWARDS_ORIGIN]:

                for previousStep in previousSteps:
                    labels = lowerThresholdLabels
                    for upperThreshold in upperThresholds:
                        subtitle = f"{dist} - lower threshold comparison with \n{previousStep} previous steps & upper threshold = {upperThreshold} - events at 2000 and 6000"
                        modelParams = []
                        simulationData = []
                        colours = []
                        switchTypeValues = []
                        for lowerThreshold in lowerThresholds:
                            modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_1.json",
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_2.json",
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_3.json"

                                                                                                                    ], loadSwitchValues=True)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)
                            switchTypeValues.append(switchTypeValuesDensity)

                        #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                        savePath = f"{metric.value}_lt-comp_avg_and_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ut={upperThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                        evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                        ServiceGeneral.logWithTime(f"created lt comp graph for {dist} with effect = {eventEffect}, previous steps = {previousStep}, ut = {upperThreshold} and metric {metric.name}")

                    labels = upperThresholdLabels
                    for lowerThreshold in lowerThresholds:
                        subtitle = f"{dist} - upper threshold comparison with \n{previousStep} previous steps & lower threshold = {lowerThreshold} - events at 2000 and 6000"
                        modelParams = []
                        simulationData = []
                        colours = []
                        switchTypeValues = []
                        for upperThreshold in upperThresholds:
                            modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_1.json",
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_2.json",
                                                                                                                    f"d:/vicsek-data/ind-single-with-previous-steps/avg_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_ot=[{lowerThreshold}, {upperThreshold}]_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_3.json"

                                                                                                                    ], loadSwitchValues=True)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)
                            switchTypeValues.append(switchTypeValuesDensity)

                        #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                        savePath = f"{metric.value}_ut-comp_avg_and_double_ind_{initialState}_st=K_order=5_disorder=1_start={startValue}_d=0.01_LOD_noise=1_lt={lowerThreshold}_psteps={previousStep}_events-t2000e{eventEffect.val}p30a180dt{distributionType.value}a{area}_t6000e{eventEffect.val}p30a180dt{distributionType.value}a{area}.svg"
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                        evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                        ServiceGeneral.logWithTime(f"created ut comp graph for {dist} with effect = {eventEffect.val}, previous steps = {previousStep}, lt = {lowerThreshold} and metric {metric.name}")

"""
