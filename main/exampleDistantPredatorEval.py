import time
import numpy as np

import VicsekWithNeighbourSelectionSwitchingCellBased
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration
import EvaluatorMultiAvgComp

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern
from EnumMetrics import Metrics

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates a complete set of data for a single density value
for "Neighbour selection can cause collective response"
--------------------------------------------------------------------------------
"""

def getOrderDisorderValue(switchType):
    match switchType:
        case SwitchType.K:
            return 5, 1
        case SwitchType.NEIGHBOUR_SELECTION_MODE:
            #return NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST
            return NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

speed = 1

angle = np.pi
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]


#domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.09, 100)
domainSize = (50, 50)

distTypeString = "lssmid"
distributionType = DistributionType.LOCAL_SINGLE_SITE
percentage = 100
movementPattern = MovementPattern.STATIC
e1Start = 5000

noisePercentage = 1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

tmaxWithoutEvent = 3000
tmaxWithEvent = 15000

densities = [0.05]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
duration = 1000
ks = [1, 5]
radii = [10] # area is always 4x bigger than the last

neighbourSelectionModes = [NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

orderNeighbourSelectionModes = [NeighbourSelectionMode.ALL,
                                NeighbourSelectionMode.RANDOM,
                                NeighbourSelectionMode.FARTHEST,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

disorderNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                                   NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

localNeighbourSelectionmodes = [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

eventEffects = [
                EventEffect.AWAY_FROM_ORIGIN,
                ]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]

#baseLocation = f"D:/vicsek-data2/adaptive_radius"
saveLocation = ""
iStart = 1
iStop = 11

switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
orderValue = NeighbourSelectionMode.FARTHEST
disorderValue = NeighbourSelectionMode.NEAREST


startTotal = time.time()
saveLocation = "D:/data/visek-data2/predator_outside/"
metric = Metrics.ORDER
labels = ["ordered", "disordered"]
xLabel = "timesteps"
yLabel = "order"
subtitle = None
eventEffect = EventEffect.AWAY_FROM_ORIGIN
iStart = 1
iStop = 11
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    #saveLocation = f"{baseLocation}/global"
    for radius in radii:
# ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
        #saveLocation = f"{baseLocation}/local"
        tmax = tmaxWithEvent
        
        for xPosOffset in range(1, int(4)):
            areas = [(domainSize[0] + xPosOffset, domainSize[1]/2, radius)] # to the right of the domain because Distant has been tested with PI

            # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
            for k in [1]:
                #for neighbourSelectionMode in neighbourSelectionModes:
                    modelParams = []
                    simulationData = []
                    colours = []
                    switchTypeValues = []
                    for initialStateString in ["ordered", "random"]:
                        if initialStateString == "ordered":
                            startValue = orderValue
                        else:
                            startValue = disorderValue
                        eventsString = f"{e1Start}-{eventEffect.val}"
                        #baseFilename = f"{saveLocation}local_1e_nsmsw_{initialStateString}_st={startValue.value}_o=F_do=N_xPosOffset={xPosOffset}_d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-origin_away"
                        baseFilename = f"{saveLocation}local_1e_nosw_{initialStateString}_st={startValue.value}_xPosOffset={xPosOffset}_d={density}_n={n}_r={radius}_k={k}_noise=1_drn=1000_5000-origin_away"
                        filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
                        modelParamsDensity, simulationDataDensity, coloursDensity, switchTypeValuesDensity = ServiceSavedModel.loadModels(filenames, loadSwitchValues=True)
                        modelParams.append(modelParamsDensity)
                        simulationData.append(simulationDataDensity)
                        colours.append(coloursDensity)
                        switchTypeValues.append(switchTypeValuesDensity)

                    #savePath = f"test_order_pred_dist_xPosOffset={xPosOffset}_d={density}_r={radius}_k={k}.svg"
                    savePath = f"test_order_pred_dist_nosw_xPosOffset={xPosOffset}_d={density}_r={radius}_k={k}.svg"
                    evaluator = EvaluatorMultiAvgComp.EvaluatorMultiAvgComp(modelParams, metric, simulationData, evaluationTimestepInterval=1)
                    evaluator.evaluateAndVisualize(labels=labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, savePath=savePath)
                    ServiceGeneral.logWithTime(f"created threshold type comp graph for distributionType={distributionType.name}, density={density}, eventEffect = {eventEffect} and metric {metric.name}")
