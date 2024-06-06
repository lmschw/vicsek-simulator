import math
import numpy as np

def determineMinMaxAngleOfVision(orientation, degreesOfVision):
    angularDistance = degreesOfVision / 2
    currentAngle = normaliseDegreesAngle(computeCurrentAngle(orientation))
    
    minAngle = normaliseDegreesAngle(currentAngle - angularDistance)
    maxAngle = normaliseDegreesAngle(currentAngle + angularDistance)

    return minAngle, maxAngle

def isInFieldOfVision(positionParticle, positionCandidate, minAngle, maxAngle):
    if positionCandidate[0] == positionParticle[0] and positionParticle[1] == positionCandidate[1]:
        return True
    orientationFromOrigin = positionCandidate - positionParticle
    angleRadian = np.arctan(orientationFromOrigin[1]/orientationFromOrigin[0])
    angle = normaliseDegreesAngle(math.degrees(angleRadian))
    if minAngle < maxAngle:
        isIn = angle >= minAngle and angle <= maxAngle
    else:
        isIn = angle >= minAngle or angle <= maxAngle
    return isIn

def isParticleOccluded(particleIdx, otherIdx, positions, candidates, epsilon=1):
    if particleIdx == otherIdx:
        return False
    isOccluded = False
    if len(candidates) > 0:
        for candidateIdx in candidates[0]:
            if candidateIdx != particleIdx and candidateIdx != otherIdx:
                isOccluded = isOccluded or isCOccludingB(positions[particleIdx], positions[otherIdx], positions[candidateIdx], epsilon)
    return isOccluded

def isCOccludingB(a, b, c, epsilon=1):
    return isCollinear(a, b, c, epsilon) and isCBetweenAB(a, b, c)


def isCollinear(a, b, c, epsilon=1):
    return np.absolute((a[1] - b[1]) * (a[0] - c[0]) - (a[1] - c[1]) * (a[0] - b[0])) <= epsilon

def isCBetweenAB(a, b, c):
    isBetweenX = a[0] <= c[0] <= b[0] or a[0] >= c[0] >= b[0]
    isBetweenY = a[1] <= c[1] <= b[1] or a[1] >= c[1] >= b[1]
    return isBetweenX and isBetweenY


def computeCurrentAngle(orientation):
    # determine the current angle
    previousU = orientation[0]
    return np.arccos(previousU) * 180 / np.pi

def computeUvCoordinates(angle):
    # compute the uv-coordinates
    U = np.cos(angle*np.pi/180)
    V = np.sin(angle*np.pi/180)
    
    return [U,V]

def normaliseDegreesAngle(angle):
    if angle < 0:
        return 360 - abs(angle)
    if angle > 360:
        return angle % 360
    return angle