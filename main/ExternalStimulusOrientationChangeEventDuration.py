import random
import math
import numpy as np
from heapq import nsmallest

import ExternalStimulusOrientationChangeEvent

from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumMovementPattern import MovementPattern

import DefaultValues as dv
import ServiceMetric
import ServiceVicsekHelper
import ServiceOrientations

class ExternalStimulusOrientationChangeEventDuration(ExternalStimulusOrientationChangeEvent.ExternalStimulusOrientationChangeEvent):
    """
    Representation of an event occurring for a specified duration with a specified movement behaviour within the domain and 
    affecting a specified percentage of particles. After creation, the check()-method takes care of everything.
    """
    def __init__(self, startTimestep, endTimestep, percentage, angle, eventEffect, movementPattern, movementSpeed, perceptionRadius=30, distributionType=DistributionType.GLOBAL, areas=None, orientation=[0,0], domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, targetSwitchValue=None):
        """
        Creates an external stimulus event that affects part of the swarm at a given timestep.

        Params:
            - timestep (int): the timestep at which the stimulus is presented and affects the swarm
            - percentage (float, range: 0-100): how many percent of the swarm is directly affected by the event
            - angle (int, range: 1-359): how much the orientation of the affected particles is changed in a counterclockwise manner
            - eventEffect (EnumEventEffect): how the orientations should be affected
            - distributionType (EnumDistributionType) [optional]: how the directly affected particles are distributed, i.e. if the event occurs globally or locally
            - areas ([(centerXCoordinate, centerYCoordinate, radius)]) [optional]: list of areas in which the event takes effect. Should be specified if the distributionType is not GLOBAL and match the DistributionType

        Returns:
            No return.
        """
        super().__init__(startTimestep, percentage, angle, eventEffect, distributionType, areas, domainSize, targetSwitchValue)        
        self.startTimestep = startTimestep
        self.endTimestep = endTimestep
        self.movementPattern = movementPattern
        self.movementSpeed = movementSpeed
        self.orientation = orientation
        self.startArea = areas

        if self.distributionType == DistributionType.GLOBAL and self.movementPattern != MovementPattern.STATIC:
            raise Exception("Movement is not possible for global effects")
        
    def getShortPrintVersion(self):
        return f"t{self.startTimestep}-{self.endTimestep}e{self.eventEffect.val}m{self.movementPattern.val}p{self.percentage}a{self.angle}dt{self.distributionType.value}a{self.startArea}"

    def check(self, totalNumberOfParticles, currentTimestep, positions, orientations, switchValues, cells, cellDims, cellToParticleDistribution):
        """
        Checks if the event is triggered at the current timestep and executes it if relevant.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (u,v)): the orientation of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - neighbouringCells (dictionary {cellIdx: array of indices of neighbouring cells}): A dictionary of all neighbouring cells for every cell
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            The orientations of all particles - altered if the event has taken place, unaltered otherwise.
        """
        selectedIndices = []
        if self.checkTimestep(currentTimestep):
            if self.movementPattern != MovementPattern.STATIC:
                self.updateAreas(positions, cells, cellDims, cellToParticleDistribution)
            #print(f"executing event at timestep {currentTimestep}")
            orientations, switchValues, selectedIndices = self.executeEvent(totalNumberOfParticles, positions, orientations, switchValues, cells, cellDims, cellToParticleDistribution)
        if self.distributionType == DistributionType.GLOBAL:
            position = [self.domainSize[0]/2, self.domainSize[1]/2]
        else:
            position = [self.areas[0][0], self.areas[0][1]]
        return orientations, switchValues, selectedIndices, position, self.orientation

    def checkTimestep(self, currentTimestep):
        """
        Checks if the event should be triggered.

        Params:
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered

        Returns:
            A boolean representing whether or not the event should be triggered.
        """
        return self.startTimestep <= currentTimestep and currentTimestep <= self.endTimestep
    
    def updateAreas(self, positions, orientations, cells, cellDims, cellToParticleDistribution):
        initialPosition = [self.areas[0][0], self.areas[0][1]]
        match self.movementPattern:
            case MovementPattern.STATIC:
                position = initialPosition
                orientation = self.orientation
            case MovementPattern.RANDOM:
                chosenAngle = random.random() * 360
                orientation = ServiceOrientations.computeUvCoordinates(chosenAngle)
                position = self.__computeNewPosition(initialPosition, orientation)
            case MovementPattern.PURSUIT_NEAREST:
                candidates = self.determineCandidates(positions, orientations, cells, cellDims, cellToParticleDistribution)
                candidateDistances = {candidateIdx: math.dist(initialPosition, positions[candidateIdx]) for candidateIdx in candidates}
                pickedNeighbours = nsmallest(1, candidateDistances, candidateDistances.get)
                if len(pickedNeighbours) >= 1:
                    pickedNeighbour = pickedNeighbours[0] # nsmallest always returns a list
                    orientation = self.computeAwayFromOrigin(positions[pickedNeighbour])
                    position = self.__computeNewPosition(initialPosition, orientation)
                else:
                    position = initialPosition
                    orientation = self.orientation
        self.areas = [(position[0], position[1], self.areas[0][2])]
        self.orientation = orientation

    def __computeNewPosition(self, initialPosition, orientation):
        change = (self.movementSpeed*orientation)
        position = [initialPosition[0] + change[0], initialPosition[1] + change[1]]
        position += -self.domainSize*np.floor(position/self.domainSize)
        return position