import numpy as np
import random

def getDomainSizeForConstantDensity(density, numberOfParticles):
    area = numberOfParticles / density
    return (np.sqrt(area), np.sqrt(area))

def getNumberOfParticlesForConstantDensity(density, domainSize):
    return density * (domainSize[0] * domainSize[1]) # density * area

def getDensity(domainSize, numberOfParticles):
    return numberOfParticles / (domainSize[0] * domainSize[1]) # n / area

def createOrderedInitialDistributionEquidistanced(domainSize, numberOfParticles, angleX=None, angleY=None):
    # choose random angle for orientations
    if angleX is None:
        angleX = random.random()
    if angleY is None:
        angleY = random.random()

    # prepare the distribution for the positions
    xLength = domainSize[0]
    yLength = domainSize[1]
    
    area = xLength * yLength
    pointArea = area / numberOfParticles
    length = np.sqrt(pointArea)

    # initialise the initialState components
    positions = np.zeros((numberOfParticles, 2))
    orientations = np.zeros((numberOfParticles, 2))
    orientations[:, 0] = angleX
    orientations[:, 1] = angleY

    counter = 0
    # set the position & orientation of every particle
    for x in np.arange(length/2, xLength, length):
        for y in np.arange(length/2, yLength, length):
            positions[counter] = [x,y]
            #orientations[counter] = [x + orientationDistance * np.cos(angle), y + orientationDistance * np.sin(angle)]
            counter += 1

    # normalize orientations
    #orientations = orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

    print(f"angleX: {angleX}, angleY: {angleY}, orientations[0] = {orientations[0]}")
    return positions, orientations