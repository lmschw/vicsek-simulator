"""
Contains a simulation for the standard 2D Vicsek model
"""

import VicsekWithNeighbourSelection
import AnimatorMatplotlib
import Animator2D
import ServiceSavedModel
import EnumNeighbourSelectionMode
import ServicePreparation

import DefaultValues as dv

"""
n = 400
domainSize=(100,100)
k = 5
noise = 0.1
radius= 10
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 20000

initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                numberOfParticles=n, 
                                                                k=k, 
                                                                noise=noise, 
                                                                radius=radius)
simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

# Save model values for future use
ServiceSavedModel.saveModel(simulationData, colours, f"{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}.json", simulator.getParameterSummary())

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

# Display Animation
preparedAnimator.showAnimation()
"""


"""
n = 500
k = 5
radius= 10
#neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE
tmax = 3000
domainSize = ServicePreparation.getDomainSizeForConstantDensity(0.05, n)
modes = [
            EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM]
         """
"""
for neighbourSelectionMode in modes:
    for noiseAmplitudePercentage in [2.5, 3]:
        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseAmplitudePercentage)
        for i in range(1, 6):
            initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

            simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                            domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                            numberOfParticles=n, 
                                                                            k=k, 
                                                                            noise=noise, 
                                                                            radius=radius)
            simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

            # Save model values for future use
            ServiceSavedModel.saveModel(simulationData, colours, f"examples/dislocationExamples/model_{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noiseAmplitudePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())

            
            # Initalise the animator
            animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

            # prepare the animator
            preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
            preparedAnimator.setParams(simulator.getParameterSummary())
            preparedAnimator.saveAnimation(f"examples/dislocationExamples/visualisation_mode={neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noise={noise}_radius={radius}")
        
"""
"""           
neighbourSelectionMode = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
noiseAmplitudePercentage = 2
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noiseAmplitudePercentage)
for i in range(5, 6):
    initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)

    simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                    domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                    numberOfParticles=n, 
                                                                    k=k, 
                                                                    noise=noise, 
                                                                    radius=radius)
    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

    # Save model values for future use
    ServiceSavedModel.saveModel(simulationData, colours, f"examples/dislocationExamples/model_{neighbourSelectionMode.name}_tmax={tmax}_n={n}_k={k}_noisePercentage={noiseAmplitudePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())
    """

modes = [EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE,
         EnumNeighbourSelectionMode.NeighbourSelectionMode.ALL]

#densities = [0.01, 0.03, 0.05, 0.07, 0.09]
densities = [0.01, 0.03, 0.05, 0.07, 0.09]

swarmSizes = [100, 300, 500, 700, 900]
baseDomain = (100, 100)
baseSwarmSize = 500

ks = [1, 3, 5]

noisePercentages = [0, 0.1, 0.5, 1, 1.5, 2] # also run with 0 noise as baseline
baseNoise = 1

radius = 10
tmax = 1000

for i in range(1, 6):
    for neighbourSelectionMode in modes:
        for k in ks:
            for density in densities:
                for n in swarmSizes:
                    domainSize = ServicePreparation.getDomainSizeForConstantDensity(density, baseSwarmSize)
                    initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
                    noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(baseNoise)

                    simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                    domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                                    numberOfParticles=n, 
                                                                                    k=k, 
                                                                                    noise=noise, 
                                                                                    radius=radius)
                    simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                    # Save model values for future use
                    ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-swarmsize_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={baseNoise}%_radius={radius}_{i}.json", simulator.getParameterSummary())
            for noisePercentage in noisePercentages:
                domainSize = baseDomain
                n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
                initialState = ServicePreparation.createOrderedInitialDistributionEquidistanced(domainSize, n)
                noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

                simulator = VicsekWithNeighbourSelection.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                                domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, 
                                                                                numberOfParticles=n, 
                                                                                k=k, 
                                                                                noise=noise, 
                                                                                radius=radius)
                simulationData, colours = simulator.simulate(tmax=tmax, initialState=initialState)

                # Save model values for future use
                ServiceSavedModel.saveModel(simulationData, colours, f"model_density-vs-noise_{neighbourSelectionMode.name}_tmax={tmax}_density={density}_n={n}_k={k}_noisePercentage={noisePercentage}%_radius={radius}_{i}.json", simulator.getParameterSummary())


