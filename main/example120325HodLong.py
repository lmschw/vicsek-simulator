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

tmax = 10_000_000
noiseP = 1
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseP)
speed = 1
domainSize = (50, 50)

neighbourSelectionMode = NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE
ks = [1,5]

densities = [0.06, 0.09]
radius = 20

areas = [(domainSize[0]/2, domainSize[1]/2, radius)]

iStart = 1
iStop = 2

saveLocation = ""

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
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
                                                                                    logInterval=1000
                                                                                    )
                    if initialStateString == "ordered":
                        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState)
                    else:
                        simulationData, colours, switchValues = simulator.simulate(tmax=tmax)

                    endRun = time.time()
                    ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, k={k}, nsm={neighbourSelectionMode.name}, {initialStateString}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
