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

angle = np.pi
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]


#domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.09, 100)
domainSize = (50, 50)

distTypeString = "lssmid"
distributionType = DistributionType.LOCAL_SINGLE_SITE
percentage = 100
movementPattern = MovementPattern.RANDOM
e1Start = 5000

tmaxWithoutEvent = 15000
tmaxWithEvent = 15000

densities = [0.09]
durations = [1000]
ks = [1]
radii = [10] # area is always 4x bigger than the last
noisePercentage = 1
psteps = 100
numbersOfPreviousSteps = [psteps]
speed = 1

neighbourSelectionModes = [NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

reducedNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
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
                EventEffect.AWAY_FROM_ORIGIN]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]

#baseLocation = f"D:/vicsek-data2/adaptive_radius"
saveLocation = "J:/randomly_moving_predator/"
iStart = 1
iStop = 11

startTotal = time.time()
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    #saveLocation = f"{baseLocation}/global"
    for radius in radii:
        for predator_speed in [0.1, 1]:
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            print(f"d={density}, n={n}, r={radius}, size={domainSize}, psteps: {psteps}")
    # ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
            #saveLocation = f"{baseLocation}/local"
            areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
            tmax = tmaxWithEvent
            
            
            for duration in durations:
                # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)    
                
                for k in ks:
                    for neighbourSelectionMode in neighbourSelectionModes:
                        for initialStateString in ["ordered", "random"]:
                            startValue = neighbourSelectionMode
                            for eventEffectOrder in eventEffects:
                                for i in range(iStart,iStop):
                                    ServiceGeneral.logWithTime(f"Started psteps={psteps}, d={density}, r={radius}, drn={duration}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
                                    event1 = ExternalStimulusOrientationChangeEventDuration(
                                                    startTimestep=e1Start,
                                                    endTimestep=e1Start + duration,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=eventEffectOrder,
                                                    movementPattern=movementPattern,
                                                    movementSpeed=predator_speed,
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
                                    savePath = f"{saveLocation}local_1e_nosw_{initialStateString}_st={startValue.value}__d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_speed={speed}_drn={duration}_psteps={psteps}_{eventsString}_predspeed={predator_speed}_{i}"
                                    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                    endRun = time.time()
                                    ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, drn={duration}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")        
                    

                for nsmCombo in [[NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.FARTHEST],
                                [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]:
                        disorderValue, orderValue = nsmCombo
                        startNsm = time.time()
                        for duration in durations:
                            switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
                            for k in ks:
                                for initialStateString in ["ordered", "random"]:
                                    if initialStateString == "ordered":
                                        startValue = orderValue
                                    else:
                                        startValue = disorderValue

                                    for eventEffectOrder in eventEffects:
                                        for i in range(iStart,iStop):
                                            ServiceGeneral.logWithTime(f"Started nsm switch psteps={psteps}, d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
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
                                            savePath = f"{saveLocation}local_nsmsw_1ev_{initialStateString}_st={startValue.value}_d={density}_n={n}_r={radius}_nsmCombo={nsmCombo[0].value}-{nsmCombo[1].value}_k={k}_noise={noisePercentage}_speed={speed}_psteps={psteps}_ee={eventEffectOrder.val}_predspeed={predator_speed}_{i}.json"
                                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                            endRun = time.time()
                                            ServiceGeneral.logWithTime(f"Completed nsm-switch d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, {orderValue.value}-{disorderValue.value}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
            endNsm = time.time()
            ServiceGeneral.logWithTime(f"Completed nsm-switch in {ServiceGeneral.formatTime(endNsm-startNsm)}")

            startK = time.time()
            for duration in durations:
                switchType = SwitchType.K
                kCombo = (1,5)    
                disorderValue, orderValue = kCombo 
                for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]:
                    for initialStateString in ["ordered", "random"]:
                        if initialStateString == "ordered":
                            startValue = orderValue
                        else:
                            startValue = disorderValue

                        for eventEffectOrder in eventEffects:
                            for i in range(iStart,iStop):
                                ServiceGeneral.logWithTime(f"Started k-switch psteps={psteps}, d={density}, r={radius}, drn={duration}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
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
                                                                                                neighbourSelectionModel=neighbourSelectionMode, 
                                                                                                domainSize=domainSize, 
                                                                                                numberOfParticles=n, 
                                                                                                k=startValue, 
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
                                savePath = f"{saveLocation}local_ksw_1ev_{initialStateString}_st={startValue}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_kCombo={kCombo[0]}-{kCombo[1]}_ee={eventEffectOrder.val}_noise={noisePercentage}_speed={speed}_psteps={psteps}_predspeed={predator_speed}_{i}.json"
                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                endRun = time.time()
                                ServiceGeneral.logWithTime(f"Completed k-switch d={density}, r={radius}, drn={duration}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")

                                endK = time.time()
    ServiceGeneral.logWithTime(f"Completed k-switch in {ServiceGeneral.formatTime(endK-startK)}")


endTotal = time.time()
ServiceGeneral.logWithTime(f"Completed total in {ServiceGeneral.formatTime(endTotal-startTotal)}")
