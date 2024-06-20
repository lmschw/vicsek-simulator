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
            return NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST

radius = 10
speed = 1

angle = np.pi
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]


#domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.09, 100)
domainSize = (100, 100)

areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
distTypeString = "lssmid"
distributionType = DistributionType.LOCAL_SINGLE_SITE
percentage = 100
movementPattern = MovementPattern.STATIC
e1Start = 5000
e2Start = 10000
e3Start = 15000

noisePercentages = [0, 0.5, 1, 1.5, 2]
densities = [0.01, 0.05, 0.09]
numbersOfPreviousSteps = [1, 100]
durations = [1, 100, 1000]
ks = [1,3,5]

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

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]


iStart = 0
iStop = 11

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    for numberOfPreviousSteps in numbersOfPreviousSteps:
        # NO EVENT - GLOBAL - NEIGHBOUR SELECTION MODE
        tmax = 5000
        switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
        orderValue, disorderValue = getOrderDisorderValue(switchType)
        k = 1

        for i in range(iStart,iStop):
            for noisePercentage in noisePercentages:
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                for neighbourSelectionMode in neighbourSelectionModes:
                    for initialStateString in ["ordered", "random"]:
                        startValue = neighbourSelectionMode
                        startRun = time.time()

                        if initialStateString == "ordered":
                            initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=startValue, 
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
                        savePath = f"global_noev_{initialStateString}_switchType={switchType.value}_st={startValue.value}_d={density}_n={n}_noise={noisePercentage}_{i}"
                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed 'NO EVENT - GLOBAL - NEIGHBOUR SELECTION MODE' - i = {i}, noise = {noisePercentage}%, nsm={neighbourSelectionMode.name}, init = {initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

        # SWITCHING - GLOBAL - NEIGHBOUR SELECTION MODE
        tmax = 20000
        switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
        orderValue, disorderValue = getOrderDisorderValue(switchType)
        k = 1

        for i in range(iStart,iStop):
            for noisePercentage in noisePercentages:
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                for orderValue in orderNeighbourSelectionModes:
                    for disorderValue in disorderNeighbourSelectionModes:
                        switches = [[5000, orderValue],
                                    [10000, disorderValue], 
                                    [15000, orderValue]]
                        for initialStateString in ["random"]:
                            if initialStateString == "ordered":
                                startValue = orderValue
                            else:
                                startValue = disorderValue

                            startRun = time.time()

                            if initialStateString == "ordered":
                                initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                            simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                            neighbourSelectionModel=startValue, 
                                                                                            domainSize=domainSize, 
                                                                                            numberOfParticles=n, 
                                                                                            k=k, 
                                                                                            noise=noise, 
                                                                                            radius=radius,
                                                                                            speed=speed,
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState, switchType=switchType,  switches=switches)
                            else:
                                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType,  switches=switches)

                            eventsString = "_".join([f"{ev[0]}-{ev[1]}" for ev in switches])
                            # Save model values for future use
                            savePath = f"global_switch_{initialStateString}_switchType={switchType.value}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 'SWITCHING - GLOBAL - NEIGHBOUR SELECTION MODE' - i = {i}, noise = {noisePercentage}%, order={orderValue.name}, disorder={disorderValue.name}, init = {initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

        # NO EVENT - GLOBAL - K
        tmax = 5000
        switchType = SwitchType.K
        orderValue, disorderValue = getOrderDisorderValue(switchType)
        neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

        for i in range(iStart,iStop):
            for noisePercentage in noisePercentages:
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                for k in ks:
                    for initialStateString in ["ordered", "random"]:
                        startValue = k
                        startRun = time.time()

                        if initialStateString == "ordered":
                            initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=neighbourSelectionMode, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=startValue, 
                                                                                        noise=noise, 
                                                                                        radius=radius,
                                                                                        speed=speed,
                                                                                        )
                        if initialStateString == "ordered":
                            simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)
                        else:
                            simulationData, colours = simulator.simulate(tmax=tmax)

                        # Save model values for future use
                        savePath = f"global_noev_{initialStateString}_switchType={switchType.value}_st={startValue}_LOD_d={density}_n={n}_noise={noisePercentage}_{i}"
                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed 'NO EVENT - GLOBAL - K' - i = {i}, noise = {noisePercentage}%, nsm={neighbourSelectionMode.name}, init = {initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

        # SWITCHING - GLOBAL - K
        tmax = 20000
        switchType = SwitchType.K
        orderValue, disorderValue = getOrderDisorderValue(switchType)
        neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

        for i in range(iStart,iStop):
            for noisePercentage in noisePercentages:
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                for neighbourSelectionMode in disorderNeighbourSelectionModes:
                        orderValue = 5
                        disorderValue = 1
                        switches = [[5000, orderValue],
                                    [10000, disorderValue], 
                                    [15000, orderValue]]
                        for initialStateString in ["random"]:
                            if initialStateString == "ordered":
                                startValue = orderValue
                            else:
                                startValue = disorderValue

                            startRun = time.time()

                            if initialStateString == "ordered":
                                initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                            simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                            neighbourSelectionModel=neighbourSelectionMode, 
                                                                                            domainSize=domainSize, 
                                                                                            numberOfParticles=n, 
                                                                                            k=startValue, 
                                                                                            noise=noise, 
                                                                                            radius=radius,
                                                                                            speed=speed,
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState, switchType=switchType,  switches=switches)
                            else:
                                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType,  switches=switches)

                            eventsString = "_".join([f"{ev[0]}-{ev[1]}" for ev in switches])
                            # Save model values for future use
                            savePath = f"global_switch_{initialStateString}_switchType={switchType.value}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 'SWITCHING - GLOBAL - K' - i = {i}, noise = {noisePercentage}%, order={orderValue}, disorder={disorderValue}, init = {initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

        for duration in durations:
            # SINGLE EVENT - LOCAL - NEIGHBOUR SELECTION MODE
            tmax = 15000
            switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
            orderValue, disorderValue = getOrderDisorderValue(switchType)
            k = 1
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)

            for i in range(iStart,iStop):
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        targetSwitchValue=disorderValue
                        startValue = orderValue
                    else:
                        targetSwitchValue=orderValue
                        startValue = disorderValue

                    for eventEffectOrder in eventEffects:
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
                                            limitVisibilityToRadius=True,
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
                                                                                            numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                            switchBlockedAfterEventTimesteps=blockSteps,
                                                                                            speed=speed,
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                            savePath = f"local_1e_{initialStateString}_switchType={switchType.value}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_k={k}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 1e nsm i={i}, eventEffect={eventEffectOrder.name}, duration={duration}, init={initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

            # 3 EVENTS - LOCAL - NEIGHBOUR SELECTION MODE
            tmax = 20000
            switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
            orderValue, disorderValue = getOrderDisorderValue(switchType)
            k = 1
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)

            for i in range(iStart,iStop):
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        targetSwitchValue=disorderValue
                        startValue = orderValue
                    else:
                        targetSwitchValue=orderValue
                        startValue = disorderValue

                    for eventEffectOrder in eventEffectsOrder:
                        for eventEffectDisorder in eventEffectsDisorder:

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
                                            limitVisibilityToRadius=True,
                                            )
                            
                            event2 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=e2Start,
                                            endTimestep=e2Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectDisorder,
                                            movementPattern=movementPattern,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=distributionType,
                                            areas=areas,
                                            limitVisibilityToRadius=True,
                                            )
                            event3 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=e3Start,
                                            endTimestep=e3Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectOrder,
                                            movementPattern=movementPattern,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=distributionType,
                                            areas=areas,
                                            limitVisibilityToRadius=True,
                                            )

                            events = [event1, event2, event3]

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
                                                                                            numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                            switchBlockedAfterEventTimesteps=blockSteps,
                                                                                            speed=speed,
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            #eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}_{event2.timestep}-{event2.eventEffect.val}_{event3.timestep}-{event3.eventEffect.val}"
                            savePath = f"local_3e_{initialStateString}_switchType={switchType.value}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_k={k}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 3e nsm i={i}, eventEffectOrder={eventEffectOrder.name}, eventEffectDisorder={eventEffectDisorder.name}, duration={duration}, init={initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

            # SINGLE EVENT - LOCAL - K
            tmax = 15000
            switchType = SwitchType.K
            orderValue, disorderValue = getOrderDisorderValue(switchType)
            neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)

            for i in range(iStart,iStop):
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        targetSwitchValue=disorderValue
                        startValue = orderValue
                    else:
                        targetSwitchValue=orderValue
                        startValue = disorderValue

                    for eventEffectOrder in eventEffects:

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
                                            limitVisibilityToRadius=True,
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
                                                                                            numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                            switchBlockedAfterEventTimesteps=blockSteps,
                                                                                            speed=speed,
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            #eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                            savePath = f"local_1e_{initialStateString}_switchType={switchType.value}_st={startValue}_o={orderValue}_do={disorderValue}_LOD_d={density}_n={n}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 1e K i={i}, eventEffect={eventEffectOrder.name}, duration={duration}, init={initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")

            # 3 EVENTS - LOCAL - K
            tmax = 20000
            switchType = SwitchType.K
            orderValue, disorderValue = getOrderDisorderValue(switchType)
            neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)

            for i in range(iStart,iStop):
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        targetSwitchValue=disorderValue
                        startValue = orderValue
                    else:
                        targetSwitchValue=orderValue
                        startValue = disorderValue

                    for eventEffectOrder in eventEffectsOrder:
                        for eventEffectDisorder in eventEffectsDisorder:

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
                                            limitVisibilityToRadius=True,
                                            )
                            
                            event2 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=e2Start,
                                            endTimestep=e2Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectDisorder,
                                            movementPattern=movementPattern,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=distributionType,
                                            areas=areas,
                                            limitVisibilityToRadius=True,
                                            )
                            event3 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=e3Start,
                                            endTimestep=e3Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectOrder,
                                            movementPattern=movementPattern,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=distributionType,
                                            areas=areas,
                                            limitVisibilityToRadius=True,
                                            )

                            events = [event1, event2, event3]

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
                                                                                            numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                            switchBlockedAfterEventTimesteps=blockSteps,
                                                                                            speed=speed
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            #eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}_{event2.timestep}-{event2.eventEffect.val}_{event3.timestep}-{event3.eventEffect.val}"
                            savePath = f"local_3e_{initialStateString}_switchType={switchType.value}_st={startValue}_o={orderValue}_do={disorderValue}_LOD_d={density}_n={n}_k={k}_noise={noisePercentage}_{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed 3e K i={i}, eventEffectOrder={eventEffectOrder.name}, eventEffectDisorder={eventEffectDisorder.name}, duration={duration}, init={initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")
