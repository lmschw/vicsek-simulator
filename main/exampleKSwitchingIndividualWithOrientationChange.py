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

eventEffect = EventEffect.ALIGN_TO_FIRST_PARTICLE
domainSize = (100, 100)
density = 0.01
radius = 10
noisePercentage = 0
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 5000
i = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = disorderValue
orderThreshold = 0.05

orderThresholds = [0.1, 0.3, 0.5, 0.7]
percentages = [1, 5, 10, 30, 50]
angles = [45, 90, 180]

"""
for orderThreshold in orderThresholds:
    for percentage in percentages:
        for angle in angles:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
                                                            eventEffect=eventEffect,
                                                            distributionType=DistributionType.GLOBAL
                                                            )

            events = [event1]
            # RANDOM START

            startRun = time.time()
            ServiceGeneral.logWithTime(f"Start global random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=startValue, 
                                                                            noise=noise, 
                                                                            radius=radius,
                                                                            switchType=switchType,
                                                                            switchValues=(orderValue, disorderValue))
            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

            # Save model values for future use
            eventsString = "_".join([event.getShortPrintVersion() for event in events])
            savePath = f"ind_random_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
            # Initalise the animator
            #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            #preparedAnimator.setParams(simulator.getParameterSummary())

            #preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            

for orderThreshold in orderThresholds:
    for percentage in percentages:
        for angle in angles:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
                                                            eventEffect=eventEffect,
                                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                            areas=[[20, 20, 10]]
                                                            )

            events = [event1]
            # RANDOM START

            startRun = time.time()
            ServiceGeneral.logWithTime(f"Start local random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=startValue, 
                                                                            noise=noise, 
                                                                            radius=radius,
                                                                            switchType=switchType,
                                                                            switchValues=(orderValue, disorderValue))
            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

            # Save model values for future use
            eventsString = "_".join([event.getShortPrintVersion() for event in events])
            savePath = f"ind_random_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            # Initalise the animator
            #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            #preparedAnimator.setParams(simulator.getParameterSummary())

            #preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed local random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
"""            

"""
for orderThreshold in orderThresholds:
    for percentage in percentages:
        for angle in angles:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=2000,
                                                            percentage=percentage,
                                                            angle=angle,
                                                            eventEffect=eventEffect,
                                                            distributionType=DistributionType.GLOBA
                                                            )

            events = [event1]
            # RANDOM START

            startRun = time.time()
            ServiceGeneral.logWithTime(f"Start global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=startValue, 
                                                                            noise=noise, 
                                                                            radius=radius,
                                                                            switchType=switchType,
                                                                            switchValues=(orderValue, disorderValue))
            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)

            # Save model values for future use
            eventsString = "_".join([event.getShortPrintVersion() for event in events])
            savePath = f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            

for orderThreshold in orderThresholds:
    for percentage in percentages:
        for angle in angles:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
                                                            eventEffect=eventEffect,
                                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                            areas=[[20, 20, 10]]
                                                            )

            events = [event1]
            # RANDOM START

            startRun = time.time()
            ServiceGeneral.logWithTime(f"Start local ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=startValue, 
                                                                            noise=noise, 
                                                                            radius=radius,
                                                                            switchType=switchType,
                                                                            switchValues=(orderValue, disorderValue))
            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

            # Save model values for future use
            eventsString = "_".join([event.getShortPrintVersion() for event in events])
            savePath = f"ind_ordered_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThreshold}_events-{eventsString}_{i}.json"

            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
            # Initalise the animator
            #animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            #preparedAnimator.setParams(simulator.getParameterSummary())

            #preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed local ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            
"""


percentage = 30
angle = 180

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

tmax = 10000
events = [event1, event2]
# RANDOM START

lowerThreshold = 0.05
upperThreshold = 0.7

noisePercentage = 1
"""
for i in range(1, 4):
    for lowerThreshold in [0.1, 0.2, 0.3, 0.4, 0.5]:
        for upperThreshold in [0.5, 0.6, 0.7, 0.8, 0.9]:
            startRun = time.time()
            ServiceGeneral.logWithTime(f"Start global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
            n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

            #initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=startValue, 
                                                                            noise=noise, 
                                                                            radius=radius,
                                                                            switchType=switchType,
                                                                            switchValues=(orderValue, disorderValue),
                                                                            switchDifferenceThresholdLower=lowerThreshold,
                                                                            switchDifferenceThresholdUpper=upperThreshold)
            #simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

            # Save model values for future use
            eventsString = "_".join([event.getShortPrintVersion() for event in events])
            savePath = f"ind_random_st={switchType.value}_order={orderValue}_disorder={disorderValue}_start={startValue}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_lt={lowerThreshold}_ut={upperThreshold}_events-{eventsString}_{i}"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            #preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            #preparedAnimator.setParams(simulator.getParameterSummary())

            #preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()
            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
"""

upperThreshold = 0.9
lowerThreshold = 0.5
singleThreshold = 0.3

switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
orderValue = NeighbourSelectionMode.FARTHEST
disorderValue = NeighbourSelectionMode.NEAREST
k = 1

startRun = time.time()
ServiceGeneral.logWithTime(f"Start global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle}")
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
startValue = disorderValue

orderThresholds = [lowerThreshold, upperThreshold]

"""
for i in range(1,4):
    for previousSteps in [1, 2, 5, 10, 50, 100, tmax]:
        for singleThreshold in [0.1,0.3,0.5,0.7,0.9]:
            #initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                            neighbourSelectionModel=startValue, 
                                                                            domainSize=domainSize, 
                                                                            numberOfParticles=n, 
                                                                            k=k, 
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
            savePath = f"avg_and_single_ind_random_st={switchType.value}_order={orderValue.value}_disorder={disorderValue.value}_start={startValue.value}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_sth={singleThreshold}_psteps={previousSteps}_events-{eventsString}_{i}"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()
            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
"""

previousSteps = 10

simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(
                                                                neighbourSelectionModel=startValue, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius,
                                                                switchType=switchType,
                                                                switchValues=(orderValue, disorderValue),
                                                                orderThresholds=orderThresholds,
                                                                numberPreviousStepsForThreshold=previousSteps
                                                                )

#simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

# Save model values for future use
eventsString = "_".join([event.getShortPrintVersion() for event in events])
savePath = f"avg_and_single_ind_random_st={switchType.value}_order={orderValue.value}_disorder={disorderValue.value}_start={startValue.value}_d={density}_{neighbourSelectionMode.value}_noise={noisePercentage}_ot={orderThresholds}_psteps={previousSteps}_events-{eventsString}_{i}"
ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

preparedAnimator.saveAnimation(f"{savePath}.mp4")

# Display Animation
#preparedAnimator.showAnimation()
endRun = time.time()
ServiceGeneral.logWithTime(f"Completed global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
