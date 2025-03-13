import time
import numpy as np

import VicsekWithNeighbourSelectionSwitchingCellBased
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
import ServiceMetric
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]
angle = np.pi
blockSteps = -1
psteps = 100
numbersOfPreviousSteps = [psteps]

tmax = 15000
noiseP = 1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseP)
speed = 1
domainSize = (50, 50)

ks = [5]

nsmCombos = [[NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.FARTHEST],
             [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]]

kCombos = [[1,5]]

densities = [0.09, 0.06]
radius = 20

areas = [(domainSize[0]/2, domainSize[1]/2, radius)]
duration = 1000
percentage = 100
movementPattern = MovementPattern.STATIC
distributionType = DistributionType.LOCAL_SINGLE_SITE
e1Start = 5000

neighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

iStart = 1
iStop = 11

saveLocation = ""

k = 5

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    for neighbourSelectionMode in neighbourSelectionModes:
        for initialStateString in ["ordered", "random"]:
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
                        initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(neighbourSelectionMode, domainSize, n)
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection(
                                                                                    neighbourSelectionModel=neighbourSelectionMode, 
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
                                                                                    )
                    if initialStateString == "ordered":
                        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
                    else:
                        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

                    # Save model values for future use
                    eventsString = f"{event1.timestep}-{event1.eventEffect.val}"
                    savePath = f"{saveLocation}/local_1e_nosw_{initialStateString}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_k={k}_noise={noiseP}_drn={duration}_{eventsString}_{i}"
                    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                    endRun = time.time()
                    ServiceGeneral.logWithTime(f"Completed k-switch d={density}, r={radius}, drn={duration}, nsm={neighbourSelectionMode.name}, {initialStateString}, eventEffect={eventEffectOrder.name}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")

                    endK = time.time()