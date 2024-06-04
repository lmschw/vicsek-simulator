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