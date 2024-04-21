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
startValue = orderValue
orderThreshold = 0.05


for orderThreshold in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
    for percentage in [1, 5, 10, 30, 50]:
        for angle in [45, 90, 180, 270]:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
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
            savePath = f"individual_random_switch={switchType.name}_orderV={orderValue}_disorderV={disorderValue}_startV={startValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_events-{eventsString}_{i}"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
            """
            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()
            """

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            

for orderThreshold in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
    for percentage in [1, 5, 10, 30, 50]:
        for angle in [45, 90, 180, 270]:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
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
            savePath = f"individual_random_switch={switchType.name}_orderV={orderValue}_disorderV={disorderValue}_startV={startValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            """
            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()
            """

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed local random start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            

for orderThreshold in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
    for percentage in [1, 5, 10, 30, 50]:
        for angle in [45, 90, 180, 270]:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
                                                            distributionType=DistributionType.GLOBAL
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
            savePath = f"individual_ordered_switch={switchType.name}_orderV={orderValue}_disorderV={disorderValue}_startV={startValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

            """
            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            #preparedAnimator.showAnimation()
            """

            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed global ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            

for orderThreshold in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
    for percentage in [1, 5, 10, 30, 50]:
        for angle in [45, 90, 180, 270]:
            event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                            percentage=percentage,
                                                            angle=angle,
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
            savePath = f"individual_ordered_switch={switchType.name}_orderV={orderValue}_disorderV={disorderValue}_startV={startValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_events-{eventsString}_{i}.json"
            ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())
            """
            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())

            preparedAnimator.saveAnimation(f"{savePath}.mp4")

            # Display Animation
            """

            #preparedAnimator.showAnimation()
            endRun = time.time()
            ServiceGeneral.logWithTime(f"Completed local ordered start i={i}, threshold={orderThreshold}, startValue={startValue}, percentage={percentage}, angle={angle} in {ServiceGeneral.formatTime(endRun-startRun)}")
            
