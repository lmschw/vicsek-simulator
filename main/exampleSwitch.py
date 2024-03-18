"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelectionSwitching
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode
import EnumSwitchType
import ServicePreparation

import DefaultValues as dv


"""
n = 500
domainSize=ServicePreparation.getDomainSizeForConstantDensity(0.05, n)
k = 5
noise = 0
noiseAmplitudePercentage = 0.5
noiseSwitchValue = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseAmplitudePercentage)
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
tmax = 4000
noiseSwitchTimestep = 2000

#initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, noiseSwitchValue=noiseSwitchValue, noiseSwitchTimestep=noiseSwitchTimestep)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"switch_{neighbourSelectionMode.name}_tmax={tmax}_tswitch={noiseSwitchTimestep}_n={n}_k={k}_noise={noise}_noisePercentageSwitch={noiseAmplitudePercentage}%_radius={radius}.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())


# Display Animation
preparedAnimator.showAnimation()
"""

n = 500
domainSize=ServicePreparation.getDomainSizeForConstantDensity(0.05, n)
k = 5
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(0.5)
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST
tmax = 5000

switchType = EnumSwitchType.SwitchType.NEIGHBOUR_SELECTION_MODE
switches = [[1000, EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST], 
            [4000, EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST]]

print(f"switches={switches}")
#initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

simulator = VicsekWithNeighbourSelectionSwitching.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, switchType=switchType, switches=switches)

# Save model values for future use
switchesStr = "_".join([f"{switch[0]}-{switch[1].name}" for switch in switches])
ServiceSavedModel.saveModel(simulationData, colours, f"switch_{neighbourSelectionMode.name}_switchType={switchType}_switches={switchesStr}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())


# Display Animation
preparedAnimator.showAnimation()
