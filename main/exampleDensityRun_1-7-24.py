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

densities = [0.01, 0.05, 0.09]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
ks = [1, 5]
radii = [5, 10, 20] # area is always 4x bigger than the last

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

baseLocation = f"D:/vicsek-data2/adaptive_radius"
#saveLocation = ""
iStart = 1
iStop = 11

startTotal = time.time()
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    saveLocation = f"{baseLocation}/global"
    for radius in radii:
        print(f"d={density}, n={n}, r={radius}, size={domainSize}")

        
        """
        # ---neighbourSelectionMode only (3000) for all 6 modes
        tmax = tmaxWithoutEvent

        for initialStateString in ["ordered", "random"]:
            for neighbourSelectionMode in neighbourSelectionModes:
                for k in ks:
                    for i in range(iStart,iStop): 
                        ServiceGeneral.logWithTime(f"Starting d={density}, r={radius}, {initialStateString}, nsm={neighbourSelectionMode.name}, k={k} i={i}")
                        startRun = time.time()

                        if initialStateString == "ordered":
                            initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=neighbourSelectionMode, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius,
                                                                                        speed=speed,
                                                                                        )
                        if initialStateString == "ordered":
                            simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)
                        else:
                            simulationData, colours = simulator.simulate(tmax=tmax)

                        # Save model values for future use
                        savePath = f"{saveLocation}/global_noev_nosw_d={density}_r={radius}_{initialStateString}_nsm={neighbourSelectionMode.value}_k={k}_n={n}_noise={noisePercentage}_psteps={psteps}_{i}"
                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, {initialStateString}, nsm={neighbourSelectionMode.name}, k={k} i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
            endTotal = time.time()
            ServiceGeneral.logWithTime(f"Completed GLOBAL in {ServiceGeneral.formatTime(endTotal-startTotal)}")
        """
# ----------------------------------------------- LOCAL STARTS HERE ----------------------------------------------
        saveLocation = f"{baseLocation}/local"
        areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
        tmax = tmaxWithEvent
        """
        for duration in durations:
            # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
            for k in ks:
                for neighbourSelectionMode in neighbourSelectionModes:
                    for initialStateString in ["ordered", "random"]:
                        startValue = neighbourSelectionMode
                        for eventEffectOrder in eventEffects:
                            for i in range(iStart,iStop):
                                ServiceGeneral.logWithTime(f"Started d={density}, r={radius}, drn={duration}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
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
                                savePath = f"{saveLocation}local_1e_sw_{initialStateString}_st={startValue.value}__d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"
                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                endRun = time.time()
                                ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, drn={duration}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
        """
        saveLocation = f"{saveLocation}/switchingActive"

        for orderValue in [NeighbourSelectionMode.ALL, NeighbourSelectionMode.RANDOM, NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
            for disorderValue in disorderNeighbourSelectionModes: 
                startNsm = time.time()
                for duration in durations:
                    switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
                    orderValue, disorderValue = getOrderDisorderValue(switchType)      
                    for k in ks:
                        for initialStateString in ["ordered", "random"]:
                            if initialStateString == "ordered":
                                startValue = orderValue
                            else:
                                startValue = disorderValue

                            for eventEffectOrder in eventEffects:
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
                                    savePath = f"{saveLocation}/local_1e_switchType={switchType.value}_{initialStateString}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_r={radius}_k={k}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"
                                    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                    endRun = time.time()
                                    ServiceGeneral.logWithTime(f"Completed nsm-switch d={density}, r={radius}, drn={duration}, k={k}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
        endNsm = time.time()
        ServiceGeneral.logWithTime(f"Completed nsm-switch in {ServiceGeneral.formatTime(endNsm-startNsm)}")
        """
        startK = time.time()
        for duration in durations:
            switchType = SwitchType.K
            orderValue, disorderValue = getOrderDisorderValue(switchType)      
            for neighbourSelectionMode in neighbourSelectionModes:
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        startValue = orderValue
                    else:
                        startValue = disorderValue

                    for eventEffectOrder in eventEffects:
                        for i in range(iStart,iStop):
                            ServiceGeneral.logWithTime(f"Started k-switch d={density}, r={radius}, drn={duration}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i}")
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
                            savePath = f"{saveLocation}/local_1e_switchType={switchType.value}_{initialStateString}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_noise={noisePercentage}_drn={duration}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed k-switch d={density}, r={radius}, drn={duration}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")

                            endK = time.time()
ServiceGeneral.logWithTime(f"Completed k-switch in {ServiceGeneral.formatTime(endK-startK)}")
"""
endK = time.time()
ServiceGeneral.logWithTime(f"Completed nsm-switch in {ServiceGeneral.formatTime(endNsm-startNsm)}")
ServiceGeneral.logWithTime(f"Completed nsm-switch + k-switch in {ServiceGeneral.formatTime(endK-startNsm)}")
