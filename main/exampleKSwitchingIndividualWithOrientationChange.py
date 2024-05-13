import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEvent import ExternalStimulusOrientationChangeEvent
import AnimatorMatplotlib
import Animator2D

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType


domainSize = (100, 100)
density = 0.01
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

thresholdType = ThresholdType.TWO_THRESHOLDS
thresholds = [0.1]

numberOfPreviousSteps = 100
tmax = 15000
i = 1

for initialStateString in ["ordered", "random"]:
    if initialStateString == "ordered":
        targetSwitchValue=disorderValue
        startValue = orderValue
    else:
        targetSwitchValue=orderValue
        startValue = disorderValue

    for percentage in [10, 30, 50, 70, 100]:
        for eventEffect in [EventEffect.TURN_BY_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIXED_ANGLE,
                            EventEffect.ALIGN_TO_FIRST_PARTICLE,
                            EventEffect.AWAY_FROM_ORIGIN,
                            EventEffect.TOWARDS_ORIGIN]:
            
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
                                                                                numberPreviousStepsForThreshold=numberOfPreviousSteps
                                                                                )
                if initialStateString == "ordered":
                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                else:
                    simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                # Save model values for future use
                eventsString = "_".join([event.getShortPrintVersion() for event in events])
                savePath = f"ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={thresholds}_psteps={numberOfPreviousSteps}_e-{eventsString}_{i}"
                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed percentage={percentage}, eventEffect={eventEffect.name} in {ServiceGeneral.formatTime(endRun-startRun)}")
