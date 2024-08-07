import numpy as np

from EnumWallInfluenceType import WallInfluenceType

import ServiceMetric
import ServiceOrientations


class WallType(object):
    def __init__(self, name, wallInfluenceType, influenceDistance=None, focusPoint=[None, None], radius=None, cornerPoints=[None], areParticlesWithinWall=True):
        self.name = name
        self.wallInfluenceType = wallInfluenceType
        self.influenceDistance = influenceDistance
        self.focusPoint = focusPoint
        self.radius = radius
        self.cornerPoints = cornerPoints
        self.areParticlesWithinWall = areParticlesWithinWall

        self.checkCompleteness()

    def checkClosenessToBorder(self, position):
        isInside = self.isInsideOfWalls(position)
        if (isInside == True and self.areParticlesWithinWall == False) or (isInside == False and self.areParticlesWithinWall == True):
            return False # we don't consider those, so they are not close to the wall for the current purposes
        match(self.wallInfluenceType):
            case WallInfluenceType.FULL_AREA:
                return isInside
            case WallInfluenceType.EXCEPT_NEAR_BORDER:
                return self.getDistanceFromBorder(position) >= self.influenceDistance
            case WallInfluenceType.CLOSE_TO_BORDER:
                return self.getDistanceFromBorder(position) <= self.influenceDistance
        
    def isInsideOfWalls(self, position):
        pass

    def getDistanceFromBorder(self, position):
        pass

    def getAvoidanceOrientation(self, orientation):
        pass

    def checkCompleteness(self):
        hasFocusPoint = not self.__isPointOrListNull(self.focusPoint)
        hasCornerPoints = not self.__isPointOrListNull(self.cornerPoints)

        if self.wallInfluenceType != WallInfluenceType.FULL_AREA and self.influenceDistance == None:
            raise Exception("If the wall event does not affect all particles within that area, an influenceDistance needs to be specified.")
        if hasFocusPoint and self.radius == None or self.radius != None and not hasFocusPoint:
            raise Exception("If a focus point or radius is supplied, so must the other value be.")
        if hasCornerPoints and (self.radius != None or hasFocusPoint):
            raise Exception("If corner points are provided, radius and focus point may not be supplied.")

    def __isPointOrListNull(self, pointOrList):
        return any(ele is None for ele in pointOrList)
    

class WallTypeCircle(WallType):
    def __init__(self, name, wallInfluenceType, focusPoint, radius, influenceDistance=None):
        super().__init__(name=name, wallInfluenceType=wallInfluenceType, influenceDistance=influenceDistance, focusPoint=focusPoint, radius=radius)
    
    def isInsideOfWalls(self, position):
        return ((self.focusPoint[0] - position[0])**2 + (self.focusPoint[1] - position[1])**2) <= self.radius **2 

    def getDistanceFromBorder(self, position):
        return np.absolute((((self.focusPoint[0] - position[0])**2 + (self.focusPoint[1] - position[1])** 2)**(1/2)) - self.radius)
    
    def getAvoidanceOrientation(self, position, orientation, speed, dt):
        if self.wallInfluenceType != WallInfluenceType.FULL_AREA and self.getDistanceFromBorder(position) >= self.influenceDistance:
            return orientation
        
        closestPointOnCircle = self.getClosestPointToCircle(position)
        angleToClosestPoint = ServiceMetric.angleBetweenTwoVectors(closestPointOnCircle, position)
        angleOrientation = ServiceOrientations.computeAngleForOrientation(orientation)
        if angleOrientation > angleToClosestPoint:
            return ServiceOrientations.computeUvCoordinates(self.getAngleToAvoidCollision(position, speed, dt, minAngle=angleOrientation))
        return ServiceOrientations.computeUvCoordinates(self.getAngleToAvoidCollision(position, speed, dt, maxAngle=angleOrientation))

    def getClosestPointToCircle(self, position):
        vX = position[0] - self.focusPoint[0]
        vY = position[1] - self.focusPoint[1]
        magV = np.sqrt(vX*vX + vY*vY)
        aX = self.focusPoint[0] + vX / magV * self.radius
        aY = self.focusPoint[1] + vY / magV * self.radius 
        return [aX, aY]
    
    def getAngleToAvoidCollision(self, position, speed, dt, minAngle=None, maxAngle=None, turnBy=0.3):
        if maxAngle:
            angle = maxAngle
        else:
            angle = minAngle
        turns = (2*np.pi) / turnBy
        turn = 0
        orientation = ServiceOrientations.computeUvCoordinates(angle)
        willCollide = self.__willCollide(position, orientation, dt, speed)
        while willCollide and turn <= turns:
            if maxAngle:
                angle = self.__turnAngle(angle, maxAngle, turnBy=turnBy)
            else:
                angle = self.__turnAngle(angle, turnBy=turnBy)
            orientation = ServiceOrientations.computeUvCoordinates(angle)
            willCollide = self.__willCollide(position, orientation, dt, speed)
            turn += 1
        if willCollide:
            angle = minAngle + np.pi
        return angle
    
    def __turnAngle(self, angle, maxAngle=None, turnBy=0.03):
        if maxAngle != None:
            return angle - turnBy
        return angle + turnBy
    
    def __willCollide(self, position, orientation, dt, speed):
        do = [dt*speed*o for o in orientation]
        newPos = [position[0] + do[0], position[1] + do[1]]
        return not ((self.isInsideOfWalls(position) and self.isInsideOfWalls(newPos)) or (self.isInsideOfWalls(position) == False and self.isInsideOfWalls(newPos) == False))


class WallTypeRectangle(WallType):
    def __init__(self, name, wallInfluenceType, minPoint, maxPoint, influenceDistance=None):
        super().__init__(name=name, wallInfluenceType=wallInfluenceType, influenceDistance=influenceDistance, cornerPoints=[minPoint, [minPoint[0], maxPoint[1]], [maxPoint[0], minPoint[1]], maxPoint])
        self.minPoint = minPoint
        self.maxPoint = maxPoint

    def isInsideOfWalls(self, position):
        return position[0] >= self.minPoint[0] and position[0] <= self.maxPoint[0] and position[1] >= self.minPoint[1] and position[1] <= self.maxPoint[1]

    def onBorder(self, position):
        onLower = position[0] == self.minPoint[0] and position[1] >= self.minPoint[1] and position[1] <= self.maxPoint[1]
        onUpper = position[0] == self.maxPoint[0] and position[1] >= self.minPoint[1] and position[1] <= self.maxPoint[1]
        onLeft = position[1] == self.minPoint[1] and position[0] >= self.minPoint[0] and position[0] <= self.maxPoint[0]
        onRight = position[1] == self.maxPoint[1] and position[0] >= self.minPoint[0] and position[0] <= self.maxPoint[0]
        return onLower or onUpper or onLeft or onRight

    def getDistanceFromBorder(self, position):
        """
        dx = max(self.minPoint[0] - position[0], 0, position[0] - self.maxPoint[0])
        dy = max(self.minPoint[1] - position[1], 0, position[1] - self.maxPoint[1])
        return math.sqrt(dx*dx + dy*dy)

        """
        if self.onBorder(position):
            return 0
        dx = min(np.absolute(self.minPoint[0]-position[0]), np.absolute(self.maxPoint[0]-position[0]))
        dy = min(np.absolute(self.minPoint[1]-position[1]), np.absolute(self.maxPoint[1]-position[1]))
        if dx == 0:
            return dy
        elif dy == 0:
            return dx
        return min(dx, dy)
    
    # TODO add implementation for getAvoidanceOrientation()
    def getAvoidanceOrientation(self, position, orientation, speed, dt):
        pass

"""
circle = WallTypeCircle(name="circle", wallInfluenceType=WallInfluenceType.CLOSE_TO_BORDER, influenceDistance=5, focusPoint=[0,0], radius=10)
rect = WallTypeRectangle(name="rect", wallInfluenceType=WallInfluenceType.CLOSE_TO_BORDER, influenceDistance=5, minPoint=[0,0], maxPoint=[4,5])
"""

"""
circle = WallTypeCircle(name="circle", wallInfluenceType=WallInfluenceType.CLOSE_TO_BORDER, influenceDistance=50, focusPoint=[0,0], radius=100)
position = [1, -98]
orientation = ServiceOrientations.computeUvCoordinates(3*np.pi/2)
print(ServiceOrientations.computeAngleForOrientation(orientation))
print(ServiceOrientations.computeAngleForOrientation(circle.getAvoidanceOrientation(position, orientation, 1, 2)))
"""