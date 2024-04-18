import time
import random
import copy
from datetime import datetime

import VicsekWithNeighbourSelectionSwitchingCellBased
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral

import EnumSwitchType


import DefaultValues as dv

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

"""
radius = 10
tmax = 5000

ksSwitching = [1,5]

k = 1
density = 0.03
startK = time.time()
for noisePercentage in [0.5, 1, 1.5, 2]:
    startNoise = time.time()
    for i in range(7, 17):
        for orderState in orderStates:
            for disorderState in disorderStates:
                dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                switches = [[0, orderState],
                            [1000, disorderState], 
                            [4000, orderState]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=k, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
    endNoise = time.time()
    print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
endK = time.time()
print(f"Duration for k = {k}: {formatTime(endK-startK)}")
"""
"""
startTotal = time.time()
for density in densities:
    for k in kSwitching:
        startK = time.time()
        for noisePercentage in [0, 0.5, 1, 1.5, 2]:
            startNoise = time.time()
            for i in range(7, 17):
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()
                        domainSize = baseDomain
                        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
            endNoise = time.time()
            print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        print(f"Duration for k = {k}: {formatTime(endK-startK)}")
endTotal = time.time()
print(f"Duration for k = 1: {formatTime(endTotal-startTotal)}")

"""
"""
startTotal = time.time()
i=6
startI = time.time()
k=1
startK = time.time()
for noisePercentage in [1.5, 2]:
    startNoise = time.time()
    for density in densities:
        startDensity = time.time()
        for orderState in orderStates:
            for disorderState in disorderStates:
                dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                switches = [[0, orderState],
                            [1000, disorderState], 
                            [4000, orderState]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=k, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
        endDensity = time.time()
        print(f"Duration for density = {density}: {formatTime(endDensity-startDensity)}")
    endNoise = time.time()
    print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
endK = time.time()
print(f"Duration for k = {k}: {formatTime(endK-startK)}")
k=5
startK = time.time()
for noisePercentage in noisePercentages:
    startNoise = time.time()
    for density in densities:
        startDensity = time.time()
        for orderState in orderStates:
            for disorderState in disorderStates:
                dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                startRun = time.time()
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                switches = [[0, orderState],
                            [1000, disorderState], 
                            [4000, orderState]]

                #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                domainSize=domainSize, 
                                                                                numberOfParticles=n, 
                                                                                k=k, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                # Save model values for future use
                switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                endRun = time.time()
                print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
        endDensity = time.time()
        print(f"Duration for density = {density}: {formatTime(endDensity-startDensity)}")
    endNoise = time.time()
    print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
endK = time.time()
print(f"Duration for k = {k}: {formatTime(endK-startK)}")
endI = time.time()
print(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
print(f"Duration for total: {formatTime(endTotal-startTotal)}")


startTotal = time.time()
for i in range(7,11):
    startI = time.time()
    for k in ksSwitching:
        startK = time.time()
        for noisePercentage in noisePercentages:
            startNoise = time.time()
            for density in densities:
                startDensity = time.time()
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()
                        domainSize = baseDomain
                        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        print(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
                endDensity = time.time()
                print(f"Duration for density = {density}: {formatTime(endDensity-startDensity)}")
            endNoise = time.time()
            print(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        print(f"Duration for k = {k}: {formatTime(endK-startK)}")
    endI = time.time()
    print(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
print(f"Duration for total: {formatTime(endTotal-startTotal)}")

"""

"""
# VERY LOW DENSITY/N

low_densities =[0.0003, 0.0005, 0.0008, 0.001, 0.005]

startTotal = time.time()
for i in range(1,11):
    startI = time.time()
    for k in ks:
        startK = time.time()
        for noisePercentage in noisePercentages:
            startNoise = time.time()
            for density in low_densities:
                startN = time.time()
                #density = 0.01
                #domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                domainSize = baseDomain
                n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
                #density = ServicePreparation.getDensity(domainSize, n)
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                for neighbourSelectionMode in modes:
                    # ORDERED START
                    start = time.time()
                    tmax = 1000
                    ServiceGeneral.logWithTime(f"Executing low density with ordered start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, n={n}, density={density}, noisePercentage={noisePercentage}")
                    
                    if density < 0.001:
                        initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedForLowNumbers(domainSize, n)
                    else:
                        initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
                    
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")

                    # RANDOM START
                    start = time.time()
                    tmax = 1000
                    ServiceGeneral.logWithTime(f"Executing density-vs-noise with random start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, density={density}, noisePercentage={noisePercentage}")
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_random-start_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")
                # SWITCHING
                tmax = 5000
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()
                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
                endN = time.time()
                ServiceGeneral.logWithTime(f"Duration for density = {density}: {formatTime(endN-startN)}")
            endNoise = time.time()
            ServiceGeneral.logWithTime(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        ServiceGeneral.logWithTime(f"Duration for k = {k}: {formatTime(endK-startK)}")
    endI = time.time()
    ServiceGeneral.logWithTime(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Duration for total: {formatTime(endTotal-startTotal)}")
"""

low_densities =[0.0003, 0.0005, 0.0008, 0.001, 0.005]

startTotal = time.time()
for i in range(11,17):
    startI = time.time()
    for k in ks:
        startK = time.time()
        for noisePercentage in noisePercentages:
            startNoise = time.time()
            for density in low_densities:
                startN = time.time()
                #density = 0.01
                #domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                domainSize = baseDomain
                n = ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)
                #density = ServicePreparation.getDensity(domainSize, n)
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                # SWITCHING
                tmax = 5000
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()
                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
                endN = time.time()
                ServiceGeneral.logWithTime(f"Duration for density = {density}: {formatTime(endN-startN)}")
            endNoise = time.time()
            ServiceGeneral.logWithTime(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        ServiceGeneral.logWithTime(f"Duration for k = {k}: {formatTime(endK-startK)}")
    endI = time.time()
    ServiceGeneral.logWithTime(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Duration for total: {formatTime(endTotal-startTotal)}")

"""
startTotal = time.time()
for i in range(1,11):
    startI = time.time()
    for k in [1,3,5]:
        startK = time.time()
        for noisePercentage in noisePercentages:
            startNoise = time.time()
            for n in [3,5,8,10,50]:
                startN = time.time()
                density = 0.01
                domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, n)
                #domainSize = baseDomain
                #density = ServicePreparation.getDensity(domainSize, n)
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                for neighbourSelectionMode in modes:
                    # ORDERED START
                    start = time.time()
                    tmax = 1000
                    ServiceGeneral.logWithTime(f"Executing low density with ordered start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, n={n}, density={density}, noisePercentage={noisePercentage}")
                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedForLowNumbers(domainSize, n)
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_low-density_ordered-start_fixed-density_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")

                    # RANDOM START
                    start = time.time()
                    tmax = 1000
                    ServiceGeneral.logWithTime(f"Executing density-vs-noise with random start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, density={density}, noisePercentage={noisePercentage}")
                    simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=domainSize, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_low-density_random-start_fixed-density_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
                    end = time.time()
                    print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")
                # SWITCHING
                tmax = 5000
                for orderState in orderStates:
                    for disorderState in disorderStates:
                        dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{dateTime}: Start i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name}")
                        startRun = time.time()

                        switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
                        switches = [[0, orderState],
                                    [1000, disorderState], 
                                    [4000, orderState]]

                        #initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

                        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(orderState, 
                                                                                        domainSize=domainSize, 
                                                                                        numberOfParticles=n, 
                                                                                        k=k, 
                                                                                        noise=noise, 
                                                                                        radius=radius)
                        simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

                        # Save model values for future use
                        switchesStr = "_".join([f"{switch[0]}-{switch[1].name[0]}" for switch in switches])
                        ServiceSavedModel.saveModel(simulationData, colours, f"switch_low-density_fixed-density_switchType={switchType.name}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noisePercentage}%_{i}.json", simulator.getParameterSummary())
                        endRun = time.time()
                        ServiceGeneral.logWithTime(f"Completed i={i}, k={k}, noiseP={noisePercentage}, density={density}, orderState={orderState.name}, disorderState={disorderState.name} in {formatTime(endRun-startRun)}")
                endN = time.time()
                ServiceGeneral.logWithTime(f"Duration for density = {density}: {formatTime(endN-startN)}")
            endNoise = time.time()
            ServiceGeneral.logWithTime(f"Duration for noise = {noisePercentage}%: {formatTime(endNoise-startNoise)}")
        endK = time.time()
        ServiceGeneral.logWithTime(f"Duration for k = {k}: {formatTime(endK-startK)}")
    endI = time.time()
    ServiceGeneral.logWithTime(f"Duration for i = {i}: {formatTime(endI-startI)}")
endTotal = time.time()
ServiceGeneral.logWithTime(f"Duration for total: {formatTime(endTotal-startTotal)}")
"""


"""
domainSize = baseDomain
i = 1
tmax = 10000
k = 3
for noisePercentage in noisePercentages:
    for neighbourSelectionMode in [NeighbourSelectionMode.NEAREST,
                                   NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]:
        n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

        start = time.time()
        print(f"Executing density-vs-noise with random start run for i={i}, neighbourSelectionMode={neighbourSelectionMode.name}\nk={k}, density={density}, noisePercentage={noisePercentage}")
        simulator = VicsekWithNeighbourSelectionSwitchingCellBased.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                        domainSize=domainSize, 
                                                                        numberOfParticles=n, 
                                                                        k=k, 
                                                                        noise=noise, 
                                                                        radius=radius)
        simulationData, colours = simulator.simulate(tmax=tmax)

        # Save model values for future use
        ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_random-start_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
        end = time.time()
        print(f"Completed experiment for i={i}, nMode={neighbourSelectionMode.name}, k={k}, density={density}, noiseP={noisePercentage} in {formatTime(end-start)}")
"""