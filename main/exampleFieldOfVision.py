import time
import numpy as np

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDurationFov
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDurationFov import ExternalStimulusOrientationChangeEventDurationFov

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates data for field of vision experiments
--------------------------------------------------------------------------------
"""

domainSize = (100, 100)
density = 0.05
radius = 10
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE

percentage = 30
angle = np.pi

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

thresholdType = ThresholdType.TWO_THRESHOLDS

tmax = 25000
i = 1

blockSteps = -1
numberOfPreviousSteps = 100
angle = 90
radius = 10
threshold = [0.1]
density = 0.09

for duration in [2000]:
    for i in range(1,2):
        for initialStateString in ["random"]:
            if initialStateString == "ordered":
                targetSwitchValue=disorderValue
                startValue = orderValue
            else:
                targetSwitchValue=orderValue
                startValue = disorderValue
            for thresholdType in [ThresholdType.HYSTERESIS]:

                for eventEffectOrder in [EventEffect.TURN_BY_FIXED_ANGLE,
]:

                    for eventEffectDisorder in [EventEffect.AWAY_FROM_ORIGIN,
]:
                        distTypeString = "lssmid"
                        areas = [(16.67, 16.67, radius)]

                        distributionType = DistributionType.LOCAL_SINGLE_SITE
                        percentage = 100
                        e1Start = 5000
                        e2Start = 10000
                        e3Start = 15000
                        for degreesOfVision in [np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3, 2*np.pi]:

                            event1 = ExternalStimulusOrientationChangeEventDurationFov(
                                            startTimestep=e1Start,
                                            endTimestep=e1Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectOrder,
                                            movementPattern=MovementPattern.STATIC,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                            areas=areas,
                                            degreesOfVision=degreesOfVision
                                            )
                            event2 = ExternalStimulusOrientationChangeEventDurationFov(
                                            startTimestep=e2Start,
                                            endTimestep=e2Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectDisorder,
                                            movementPattern=MovementPattern.STATIC,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                            areas=areas,
                                            degreesOfVision=degreesOfVision
                                            )
                            event3 = ExternalStimulusOrientationChangeEventDurationFov(
                                            startTimestep=e3Start,
                                            endTimestep=e3Start + duration,
                                            percentage=percentage,
                                            angle=angle,
                                            eventEffect=eventEffectOrder,
                                            movementPattern=MovementPattern.STATIC,
                                            movementSpeed=1,
                                            perceptionRadius=radius,
                                            distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                            areas=areas,
                                            degreesOfVision=degreesOfVision
                                            )

                            events = [event1, event2, event3]
                            #events = []

                            n = 100
                            domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                            #n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                            n = 500

                            startRun = time.time()

                            if initialStateString == "ordered":
                                initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

                            simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDurationFov.VicsekWithNeighbourSelection(
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
                                                                                            degreesOfVision=degreesOfVision
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                            # Save model values for future use
                            #eventsString = "_".join([event.getShortPrintVersion() for event in events])
                            eventsString = f"{event1.timestep}-{event1.eventEffect.val}_{event2.timestep}-{event2.eventEffect.val}_{event3.timestep}-{event3.eventEffect.val}"
                            savePath = f"fov-3ev-n=500-{degreesOfVision}-{distTypeString}-drn={duration}_ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_n={n}_r={radius}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={threshold}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"
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
                            ServiceGeneral.logWithTime(f"Completed i={i}, thresholdType={thresholdType}, eventEffectOrder={eventEffectOrder.name}, eventEffectDisorder={eventEffectDisorder.name}, distributionType={distTypeString}, density={density}, duration={duration}, init={initialStateString},  in {ServiceGeneral.formatTime(endRun-startRun)}")

