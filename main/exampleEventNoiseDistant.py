import time
import numpy as np

import VicsekWithNeighbourSelectionSwitchingCellBased
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates a complete set of data for a single density value
for "Neighbour selection can cause collective response"
--------------------------------------------------------------------------------
"""
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

tmaxWithEvent = 15000

densities = [0.05]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
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

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]

iStart = 1
iStop = 11

startTotal = time.time()


for eventNoisePercentage in [100]:
    for density in densities:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
        for radius in radii:
    # ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
            areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
            tmax = tmaxWithEvent

            for nsmCombo in [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
                             [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]: 
                    startNsm = time.time()
                    orderValue, disorderValue = nsmCombo
                    for duration in durations:
                        switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
                        for k in [1]:
                            for initialStateString in ["ordered", "random"]:
                                
                                if initialStateString == "ordered":
                                    startValue = orderValue
                                else:
                                    startValue = disorderValue
                                
                                for eventEffectOrder in [EventEffect.ALIGN_TO_FIXED_ANGLE_NOISE]:
                                    for i in range(iStart,iStop):
                                        ServiceGeneral.logWithTime(f"Started nsm switch d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
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
                                                        noisePercentage=eventNoisePercentage
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
                                                                                                        orderThresholds=[0.1],
                                                                                                        thresholdType=ThresholdType.HYSTERESIS,
                                                                                                        switchType=SwitchType.NEIGHBOUR_SELECTION_MODE,
                                                                                                        switchValues=nsmCombo
                                                                                                        )
                                            
                                        
                                        if initialStateString == "ordered":
                                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                                        else:
                                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                                        # Save model values for future use
                                        eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                                        savePath = f"nsmsw_event_noise={eventNoisePercentage}_{initialStateString}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"
                                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                        endRun = time.time()
                                        ServiceGeneral.logWithTime(f"Completed nsm-switch d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
            endNsm = time.time()
            ServiceGeneral.logWithTime(f"Completed nsm-switch in {ServiceGeneral.formatTime(endNsm-startNsm)}")
