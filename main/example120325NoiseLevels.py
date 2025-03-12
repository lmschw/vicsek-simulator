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

tmax = 100000
noisePs = [1, 4]
speed = 1
domainSize = (50, 50)

ks = [1]

densities = [0.06, 0.09, 0.12, 0.03, 0.01]
radii = [20, 15, 10, 5]

iStart = 1
iStop = 11

saveLocation = ""

for density in densities:
    for radius in radii:
        for noiseP in noisePs:
            noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseP)
            for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST,
                                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                           NeighbourSelectionMode.FARTHEST,
                                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
                n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
                for k in ks:
                    for initialStateString in ["ordered", "random"]:
                        startValue = neighbourSelectionMode
                        for i in range(iStart,iStop):
                            ServiceGeneral.logWithTime(f"Started d={density}, r={radius},k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, i={i}")
                            startRun = time.time()

                            if initialStateString == "ordered":
                                initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)
                            savePath = f"{saveLocation}global_noev_nosw_{initialStateString}_st={startValue.value}_d={density}_n={n}_r={radius}_tmax={tmax}_k={k}_noise={noiseP}_{i}"

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
                                                                                            returnHistories=False,
                                                                                            logPath=savePath,
                                                                                            logInterval=1
                                                                                            )
                            if initialStateString == "ordered":
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState)
                            else:
                                simulationData, colours, switchValues = simulator.simulate(tmax=tmax)

                            endRun = time.time()
                            ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
