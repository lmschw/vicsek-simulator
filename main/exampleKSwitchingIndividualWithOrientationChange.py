import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEvent import ExternalStimulusOrientationChangeEvent
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration
import AnimatorMatplotlib
import Animator2D

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern


domainSize = (100, 100)
density = 0.05
radius = 10
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

percentage = 30
angle = 180

areas = [(20, 20, 10)]
tmax = 10000
noisePercentage = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
#orderValue = NeighbourSelectionMode.FARTHEST
#disorderValue = NeighbourSelectionMode.NEAREST

n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

"""
startTotal = time.time()
for eventEffect in [EventEffect.AWAY_FROM_ORIGIN,
                    EventEffect.TOWARDS_ORIGIN]:

    event1 = ExternalStimulusOrientationChangeEvent(timestep=2000,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=eventEffect,
                                                    distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                    areas=areas
                                                    )

    event2 = ExternalStimulusOrientationChangeEvent(timestep=6000,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=eventEffect,
                                                    distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                    areas=areas
                                                    )

    events = [event1, event2]

    startRun = time.time()
    startValue = orderValue

    for i in range(1,4):
        for previousSteps in [10, 50, tmax]:
            for singleThreshold in [0.5,0.7]:
                ServiceGeneral.logWithTime(f"Start local random start effect={eventEffect.name}, i={i}, previousSteps={previousSteps}, singleThreshold={singleThreshold}")

                initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                                neighbourSelectionModel=neighbourSelectionMode, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=startValue, 
                                                                                noise=noise, 
                                                                                radius=radius,
                                                                                switchType=switchType,
                                                                                switchValues=(orderValue, disorderValue),
                                                                                orderThresholds=[singleThreshold],
                                                                                numberPreviousStepsForThreshold=previousSteps
                                                                                )

                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                #simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                # Save model values for future use
                eventsString = "_".join([event.getShortPrintVersion() for event in events])
                savePath = f"avg_and_single_ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_sth={singleThreshold}_psteps={previousSteps}_events-{eventsString}_{i}"
                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                #if i == 1:
                    # Initalise the animator
                    #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                    # prepare the animator
                    #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                    #preparedAnimator.setParams(simulator.getParameterSummary())

                    #preparedAnimator.saveAnimation(f"{savePath}.mp4")

                    # Display Animation
                    #preparedAnimator.showAnimation()
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed local random effect={eventEffect.name}, start i={i}, previousSteps={previousSteps}, threshold={singleThreshold} in {ServiceGeneral.formatTime(endRun-startRun)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Completed local random start in {ServiceGeneral.formatTime(endTotal-startTotal)}")
"""
"""
initialStateString = "ordered"
targetSwitchValue=disorderValue
startValue = orderValue


for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                    EventEffect.ALIGN_TO_FIXED_ANGLE]:
        event1 = ExternalStimulusOrientationChangeEvent(timestep=2000,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffect,
                                        distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                        areas=areas,
                                        targetSwitchValue=targetSwitchValue
                                        )

        event2 = ExternalStimulusOrientationChangeEvent(timestep=6000,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffect,
                                        distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                        areas=areas,
                                        targetSwitchValue=targetSwitchValue
                                        )

        events = [event1]

        startRun = time.time()
        for i in range(1,4):
            for numberOfBlockedSteps in [10, 100, 500, 1000]:
                for previousSteps in [10, 50, tmax]:
                    for singleThreshold in [0.5,0.7]:
                        ServiceGeneral.logWithTime(f"Started eventEffect={eventEffect.name}, i={i}, blocked={numberOfBlockedSteps}, steps={previousSteps}, threshold={singleThreshold}")
                        initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=neighbourSelectionMode, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=startValue, 
                                                                                        noise=noise, 
                                                                                        radius=radius,
                                                                                        switchType=switchType,
                                                                                        switchValues=(orderValue, disorderValue),
                                                                                        orderThresholds=[singleThreshold],
                                                                                        numberPreviousStepsForThreshold=previousSteps,
                                                                                        switchBlockedAfterEventTimesteps=numberOfBlockedSteps
                                                                                        )

                        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                        #simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                        # Save model values for future use
                        eventsString = "_".join([event.getShortPrintVersion() for event in events])
                        savePath = f"avg_and_single_ind_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_st={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_sth={singleThreshold}_psteps={previousSteps}_bl={numberOfBlockedSteps}_tsv={targetSwitchValue}_e-{eventsString}_{i}"
                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
                        ServiceGeneral.logWithTime(f"Completed eventEffect={eventEffect.name}, i={i}, blocked={numberOfBlockedSteps}, steps={previousSteps}, threshold={singleThreshold}")
"""

"""
domainSize = (100, 100)
density = 0.01
radius = 10
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE


percentage = 30
angle = 180
tmax = 10000

noisePercentage = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
#orderValue = NeighbourSelectionMode.FARTHEST
#disorderValue = NeighbourSelectionMode.NEAREST

startRun = time.time()
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

areas = None
startValue = orderValue
# todo local random
for eventEffect in [
                    EventEffect.AWAY_FROM_ORIGIN]:

    event1 = ExternalStimulusOrientationChangeEvent(timestep=2000,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=eventEffect,
                                                    distributionType=DistributionType.GLOBAL
                                                    )

    event2 = ExternalStimulusOrientationChangeEvent(timestep=6000,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=eventEffect,
                                                    distributionType=DistributionType.GLOBAL
                                                    )

    events = [event1, event2]

    for i in range(1,4):
        for previousSteps in [1, 2, 5, 10, 50, 100, tmax]:
            for lowerThreshold in [0.1, 0.3, 0.5]:
                for upperThreshold in [0.5, 0.7, 0.9]:

                    orderThresholds = [lowerThreshold, upperThreshold]
                    ServiceGeneral.logWithTime(f"Start local ordered start i={i}, previousSteps={previousSteps}, thresholds={orderThresholds}")

                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                    simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                                    neighbourSelectionModel=neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=startValue, 
                                                                                    noise=noise, 
                                                                                    radius=radius,
                                                                                    switchType=switchType,
                                                                                    switchValues=(orderValue, disorderValue),
                                                                                    orderThresholds=orderThresholds,
                                                                                    numberPreviousStepsForThreshold=previousSteps
                                                                                    )

                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                    #simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                    # Save model values for future use
                    eventsString = "_".join([event.getShortPrintVersion() for event in events])
                    savePath = f"avg_and_double_ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThresholds}_psteps={previousSteps}_events-{eventsString}_{i}"
                    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                    #if i == 1:
                        # Initalise the animator
                        #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                        # prepare the animator
                        #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                        #preparedAnimator.setParams(simulator.getParameterSummary())

                        #preparedAnimator.saveAnimation(f"{savePath}.mp4")

                    # Display Animation
                    #preparedAnimator.showAnimation()
                    endRun = time.time()
                    ServiceGeneral.logWithTime(f"Completed local ordered start i={i}, previousSteps={previousSteps}, thresholds={orderThresholds} in {ServiceGeneral.formatTime(endRun-startRun)}")

"""

"""
domainSize = (100, 100)
density = 0.01
radius = 10
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

percentage = 100
angle = 180

areas = [(50, 50, 1000)]
tmax = 100
noisePercentage = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
#orderValue = NeighbourSelectionMode.FARTHEST
#disorderValue = NeighbourSelectionMode.NEAREST

n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

eventEffect = EventEffect.TOWARDS_ORIGIN
event1 = ExternalStimulusOrientationChangeEvent(timestep=10,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                areas = areas
                                                )
event2 = ExternalStimulusOrientationChangeEvent(timestep=30,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                areas = areas
                                                )
event3 = ExternalStimulusOrientationChangeEvent(timestep=50,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                areas = areas
                                                )
event4 = ExternalStimulusOrientationChangeEvent(timestep=70,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                areas = areas
                                                )
event5 = ExternalStimulusOrientationChangeEvent(timestep=90,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                areas = areas
                                                )

events = [event1, event2, event3, event4, event5]
#events = [event1]

startValue = disorderValue

startTotal = time.time()
singleThreshold = 0.7
previousSteps = 5
i = 1
noise = 0
simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                neighbourSelectionModel=neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=startValue, 
                                                                noise=noise, 
                                                                radius=radius,
                                                                switchType=switchType,
                                                                switchValues=(orderValue, disorderValue),
                                                                orderThresholds=[singleThreshold],
                                                                numberPreviousStepsForThreshold=previousSteps
                                                                )

#simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

# Save model values for future use
eventsString = "_".join([event.getShortPrintVersion() for event in events])
#savePath = f"avg_and_single_ind_random_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_sth={singleThreshold}_psteps={previousSteps}_events-{eventsString}_{i}"
savePath = "test"
ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

preparedAnimator.saveAnimation(f"{savePath}.mp4")
preparedAnimator.showAnimation()
"""

"""
thresholdType = ThresholdType.TWO_THRESHOLDS
thresholds = [0.1]

tmax = 15000
i = 1

blockSteps = -1

initialStateString = "random"
for numberOfPreviousSteps in [150, 200, 500, 1000]:
    if initialStateString == "ordered":
        targetSwitchValue=disorderValue
        startValue = orderValue
    else:
        targetSwitchValue=orderValue
        startValue = disorderValue

    for percentage in [50]:
        for eventEffect in [
                            EventEffect.TURN_BY_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIRST_PARTICLE,
                            EventEffect.AWAY_FROM_ORIGIN,
                            EventEffect.TOWARDS_ORIGIN,
                            EventEffect.RANDOM,
                            ]:
            for i in range(1, 11):
                event1 = ExternalStimulusOrientationChangeEvent(timestep=5000,
                                                percentage=percentage,
                                                angle=angle,
                                                eventEffect=eventEffect,
                                                distributionType=DistributionType.GLOBAL
                                                )

                events = [event1]

                startRun = time.time()

                ServiceGeneral.logWithTime(f"Started percentage={percentage}, eventEffect={eventEffect.name}")
                if initialStateString == "ordered":
                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                                neighbourSelectionModel=neighbourSelectionMode, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=startValue, 
                                                                                noise=noise, 
                                                                                radius=radius,
                                                                                switchType=switchType,
                                                                                switchValues=(orderValue, disorderValue),
                                                                                thresholdType=thresholdType,
                                                                                orderThresholds=thresholds,
                                                                                numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                switchBlockedAfterEventTimesteps=blockSteps
                                                                                )
                if initialStateString == "ordered":
                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                else:
                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                # Save model values for future use
                eventsString = "_".join([event.getShortPrintVersion() for event in events])
                savePath = f"ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={thresholds}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"
                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, previousSteps={numberOfPreviousSteps}, eventEffect={eventEffect.name} in {ServiceGeneral.formatTime(endRun-startRun)}")
"""
"""
thresholdType = ThresholdType.TWO_THRESHOLDS

tmax = 15000
i = 1

eventEffect = EventEffect.TOWARDS_ORIGIN

blockSteps = -1
numberOfPreviousSteps = 100
percentage = 50
initialStateString = "ordered"
radius = 10
for i in range(2,3):
    for thresholdType in [ThresholdType.TWO_THRESHOLDS_SIMPLE_REVERSE]:
        for initialStateString in ["ordered", "random"]:
            if initialStateString == "ordered":
                targetSwitchValue=disorderValue
                startValue = orderValue
            else:
                targetSwitchValue=orderValue
                startValue = disorderValue

            for radius in [5, 10, 20, 30, 50, 100]:
                for thresholds in [[0.1], [0.2], [0.3], [0.4], [0.5]]:
                    for density in [0.01, 0.03, 0.05, 0.07, 0.09]:
                        n = 100
                        domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                        #n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))

                        event1 = ExternalStimulusOrientationChangeEvent(timestep=5000,
                                                        percentage=percentage,
                                                        angle=angle,
                                                        eventEffect=eventEffect,
                                                        distributionType=DistributionType.GLOBAL
                                                        )

                        events = []

                        startRun = time.time()

                        if initialStateString == "ordered":
                            initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=neighbourSelectionMode, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=startValue, 
                                                                                        noise=noise, 
                                                                                        radius=radius,
                                                                                        switchType=switchType,
                                                                                        switchValues=(orderValue, disorderValue),
                                                                                        thresholdType=thresholdType,
                                                                                        orderThresholds=thresholds,
                                                                                        numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                                        switchBlockedAfterEventTimesteps=blockSteps
                                                                                        )
                        if initialStateString == "ordered":
                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                        else:
                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                        # Save model values for future use
                        eventsString = "_".join([event.getShortPrintVersion() for event in events])
                        savePath = f"test_domsize-var_ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_n={n}_r={radius}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={thresholds}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"
                        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                        # Initalise the animator
                        animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                        # prepare the animator
                        preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                        preparedAnimator.setParams(simulator.getParameterSummary())
                        preparedAnimator.saveAnimation(f"{savePath}.mp4")
                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed i={i}, thresholdType={thresholdType}, init={initialStateString}, r={radius}, thresholds={thresholds}, density={density} in {ServiceGeneral.formatTime(endRun-startRun)}")

"""

thresholdType = ThresholdType.TWO_THRESHOLDS

tmax = 25000
i = 1

blockSteps = -1
numberOfPreviousSteps = 100
angle = 90
radius = 10
threshold = [0.1]

for duration in [1000, 2000]:
    for i in range(1,6):
        for initialStateString in ["random"]:
            if initialStateString == "ordered":
                targetSwitchValue=disorderValue
                startValue = orderValue
            else:
                targetSwitchValue=orderValue
                startValue = disorderValue
            for thresholdType in [ThresholdType.HYSTERESIS]:

                for eventEffectOrder in [EventEffect.TURN_BY_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIRST_PARTICLE]:

                    for eventEffectDisorder in [EventEffect.AWAY_FROM_ORIGIN,
                                    EventEffect.TOWARDS_ORIGIN,
                                    EventEffect.RANDOM]:
                        distTypeString = "lssmid"
                        areas = [(16.67, 16.67, radius)]

                        distributionType = DistributionType.LOCAL_SINGLE_SITE
                        percentage = 100
                        e1Start = 5000
                        e2Start = 10000
                        e3Start = 15000
                        event1 = ExternalStimulusOrientationChangeEventDuration(
                                        startTimestep=e1Start,
                                        endTimestep=e1Start + duration,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffectOrder,
                                        movementPattern=MovementPattern.STATIC,
                                        movementSpeed=1,
                                        perceptionRadius=radius,
                                        distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                        areas=areas
                                        )
                        event2 = ExternalStimulusOrientationChangeEventDuration(
                                        startTimestep=e2Start,
                                        endTimestep=e2Start + duration,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffectDisorder,
                                        movementPattern=MovementPattern.STATIC,
                                        movementSpeed=1,
                                        perceptionRadius=radius,
                                        distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                        areas=areas
                                        )
                        event3 = ExternalStimulusOrientationChangeEventDuration(
                                        startTimestep=e3Start,
                                        endTimestep=e3Start + duration,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffectOrder,
                                        movementPattern=MovementPattern.STATIC,
                                        movementSpeed=1,
                                        perceptionRadius=radius,
                                        distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                        areas=areas
                                        )

                        events = [event1, event2, event3]

                        for density in [0.09]:
                            n = 100
                            domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                            #n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))

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
                                                                                            switchBlockedAfterEventTimesteps=blockSteps
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            #eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}_{event2.timestep}-{event2.eventEffect.val}_{event3.timestep}-{event3.eventEffect.val}"
                            savePath = f"switch-{distTypeString}-drn={duration}_ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_n={n}_r={radius}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={threshold}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            """
                            # Initalise the animator
                            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                            # prepare the animator
                            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                            preparedAnimator.setParams(simulator.getParameterSummary())
                            preparedAnimator.saveAnimation(f"{savePath}.mp4")
            """
                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed i={i}, thresholdType={thresholdType}, eventEffectOrder={eventEffectOrder.name}, eventEffectDisorder={eventEffectDisorder.name}, distributionType={distTypeString}, density={density}, endTimestep={endTimestep}, init={initialStateString},  in {ServiceGeneral.formatTime(endRun-startRun)}")



"""
for endTimestep in [10000]:
    for i in range(1,11):
        for initialStateString in ["ordered", "random"]:
            if initialStateString == "ordered":
                targetSwitchValue=disorderValue
                startValue = orderValue
            else:
                targetSwitchValue=orderValue
                startValue = disorderValue
            for thresholdType in [ThresholdType.HYSTERESIS]:

                for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIXED_ANGLE,
                                    EventEffect.ALIGN_TO_FIRST_PARTICLE,
                                    EventEffect.AWAY_FROM_ORIGIN,
                                    EventEffect.TOWARDS_ORIGIN,
                                    EventEffect.RANDOM]:
                    for distTypeString in ["lssmid", "lss1"]:
                        if distTypeString == "global":
                            distributionType = DistributionType.GLOBAL
                            percentage = 30
                            event1 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=5000,
                                            endTimestep=endTimestep,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffect,
                                            movementPattern=MovementPattern.STATIC,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=DistributionType.GLOBAL
                                            )
                        else:
                            distributionType = DistributionType.LOCAL_SINGLE_SITE
                            percentage = 100
                            if distTypeString == "lss20":
                                areas = [(20, 20, radius)]
                            elif distTypeString == "lssmid":
                                areas = [(16.67, 16.67, radius)]
                            elif distTypeString == "lss-1":
                                areas = [(-1, -1, radius)]
                            elif distTypeString == "lss1":
                                areas = [(1, 1, radius)]
                            else:
                                raise Exception("typo")
                            event1 = ExternalStimulusOrientationChangeEventDuration(
                                            startTimestep=5000,
                                            endTimestep=endTimestep,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffect,
                                            movementPattern=MovementPattern.STATIC,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                            areas=areas
                                            )

                        events = [event1]

                        for density in [0.09]:
                            n = 100
                            domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                            #n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))

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
                                                                                            switchBlockedAfterEventTimesteps=blockSteps
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            savePath = f"single-event-{distTypeString}-duration={endTimestep-5000}_ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_n={n}_r={radius}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={threshold}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"
                            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                            # Initalise the animator
                            #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                            # prepare the animator
                            #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                            #preparedAnimator.setParams(simulator.getParameterSummary())
                            #preparedAnimator.saveAnimation(f"{savePath}.mp4")
                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed i={i}, thresholdType={thresholdType}, eventEffect={eventEffect.name}, distributionType={distTypeString}, density={density}, endTimestep={endTimestep}, init={initialStateString},  in {ServiceGeneral.formatTime(endRun-startRun)}")

"""