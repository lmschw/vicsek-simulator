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

ks = [1]

nsmCombos = [[NeighbourSelectionMode.NEAREST, NeighbourSelectionMode.FARTHEST],
             [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]]

kCombos = [[1,5]]

densities = [0.09, 0.06]
radius = 20

areas = [(domainSize[0]/2, domainSize[1]/2, radius)]

iStart = 1
iStop = 11

saveLocation = ""

for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)
    # --- single event, no switchvals for all modes with k = 1 and k = 5 (15000)        
    for nsm in [NeighbourSelectionMode.NEAREST,
                NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]:
        for nsmCombo in nsmCombos:
            disorderValue, orderValue = nsmCombo
            for initialStateString in ["ordered", "random"]:
                startNsm = time.time()
                switchType = SwitchType.K
                for initialStateString in ["ordered", "random"]:
                    if initialStateString == "ordered":
                        startValue = disorderValue
                    else:
                        startValue = orderValue

                    for i in range(iStart,iStop):
                        ServiceGeneral.logWithTime(f"Started k switch d={density}, r={radius}, nsm={nsm.value}, {initialStateString}, i={i}")

                        startRun = time.time()
                        logPath = f"{saveLocation}local_1e_switchType={switchType.value}_{initialStateString}_st={startValue}_o={orderValue}_do={disorderValue}_d={density}_n={n}_r={radius}_nsm={nsm.value}_noise={noiseP}_{i}"
                        if initialStateString == "ordered":
                            initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)
                        simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection(
                                                                                        neighbourSelectionModel=nsm, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=startValue, 
                                                                                        noise=noise, 
                                                                                        radius=radius,
                                                                                        switchType=switchType,
                                                                                        switchValues=(orderValue, disorderValue),
                                                                                        thresholdType=thresholdType,
                                                                                        orderThresholds=threshold,
                                                                                        numberPreviousStepsForThreshold=psteps,
                                                                                        switchBlockedAfterEventTimesteps=blockSteps,
                                                                                        speed=speed,
                                                                                        returnHistories=False,
                                                                                        logPath=logPath,
                                                                                        logInterval=1
                                                                                        )
                        if initialStateString == "ordered":
                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState)
                        else:
                            simulationData, colours, switchValues = simulator.simulate(tmax=tmax)

                    endRun = time.time()
                    ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, nsm={nsm.value},{initialStateString}, i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
