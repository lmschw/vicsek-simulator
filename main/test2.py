import numpy as np
import time

from EnumSwitchType import SwitchType
from EnumEventEffect import EventEffect
from EnumMovementPattern import MovementPattern
from EnumDistributionType import DistributionType
from EnumThresholdType import ThresholdType
from EnumNeighbourSelectionMode import NeighbourSelectionMode

from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
import ServicePreparation
import ServiceGeneral



def getOrderDisorderValue(switchType):
    match switchType:
        case SwitchType.K:
            return 5, 1
        case SwitchType.NEIGHBOUR_SELECTION_MODE:
            return NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST


tmax = 8000
switchType = SwitchType.NEIGHBOUR_SELECTION_MODE
orderValue, disorderValue = getOrderDisorderValue(switchType)
k = 1
noisePercentage =1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
iStart = 1
iStop = 2
e1Start = 1000
duration = 1000
percentage = 100
angle = np.pi
movementPattern = MovementPattern.STATIC
distributionType = DistributionType.LOCAL_SINGLE_SITE
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]
speed = 1
numberOfPreviousSteps = 50

kMax = 5
domainSize = (100, 100)

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]


for i in range(iStart,iStop):
    for density in [0.01, 0.03, 0.05, 0.07, 0.09]:
        n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
        radius = ServicePreparation.getRadiusToSeeOnAverageNNeighbours(n=kMax, density=density)
        areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
        distTypeString = "lssmid"
        for initialStateString in ["ordered"]:
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
                    savePath = f"test_radiusFormula_radius={radius}_density={density}_{initialStateString}_switchType={switchType.value}_st={startValue.value}_o={orderValue.value}_do={disorderValue.value}_d={density}_n={n}_k={k}_noise={noisePercentage}_{eventsString}_{i}"
                    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                    endRun = time.time()
                    ServiceGeneral.logWithTime(f"Completed 1e nsm i={i}, eventEffect={eventEffectOrder.name}, duration={duration}, init={initialStateString} in {ServiceGeneral.formatTime(endRun-startRun)}")
