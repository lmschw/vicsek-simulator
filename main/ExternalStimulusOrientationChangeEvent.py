import random
import math
import numpy as np

from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect

import DefaultValues as dv
import ServiceVicsekHelper
import ServiceOrientations

class ExternalStimulusOrientationChangeEvent:
    # TODO refactor to allow areas with a radius bigger than the radius of a particle, i.e. remove neighbourCells and determine all affected cells here
    """
    Representation of an event occurring at a specified time and place within the domain and affecting 
    a specified percentage of particles. After creation, the check()-method takes care of everything.
    """
    def __init__(self, timestep, percentage, angle, eventEffect, distributionType=DistributionType.GLOBAL, areas=None, 
                 domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, targetSwitchValue=None):
        """
        Creates an external stimulus event that affects part of the swarm at a given timestep.

        Params:
            - timestep (int): the timestep at which the stimulus is presented and affects the swarm
            - percentage (float, range: 0-100): how many percent of the swarm is directly affected by the event
            - angle (int, range: 1-359): how much the orientation of the affected particles is changed in a counterclockwise manner
            - eventEffect (EnumEventEffect): how the orientations should be affected
            - distributionType (EnumDistributionType) [optional]: how the directly affected particles are distributed, i.e. if the event occurs globally or locally
            - areas ([(centerXCoordinate, centerYCoordinate, radius)]) [optional]: list of areas in which the event takes effect. Should be specified if the distributionType is not GLOBAL and match the DistributionType
            - domainSize (tuple of floats) [optional]: the size of the domain
            - targetSwitchValue (switchTypeValue) [optional]: the value that every affected particle should select
            
        Returns:
            No return.
        """
        self.timestep = timestep
        self.percentage = percentage
        self.angle = angle
        self.eventEffect = eventEffect
        self.distributionType = distributionType
        self.areas = areas
        self.domainSize = np.asarray(domainSize)
        self.targetSwitchValue = targetSwitchValue

        if self.distributionType != DistributionType.GLOBAL and self.areas == None:
            raise Exception("Local effects require the area to be specified")
        
    def getShortPrintVersion(self):
        return f"t{self.timestep}e{self.eventEffect.val}p{self.percentage}a{self.angle}dt{self.distributionType.value}a{self.areas}"

    def check(self, totalNumberOfParticles, currentTimestep, positions, orientations, switchValues, cells, cellDims, cellToParticleDistribution):
        """
        Checks if the event is triggered at the current timestep and executes it if relevant.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (u,v)): the orientation of every particle in the domain at the current timestep
            - switchValues (array of switchTypeValues): the switch type value of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - cellDims (tuple of floats): the dimensions of a cell (the same for all cells)
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            The orientations of all particles - altered if the event has taken place, unaltered otherwise.
        """
        selectedIndices = []
        if self.checkTimestep(currentTimestep):
            print(f"executing event at timestep {currentTimestep}")
            orientations, switchValues, selectedIndices = self.executeEvent(totalNumberOfParticles, positions, orientations, switchValues, cells, cellDims, cellToParticleDistribution)
        return orientations, switchValues, selectedIndices

    def checkTimestep(self, currentTimestep):
        """
        Checks if the event should be triggered.

        Params:
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered

        Returns:
            A boolean representing whether or not the event should be triggered.
        """
        return self.timestep == currentTimestep
    
    def executeEvent(self, totalNumberOfParticles, positions, orientations, switchValues, cells, cellDims, cellToParticleDistribution):
        """
        Executes the event.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (u,v)): the orientation of every particle in the domain at the current timestep
            - switchValues (array of switchTypeValues): the switch type value of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - cellDims (tuple of floats): the dimensions of a cell (the same for all cells)
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            The orientations, switchTypeValues of all particles after the event has been executed as well as a list containing the indices of all affected particles.
        """
        selectedIndices = self.__determineAffectedParticles(totalNumberOfParticles, positions,  orientations, cells, cellDims, cellToParticleDistribution)
        alteredIndices = []
        for idx in selectedIndices:
            match self.eventEffect:
                case EventEffect.TURN_BY_FIXED_ANGLE:
                    orientations[idx] = self.__computeFixedAngleTurn(orientations[idx])
                case EventEffect.ALIGN_TO_FIXED_ANGLE:
                    orientations[idx] = ServiceOrientations.computeUvCoordinates(self.angle)
                case EventEffect.ALIGN_TO_FIRST_PARTICLE:
                    orientations[idx] = orientations[selectedIndices[0]]
                case EventEffect.AWAY_FROM_ORIGIN:
                    orientations[idx] = self.computeAwayFromOrigin(positions[idx])
                case EventEffect.TOWARDS_ORIGIN:
                    orientations[idx] = self.__computeTowardsOrigin(positions[idx])
                case EventEffect.RANDOM:
                    orientations[idx] = self.__getRandomOrientation()
            if self.targetSwitchValue != None:
                switchValues[idx] = self.targetSwitchValue
                alteredIndices.append(idx)

        return orientations, switchValues, alteredIndices

    def __determineAffectedParticles(self, totalNumberOfParticles, positions, orientations, cells, cellDims, cellToParticleDistribution):
        """
        Determines which particles should be affected by the event.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (x,y)): the orientation of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - cellDims (tuple of floats): the dimensions of a cell (the same for all cells)
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            An array of the indices of the affected particles.
        """
        # determine which particles might potentially be affected
        candidateIndices = self.determineCandidates(positions, orientations, cells, cellDims, cellToParticleDistribution)
        
        # how many particles will be affected
        numberOfAffectedParticles = math.ceil((self.percentage / 100) * totalNumberOfParticles)
        if numberOfAffectedParticles > len(candidateIndices):
            numberOfAffectedParticles = len(candidateIndices) # can't affect particles that don't exist
        
        # select the particle for the event to affect
        return random.sample(candidateIndices, numberOfAffectedParticles)
        

    def determineCandidates(self, positions, orientations, cells, cellDims, cellToParticleDistribution):
        """
        Determines which particles could potentially be affected based on the distributionType and the areas if relevant.

        Params:
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (x,y)): the orientation of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - cellDims (tuple of floats): the dimensions of a cell (the same for all cells)
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            An array of the indices of all particles that could potentially be affected by the event.
        """
        match self.distributionType:
            case DistributionType.GLOBAL:
                candidates = range(len(positions))
            case _: # all other options are local and can be handled in the same way
                candidateIndices = []
                for area in self.areas:
                        cellsToCheck = self.findCells(area, cells, cellDims)
                        for cellToCheck in cellsToCheck:
                            for particleIdx in cellToParticleDistribution[cellToCheck]:
                                if ((area[0] - positions[particleIdx][0])**2 + (area[1] - positions[particleIdx][1])**2) <= area[2] **2:
                                    candidateIndices.append(particleIdx)
                candidates = list(set(candidateIndices))
        return candidates

    def __findCell(self, area, cells):
        """
        Finds the cell of the centre point of the area.

        Params:
            - area ((centerX, centerY, radius)): The affected area.
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain

        Returns:
            The index of the cell containing the centre point of the area.
        """
        for cellIdx, cell in enumerate(cells):
            if cell[0][0] <= area[0] and cell[0][1] <= area[1] and cell[1][0] >= area[0] and cell[1][1] >= area[1]:
                targetCell = cellIdx
                break
        return targetCell
    
    def findCells(self, area, cells, cellDims):
        """
        Finds the cells that are affected by the event.

        Params:
            - area (array [x, y, radius]): the area affected by the event
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - cellDims (tuple of floats): the dimensions of a cell (the same for all cells)

        Returns:
            A list of the indices of the affected cells.
        """
        areaminx = max(area[0] - area[2], 0) # the radius may be greater than the available space
        areamaxx = min(area[0] + area[2], self.domainSize[0]) # the radius may be greater than the available space
        areaminy = max(area[1] - area[2], 0) # the radius may be greater than the available space
        areamaxy = min(area[1] + area[2], self.domainSize[1]) # the radius may be greater than the available space

        for cellidx, cell in enumerate(cells):
            xmin = cell[0][0]
            xmax = cell[1][0]
            ymin = cell[0][1]
            ymax = cell[1][1]

            if xmin <= areaminx and xmax > areaminx and area[1] >= ymin and area[1] <= ymax:
                left = cellidx
            if xmin < areamaxx and xmax >= areamaxx and area[1] >= ymin and area[1] <= ymax:
                right = cellidx
            if ymin <= areaminy and ymax > areaminy and area[0] >= xmin and area[0] <= xmax:
                upper = cellidx
            if ymin < areamaxy and ymax >= areamaxy and area[0] >= xmin and area[0] <= xmax:
                lower = cellidx

        colLeft = math.floor(left / cellDims[1])
        colRight = math.floor(right / cellDims[1])
        rowUpper = (upper % cellDims[1])
        rowLower = (lower % cellDims[1])

        affectedCells = []
        for cellidx, cell in enumerate(cells):
            if (cellidx / cellDims[1]) >= (colLeft-1)  and (cellidx / cellDims[1]) <= (colRight+1) and (cellidx % cellDims[1]) >= (rowUpper-1) and (cellidx % cellDims[1]) <= (rowLower+1):
                affectedCells.append(cellidx)

        return affectedCells

    def __computeFixedAngleTurn(self, orientation):
        """
        Determines the new uv-coordinates after turning the particle by the specified angle.
        The new angle is the equivalent of the old angle plus the angle specified by the event.

        Params:
            orientation ([U,V]): the current orientation of a single particle
        
        Returns:
            The new uv-coordinates for the orientation of the particle.
        """
        previousAngle = ServiceOrientations.computeCurrentAngle(orientation)

        # add the event angle to the current angle
        newAngle = (previousAngle + self.angle) % 360

        return ServiceOrientations.computeUvCoordinates(newAngle)
    
    def computeAwayFromOrigin(self, position):
        """
        Computes the (u,v)-coordinates for the orientation after turning away from the point of origin.

        Params:
            - position ([X,Y]): the position of the current particle that should turn away from the point of origin

        Returns:
            [U,V]-coordinates representing the new orientation of the current particle.
        """
        angle = self.__computeAngleWithRegardToOrigin(position)
        if (position[0] < self.getOriginPoint()[0]):
            angle += 180
        return ServiceOrientations.computeUvCoordinates(angle)

    def __computeTowardsOrigin(self, position):
        """
        Computes the (u,v)-coordinates for the orientation after turning towards the point of origin.

        Params:
            - position ([X,Y]): the position of the current particle that should turn towards the point of origin

        Returns:
            [U,V]-coordinates representing the new orientation of the current particle.
        """
        angle = self.__computeAngleWithRegardToOrigin(position)
        if (position[0] > self.getOriginPoint()[0]):
            angle += 180
        return ServiceOrientations.computeUvCoordinates(angle)

    def __computeAngleWithRegardToOrigin(self, position):
        """
        Computes the angle between the position of the current particle and the point of origin of the event.

        Params:
            - position ([X,Y]): the position of the current particle that should turn towards the point of origin

        Returns:
            The angle in degrees between the two points.
        """
        orientationFromOrigin = position - self.getOriginPoint()
        angleRadian = np.arctan(orientationFromOrigin[1]/orientationFromOrigin[0])
        return math.degrees(angleRadian)

    def getOriginPoint(self):
        """
        Determines the point of origin of the event.

        Returns:
            The point of origin of the event in [X,Y]-coordinates.
        """
        match self.distributionType:
            case DistributionType.GLOBAL:
                origin = (self.domainSize[0]/2, self.domainSize[1]/2)
            case DistributionType.LOCAL_SINGLE_SITE:
                origin = self.areas[0][:2]
        return origin


    def __getRandomOrientation(self):
        """
        Selects a random orientation.

        Returns:
            A random orientation in [U,V]-coordinates.
        """
        return ServiceVicsekHelper.normalizeOrientations(np.random.rand(1, len(self.domainSize))-0.5)
