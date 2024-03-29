import numpy as np
import random

def getDomainSizeForConstantDensity(density, numberOfParticles):
    """
    Computes the domain size to keep the density constant for the supplied number of particles.
    Density formula: "density" = "number of particles" / "domain area"

    Parameters:
        - density (float): the desired constant density of the domain
        - numberOfParticles (int): the number of particles to be placed in the domain

    Returns:
        A tuple containing the x and y dimensions of the domain size that corresponds to the density.
    """
    area = numberOfParticles / density
    return (np.sqrt(area), np.sqrt(area))

def getNumberOfParticlesForConstantDensity(density, domainSize):
    """
    Computes the number of particles to keep the density constant for the supplied domain size.
    Density formula: "density" = "number of particles" / "domain area"

    Parameters:
        - density (float): the desired constant density of the domain
        - domainSize (tuple): tuple containing the x and y dimensions of the domain size

    Returns:
        The number of particles to be placed in the domain that corresponds to the density.
    """
    return density * (domainSize[0] * domainSize[1]) # density * area

def getDensity(domainSize, numberOfParticles):
    """
    Computes the density of a given system.
    Density formula: "density" = "number of particles" / "domain area"

    Parameters:
        - domainSize (tuple): tuple containing the x and y dimensions of the domain size
        - numberOfParticles (int): the number of particles to be placed in the domain

    Returns:
        The density of the system as a float.
    """
    return numberOfParticles / (domainSize[0] * domainSize[1]) # n / area

def getNoiseAmplitudeValueForPercentage(percentage):
    """
    Paramters:
        - percentage (int, 1-100)
    """
    return 2 * np.pi * (percentage/100)

def createOrderedInitialDistributionEquidistanced(domainSize, numberOfParticles, angleX=None, angleY=None):
    """
    Creates an ordered, equidistanced initial distribution of particles in a domain. 
    The particles are placed in a grid-like fashion. The orientation of the particles is random unless specified
    but always the same for all particles.

    Parameters:
        - domainSize (tuple): tuple containing the x and y dimensions of the domain size
        - numberOfParticles (int): the number of particles to be placed in the domain
        - angleX (float [0,1)): first angle component to specify the orientation of all particles
        - angleY (float [0,1)): second angle component to specify the orientation of all particles

    Returns:
        Positions and orientations for all particles within the domain. Can be used as the initial state of a Vicsek simulation.

    """
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

    # set the orientation for all particles
    orientations[:, 0] = angleX
    orientations[:, 1] = angleY

    counter = 0
    # set the position of every particle
    for x in np.arange(length/2, xLength, length):
        for y in np.arange(length/2, yLength, length):
            positions[counter] = [x,y]
            counter += 1

    return positions, orientations