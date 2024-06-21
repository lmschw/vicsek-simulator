import numpy as np

from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

import ServiceSavedModel
import EvaluatorMultiAvgComp
import ServicePreparation
import ServiceGeneral

"""
--------------------------------------------------------------------------------
PURPOSE 
Evaluates the field of vision simulations
--------------------------------------------------------------------------------
"""


radius=10
domainSize=(100,100)

mode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
metric=Metrics.ORDER_VALUE_PERCENTAGE
xLabel = "Timestep"
yLabel = "number of particles"

density = 0.01
noisePercentage = 1
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
tmax = 2500

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = orderValue

angle = np.pi
eventPercentage = 10

switchTypeOptions = (orderValue, disorderValue)

modelParams = []
simulationData = []
colours = []
switchTypeValues = []

# LOCAL
#distributionType = DistributionType.LOCAL_SINGLE_SITE
#area = "[(20, 20, 10)]"
#distributionType = DistributionType.GLOBAL
#area = None
thresholdVals = [[0.1,0.9], [0.2, 0.9], [0.3, 0.9], [0.4, 0.9], [0.5, 0.9], [0.6,0.9], [0.7,0.9]]
thresholdLabels =  ["[0.1,0.9]", "[0.2, 0.9]", "[0.3, 0.9]", "[0.4, 0.9]", "[0.5, 0.9]", "[0.6,0.9]", "[0.7,0.9]"]
radiusVals = [5, 10, 20, 30, 50, 100]
radiusLabels = ["5", "10", "20", "30", "50", "100"]

blockSteps = -1
numberOfPreviousSteps = 100
percentage = 50
radius = 10
threshold = [0.1]
movementPattern = MovementPattern.STATIC
density = 0.09
for metric in [Metrics.ORDER]:
    if metric == Metrics.ORDER:
        yLabel = "order"
    else:
        yLabel = "percentage of particles with order value"
    for distributionType in [DistributionType.LOCAL_SINGLE_SITE]:
        if distributionType == DistributionType.GLOBAL:
            area = None
            dist = "Global"
        else:
            area = "[(16,67, 16.67, 10)]"
            dist = "Local"
        for initialState in ["ordered"]:
            if initialState == "random":
                startValue = disorderValue
                targetSwitchValue=orderValue

            else:
                startValue = orderValue
                targetSwitchValue=disorderValue
            for degreesOfVision in [2*np.pi]:
                labels = [degreesOfVision]
                for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                                    ]:
                        subtitle = f"Field of vision: {degreesOfVision}"
                        modelParams = []
                        simulationData = []
                        colours = []
                        switchTypeValues = []
                        for thresholdType in [ThresholdType.HYSTERESIS]:
                            modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels([
f"test_occ_3e-{degreesOfVision}-lssmid-drn=100_ind_avg_hst_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.09_n=100_r=10_LOD_noise=1_th=[0.1]_psteps=100_bs=-1_e-500-turn_fixed_1000-origin_away_1500-turn_fixed_1.json"
                                                                                                                    ], loadSwitchValues=True)
                            modelParams.append(modelParamsDensity)
                            simulationData.append(simulationDataDensity)
                            colours.append(coloursDensity)
                            switchTypeValues.append(switchTypeValuesDensity)

                        #savePath = f"order-ot_comp-K-ordered-d={density}-noise={noisePercentage}-{mode.name}-ot={orderThreshold}-events-t{eventTimestep}p{eventPercentage}a{angle}dt{distributionType.value}a{area}.svg"
                        savePath = f"single_{metric.value}_fov-occ-3e_{degreesOfVision}_drn=2000_threshold-type-comp_eventEffect={eventEffect.val}_ind_avg_{initialState}_st=K_o=5_do=1_s={startValue}_d={density}_r={radius}_LOD_noise=1_th={threshold}_psteps={numberOfPreviousSteps}_dist={distributionType.value}.svg"
                        evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=100, switchTypeValues=switchTypeValues, switchTypeOptions=switchTypeOptions)
                        evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle,savePath=savePath)
                        ServiceGeneral.logWithTime(f"created threshold type comp graph for distributionType={distributionType.name}, density={density}, eventEffect = {eventEffect} and metric {metric.name}")
               