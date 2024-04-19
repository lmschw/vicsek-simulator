import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral

from EnumSwitchType import SwitchType


def formatTime(timeInSecs):
    mins = int(timeInSecs / 60)
    secs = timeInSecs % 60

    if mins >= 60:
        hours = int(mins / 60)
        mins = mins % 60
        return f"{hours}h {mins}min {secs:.1f}s"
    return f"{mins}min {secs:.1f}s"


modes = [NeighbourSelectionMode.RANDOM,
         NeighbourSelectionMode.NEAREST,
         NeighbourSelectionMode.FARTHEST,
         NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         NeighbourSelectionMode.ALL]

low_densities =[0.0003, 0.0005, 0.0008, 0.001, 0.005]
densities = [0.01, 0.03, 0.05, 0.07, 0.09]

swarmSizes = [100, 300, 500, 700, 900]
baseDomain = (100, 100)
baseSwarmSize = 500

ks = [1, 3, 5]

noisePercentages = [0, 0.5, 1, 1.5, 2] # also run with 0 noise as baseline

disorderStates = [NeighbourSelectionMode.NEAREST,
                  NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]
orderStates = [NeighbourSelectionMode.RANDOM,
               NeighbourSelectionMode.FARTHEST,
               NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
               NeighbourSelectionMode.ALL]



density = 0.01
radius = 10
noisePercentage = 1
k = 1
neighbourSelectionMode = NeighbourSelectionMode.NEAREST
tmax = 5000
i = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
orderThreshold = 0.05
"""
switches = [[0, orderValue],
            [1000, disorderValue], 
            [4000, orderValue]]
"""

for i in range(1,11):
    for orderThreshold in []:
        startRun = time.time()
        ServiceGeneral.logWithTime(f"Start i={i}, noiseP={noisePercentage}, density={density}, neighbourSelectionMode={neighbourSelectionMode.name}, orderVal={orderValue}, disorderVal={disorderValue}, threshold={orderThreshold}")
        domainSize = baseDomain
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
        simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                        domainSize=domainSize, 
                                                                        numberOfParticles=n, 
                                                                        k=orderValue, 
                                                                        noise=noise, 
                                                                        radius=radius,
                                                                        switchType=switchType,
                                                                        switchValues=(orderValue, disorderValue))
        simulationData, colours, switchValues = simulator.simulate(tmax=tmax)

        # Save model values for future use
        ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"switch_individual_switchType={switchType.name}_orderVal={orderValue}_disorderVal={disorderValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_{i}.json", modelParams=simulator.getParameterSummary())
        endRun = time.time()
        ServiceGeneral.logWithTime(f"Completed i={i}, noiseP={noisePercentage}, density={density},  neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderValue}, disorderK={disorderValue} in {formatTime(endRun-startRun)}")


"""
startTotal = time.time()
for density in densities:
    startDensity = time.time()
    for noisePercentage in noisePercentages:
        startNoise = time.time()
        for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST,
                                       NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]:
            startMode = time.time()
            for i in range(1,11):
                ServiceGeneral.logWithTime(f"Start i={i}, noiseP={noisePercentage}, density={density}, neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.K
                switches = [[0, orderK],
                            [1000, disorderK], 
                            [4000, orderK]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=orderK, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1]}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, noiseP={noisePercentage}, density={density},  neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK} in {formatTime(endRun-startRun)}")
            endMode = time.time()
            ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage}, mode={neighbourSelectionMode.name} completed in {formatTime(endMode-startMode)}")
        endNoise = time.time()
        ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage} completed in {formatTime(endNoise-startNoise)}")
    endDensity = time.time()
    ServiceGeneral.logWithTime(f"density={density} completed in {formatTime(endDensity-startDensity)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Total ompleted in {formatTime(endTotal-startTotal)}")

"""
"""
startTotal = time.time()
for density in low_densities:
    startDensity = time.time()
    for noisePercentage in noisePercentages:
        startNoise = time.time()
        for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST,
                                       NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                       NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
                                       NeighbourSelectionMode.ALL]:
            startMode = time.time()
            for i in range(1,11):
                ServiceGeneral.logWithTime(f"Start i={i}, noiseP={noisePercentage}, density={density}, neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.K
                switches = [[0, orderK],
                            [1000, disorderK], 
                            [4000, orderK]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=orderK, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1]}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, noiseP={noisePercentage}, density={density},  neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK} in {formatTime(endRun-startRun)}")
            endMode = time.time()
            ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage}, mode={neighbourSelectionMode.name} completed in {formatTime(endMode-startMode)}")
        endNoise = time.time()
        ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage} completed in {formatTime(endNoise-startNoise)}")
    endDensity = time.time()
    ServiceGeneral.logWithTime(f"density={density} completed in {formatTime(endDensity-startDensity)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Total ompleted in {formatTime(endTotal-startTotal)}")
"""
"""
tmax = 10000
startTotal = time.time()
for density in low_densities:
    startDensity = time.time()
    for noisePercentage in noisePercentages:
        startNoise = time.time()
        for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST,
                                       NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                       NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
                                       NeighbourSelectionMode.ALL]:
            startMode = time.time()
            for i in range(1,11):
                ServiceGeneral.logWithTime(f"Start i={i}, noiseP={noisePercentage}, density={density}, neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.K
                switches = [[0, orderK],
                            [2000, disorderK], 
                            [8000, orderK]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=orderK, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1]}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, noiseP={noisePercentage}, density={density},  neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderK}, disorderK={disorderK} in {formatTime(endRun-startRun)}")
            endMode = time.time()
            ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage}, mode={neighbourSelectionMode.name} completed in {formatTime(endMode-startMode)}")
        endNoise = time.time()
        ServiceGeneral.logWithTime(f"density={density}, noiseP={noisePercentage} completed in {formatTime(endNoise-startNoise)}")
    endDensity = time.time()
    ServiceGeneral.logWithTime(f"density={density} completed in {formatTime(endDensity-startDensity)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Total ompleted in {formatTime(endTotal-startTotal)}")
"""