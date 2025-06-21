import ServicePreparation
import ServiceMetric

print(ServicePreparation.getNumberOfParticlesForConstantDensity(0.09, (25, 25)))

positions, orientations = ServicePreparation.createOrderedInitialDistributionEquidistancedForLowNumbers((25,25), 3)
print(orientations)

print(ServiceMetric.computeOrder(orientations))
print(ServicePreparation.getNoiseAmplitudeValueForPercentage(1))