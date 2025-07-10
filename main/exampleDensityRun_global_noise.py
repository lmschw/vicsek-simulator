import time
import numpy as np

import VicsekWithNeighbourSelectionSwitchingCellBased
import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates a complete set of data for a single density value
for "Neighbour selection can cause collective response"
--------------------------------------------------------------------------------
"""

angle = np.pi
blockSteps = -1
thresholdType = ThresholdType.HYSTERESIS
threshold = [0.1]


#domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.09, 100)
domainSize = (50, 50)

distTypeString = "lssmid"
distributionType = DistributionType.LOCAL_SINGLE_SITE
percentage = 100
movementPattern = MovementPattern.STATIC
e1Start = 5000

tmaxWithoutEvent = 15000
tmaxWithEvent = 15000

densities = [0.09]
psteps = 100
numbersOfPreviousSteps = [psteps]
durations = [1000]
ks = [1]
radii = [10] # area is always 4x bigger than the last

neighbourSelectionModes = [NeighbourSelectionMode.ALL,
                           NeighbourSelectionMode.RANDOM,
                           NeighbourSelectionMode.NEAREST,
                           NeighbourSelectionMode.FARTHEST,
                           NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                           NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

reducedNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                                  NeighbourSelectionMode.FARTHEST,
                                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                  NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

orderNeighbourSelectionModes = [NeighbourSelectionMode.ALL,
                                NeighbourSelectionMode.RANDOM,
                                NeighbourSelectionMode.FARTHEST,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

disorderNeighbourSelectionModes = [NeighbourSelectionMode.NEAREST,
                                   NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]

localNeighbourSelectionmodes = [NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

eventEffects = [EventEffect.ALIGN_TO_FIXED_ANGLE,
                EventEffect.AWAY_FROM_ORIGIN,
                EventEffect.RANDOM]

eventEffectsOrder = [
                     EventEffect.ALIGN_TO_FIXED_ANGLE,
                     ]

eventEffectsDisorder = [EventEffect.AWAY_FROM_ORIGIN,
                        EventEffect.RANDOM]

#baseLocation = f"D:/vicsek-data2/adaptive_radius"
saveLocation = "J:/noise_global/"
iStart = 1
iStop = 11

startTotal = time.time()
for density in densities:
    n = ServicePreparation.getNumberOfParticlesForConstantDensity(density=density, domainSize=domainSize)   
    # ----------------------------------------------- GLOBAL STARTS HERE ----------------------------------------------
    #saveLocation = f"{baseLocation}/global"
    for radius in radii:
        for speed in [1]:
            for noisePercentage in [1, 4]:
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                print(f"d={density}, n={n}, r={radius}, size={domainSize}")

        # ---neighbourSelectionMode only (3000) for all 6 modes
                tmax = tmaxWithoutEvent

                for initialStateString in ["ordered", "random"]:
                    for neighbourSelectionMode in reducedNeighbourSelectionModes:
                        for k in ks:
                            for i in range(iStart,iStop): 
                                ServiceGeneral.logWithTime(f"Starting d={density}, r={radius}, {initialStateString}, nsm={neighbourSelectionMode.name}, k={k} i={i}")
                                startRun = time.time()

                                if initialStateString == "ordered":
                                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(
                                                                                                neighbourSelectionModel=neighbourSelectionMode, 
                                                                                                domainSize=domainSize, 
                                                                                                numberOfParticles=n, 
                                                                                                k=k, 
                                                                                                noise=noise, 
                                                                                                radius=radius,
                                                                                                speed=speed,
                                                                                                )
                                if initialStateString == "ordered":
                                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)
                                else:
                                    simulationData, colours = simulator.simulate(tmax=tmax)

                                # Save model values for future use
                                savePath = f"{saveLocation}global_nosw_noev_{initialStateString}_d={density}_n={n}_r={radius}_nsm={neighbourSelectionMode.value}_k={k}_noise={noisePercentage}_speed={speed}_{i}.json"
                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

                                endRun = time.time()
                                ServiceGeneral.logWithTime(f"Completed d={density}, r={radius}, {initialStateString}, nsm={neighbourSelectionMode.name}, k={k} i={i} in {ServiceGeneral.formatTime(endRun-startRun)}")
                endTotal = time.time()
                ServiceGeneral.logWithTime(f"Completed GLOBAL in {ServiceGeneral.formatTime(endTotal-startTotal)}")

                


endTotal = time.time()
ServiceGeneral.logWithTime(f"Completed total in {ServiceGeneral.formatTime(endTotal-startTotal)}")
