import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration
import AnimatorMatplotlib
import Animator2D

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

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


thresholdType = ThresholdType.TWO_THRESHOLDS

tmax = 15000
i = 1

eventEffect1 = EventEffect.TOWARDS_ORIGIN
eventEffect2 = EventEffect.ALIGN_TO_FIXED_ANGLE

blockSteps = -1
numberOfPreviousSteps = 1000
percentage = 50
initialStateString = "ordered"
for i in range(1,2):
    if initialStateString == "ordered":
        targetSwitchValue=disorderValue
        startValue = orderValue
    else:
        targetSwitchValue=orderValue
        startValue = disorderValue
    for radius in [30]:

        for thresholds in [[0.1,0.9]]:
            for density in [0.01]:
                n = 100
                domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                
                #n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))

                event1 = ExternalStimulusOrientationChangeEventDuration(
                                                    startTimestep=0, 
                                                    endTimestep=tmax,
                                                    percentage=percentage,
                                                    angle=angle,
                                                    eventEffect=EventEffect.AWAY_FROM_ORIGIN,
                                                    movementPattern=MovementPattern.RANDOM,
                                                    movementSpeed=1,
                                                    domainSize=domainSize,
                                                    distributionType=DistributionType.LOCAL_SINGLE_SITE,
                                                    areas=[(20,20,radius)]
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
                savePath = f"test_predator_std_ind_avg_{thresholdType.value}_{initialStateString}_st={switchType.value}_o={orderValue}_do={disorderValue}_s={startValue}_d={density}_n={n}_r={radius}_{neighbourSelectionMode.value}_noise={noisePercentage}_th={thresholds}_psteps={numberOfPreviousSteps}_bs={blockSteps}_e-{eventsString}_{i}"

                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                # Initalise the animator
                animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                # prepare the animator
                preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
                preparedAnimator.setParams(simulator.getParameterSummary())
                preparedAnimator.saveAnimation(f"{savePath}.mp4")

                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, r={radius}, thresholds={thresholds}, density={density} in {ServiceGeneral.formatTime(endRun-startRun)}")
