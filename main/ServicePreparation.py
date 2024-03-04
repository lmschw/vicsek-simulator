import numpy as np

def getDomainSizeForConstantDensity(density, numberOfParticles):
    area = numberOfParticles / density
    return (np.sqrt(area), np.sqrt(area))

def getNumberOfParticlesForConstantDensity(density, domainSize):
    return density * (domainSize[0] * domainSize[1]) # density * area

def getDensity(domainSize, numberOfParticles):
    return numberOfParticles / (domainSize[0] * domainSize[1]) # n / area