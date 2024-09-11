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

"""
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    #saveLocation = f"{baseLocation}/global"
    for radius in radii:
# ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
        #saveLocation = f"{baseLocation}/local"
        tmax = tmaxWithEvent
        
        for k in [1]:
                for xPosOffset in range(4, int(radius)):
                    areas = [(domainSize[0] + xPosOffset, domainSize[1]/2, radius)] # to the right of the domain because Distant has been tested with PI

            # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
            
                #for neighbourSelectionMode in neighbourSelectionModes:
                    for initialStateString in ["ordered", "random"]:
                        if initialStateString == "ordered":
                            startValue = orderValue
                        else:
                            startValue = disorderValue
                        #startValue = neighbourSelectionMode
                        for eventEffectOrder in eventEffects:
                            for i in range(iStart,iStop):
                                ServiceGeneral.logWithTime(f"Started d={density}, r={radius}, drn={duration}, k={k},  {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
                                event1 = ExternalStimulusOrientationChangeEventDuration(
                                                startTimestep=e1Start,
                                                endTimestep=e1Start + duration,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffectOrder,
                                                movementPattern=movementPattern,
                                                movementSpeed=1,
                                                perceptionRadius=radius,
                                                distributionType=distributionType,
                                                areas=areas,
                                                )
                                
                                events = [event1]

                                startRun = time.time()

                                if initialStateString == "ordered":
                                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                                
                                simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection(
                                                                                                neighbourSelectionModel=startValue, 
                                                                                                domainSize=domainSize, 
                                                                                                numberOfParticles=n, 
                                                                                                k=k, 
                                                                                                noise=noise, 
                                                                                                radius=radius,
                                                                                                thresholdType=thresholdType,
                                                                                                orderThresholds=threshold,
                                                                                                numberPreviousStepsForThreshold=psteps,
                                                                                                switchBlockedAfterEventTimesteps=blockSteps,
                                                                                                speed=speed,
                                                                                                switchingActive=False,
                                                                                                )
                                     
                                

                                if initialStateString == "ordered":
                                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                                else:
                                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                                # Save model values for future use
                                eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                                savePath = f"{saveLocation}local_1e_nosw_{initialStateString}_st={startValue.value}_xPosOffset={xPosOffset}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"

                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                endRun = time.time()
                                ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")

"""

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    #saveLocation = f"{baseLocation}/global"
    for radius in radii:
# ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
        #saveLocation = f"{baseLocation}/local"
        tmax = tmaxWithEvent
        for k in [1]:
            for xPosOffset in range(4, int(radius)):
                areas = [(domainSize[0] + xPosOffset, domainSize[1]/2, radius)] # to the right of the domain because Distant has been tested with PI

            # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
            
                #for neighbourSelectionMode in neighbourSelectionModes:
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        startValue = orderValue
                    else:
                        startValue = disorderValue
                    #startValue = neighbourSelectionMode
                    for eventEffectOrder in eventEffects:
                        for i in range(iStart,iStop):
                            ServiceGeneral.logWithTime(f"Started d={density}, r={radius}, drn={duration}, k={k},  {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
                            event1 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=e1Start,
                                            endTimestep=e1Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectOrder,
                                            movementPattern=movementPattern,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=distributionType,
                                            areas=areas,
                                            )
                            
                            events = [event1]

                            startRun = time.time()

                            if initialStateString == "ordered":
                                initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                            
                            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection(
                                                            neighbourSelectionModel=startValue, 
                                                            domainSize=domainSize, 
                                                            numberOfParticles=n, 
                                                            k=k, 
                                                            noise=noise, 
                                                            radius=radius,
                                                            switchType=switchType,
                                                            switchValues=(orderValue, disorderValue),
                                                            thresholdType=thresholdType,
                                                            orderThresholds=threshold,
                                                            numberPreviousStepsForThreshold=psteps,
                                                            switchBlockedAfterEventTimesteps=blockSteps,
                                                            speed=speed,
                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                            savePath = f"{saveLocation}local_1e_nsmsw_{initialStateString}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_xPosOffset={xPosOffset}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"

                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")



