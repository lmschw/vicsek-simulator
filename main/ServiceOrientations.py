import math
import numpy as np

"""
Service containing static methods to manipulate orientations and determine the effect of orientation of vision etc.
"""

def determineMinMaxAngleOfVision(orientation, degreesOfVision):
    """
    Determines the boundaries of the field of vision of a particle.

    Params:
        - orientation (array of floats): the current orientation of the particle
        - degreesOfVision (int [0,2*np.pi]): how many degrees of its surroundings the particle can see.

    Returns:
        Two integers representing the angular boundary of vision, i.e. the minimal and maximal angle that is still visible to the particle
    """
    angularDistance = degreesOfVision / 2
    currentAngle = normaliseAngle(computeAngleForOrientation(orientation))
    
    minAngle = normaliseAngle(currentAngle - angularDistance)
    maxAngle = normaliseAngle(currentAngle + angularDistance)

    return minAngle, maxAngle

def isInFieldOfVision(positionParticle, positionCandidate, minAngle, maxAngle):
    """
    Checks if a given particle is within the field of vision of the current particle.

    Params:
        - positionParticle (array of floats): the position of the current particle in (x,y)-coordinates
        - positionCandidate (array of floats): the position of the particle that is considered as potentially visible to the current particle
        - minAngle (float): the left boundary of the field of vision
        - maxAngle (float): the right boundary of the field of vision

    Returns:
        A boolean representing whether the given particle is in the field of vision of the current particle.
    """
    if positionCandidate[0] == positionParticle[0] and positionParticle[1] == positionCandidate[1]:
        return True
    orientationFromOrigin = positionCandidate - positionParticle
    angleRadian = np.arctan(orientationFromOrigin[1]/orientationFromOrigin[0])
    angle = normaliseAngle(angleRadian)
    if minAngle < maxAngle:
        isIn = angle >= minAngle and angle <= maxAngle
    else:
        isIn = angle >= minAngle or angle <= maxAngle
    return isIn

def isParticleOccluded(particleIdx, otherIdx, positions, candidates, epsilon=1):
    """
    Checks if a particle is occluded from the perspective of the current particle.

    Params:
        - particleIdx (int): the index of the current particle
        - otherIdx (int): the index of the particle to be checked
        - positions (array of arrays of float): the position of every particle at the given timestep
        - candidates (array of int): the indices of all particles within the radius of the current particle
        - epsilon (float) [optional]: the margin of error when judging if the particles are colinear

    Returns:
        A boolean representing if the other particle is hidden from the current particle.
    """
    if particleIdx == otherIdx:
        return False
    isOccluded = False
    if len(candidates) > 0:
        for candidateIdx in candidates[0]:
            if candidateIdx != particleIdx and candidateIdx != otherIdx:
                isOccluded = isOccluded or isCOccludingB(positions[particleIdx], positions[otherIdx], positions[candidateIdx], epsilon)
    return isOccluded

def isCOccludingB(a, b, c, epsilon=1):
    """
    Checks if a third particle is hiding the second particle from the first particle

    If they are colinear, i.e. all on the same line, the following rules apply:
        A ----- C ----- B -> true
        A ----- B ----- C -> false
        B ----- A ----- C -> false
        B ----- C ----- A -> true
        C ----- A ----- B -> false
        C ----- B ----- A -> false
    If they are not colinear, then there is no possibility of occlusion.

    Params:
        - a (array of float): the position of the first particle (the current particle)
        - b (array of float): the position of the second particle (the occlusion candidate)
        - c (array of float): the position of the third particle (the potential middle particle)
        - epsilon (float) [optional]: the margin of error when judging if the particles are colinear

    Returns:
        A boolean representing whether B is hidden from A by C
    """
    return isCollinear(a, b, c, epsilon) and isCBetweenAB(a, b, c)


def isCollinear(a, b, c, epsilon=1):
    """
    Checks if three particles are positioned on the same straight line.

    Params:
        - a (array of float): the position of the first particle (the current particle)
        - b (array of float): the position of the second particle (the occlusion candidate)
        - c (array of float): the position of the third particle (the potential middle particle)
        - epsilon (float) [optional]: the margin of error when judging if the particles are colinear

    Returns:
        A boolean representing whether the three particles are arranged in a straight line.

    """
    return np.absolute((a[1] - b[1]) * (a[0] - c[0]) - (a[1] - c[1]) * (a[0] - b[0])) <= epsilon

def isCBetweenAB(a, b, c):
    """
    Checks if the third particle lies between the first and the second particle on the x-axis and y-axis.

    Params:
        - a (array of float): the position of the first particle (the current particle)
        - b (array of float): the position of the second particle (the occlusion candidate)
        - c (array of float): the position of the third particle (the potential middle particle)
    
    Returns:
        A boolean representing whether c lies between a and b
    """
    isBetweenX = a[0] <= c[0] <= b[0] or a[0] >= c[0] >= b[0]
    isBetweenY = a[1] <= c[1] <= b[1] or a[1] >= c[1] >= b[1]
    return isBetweenX and isBetweenY

def computeAngleForOrientation(orientation):
    """
    Computes the angle in radians based on the (u,v)-coordinates of the current orientation.

    Params:
        - orientation (array of floats): the current orientation in (u,v)-coordinates

    Returns:
        A float representin the angle in radians.
    """
    return np.arctan2(orientation[1], orientation[0])

def computeUvCoordinates(angle):
    """
    Computes the (u,v)-coordinates based on the angle.

    Params:
        - angle (float): the angle in radians

    Returns:
        An array containing the [u, v]-coordinates corresponding to the angle.
    """
    # compute the uv-coordinates
    U = np.cos(angle)
    V = np.sin(angle)
    
    return [U,V]

def normaliseAngle(angle):
    """
    Normalises the degrees of an angle to be between 0 and 2pi.

    Params:
        - angle (float): the angle in radians

    Returns:
        Float representing the normalised angle.
    """
    if angle < 0:
        return (2*np.pi) - abs(angle)
    if angle > (2*np.pi):
        return angle % (2*np.pi)
    return angle