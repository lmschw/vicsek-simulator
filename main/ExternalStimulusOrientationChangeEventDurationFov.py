import random
import math
import numpy as np
from heapq import nsmallest

import ExternalStimulusOrientationChangeEventDuration

from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumMovementPattern import MovementPattern

import DefaultValues as dv
import ServiceMetric
import ServiceVicsekHelper
import ServiceOrientations

"""
Modified version of ExternalStimulusOrientationChangeEventDuration allowing limitation of the field of vision.
"""

class ExternalStimulusOrientationChangeEventDurationFov(ExternalStimulusOrientationChangeEventDuration.ExternalStimulusOrientationChangeEventDuration):
    """
    Representation of an event occurring for a specified duration with a specified movement behaviour within the domain and 
    affecting a specified percentage of particles. After creation, the check()-method takes care of everything.
    """
    def __init__(self, startTimestep, endTimestep, percentage, angle, eventEffect, movementPattern, movementSpeed, 
                 perceptionRadius=30, distributionType=DistributionType.GLOBAL, areas=None, orientation=[0,0], 
                 domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, targetSwitchValue=None, degreesOfVision=360):
        """
        Creates an external stimulus event that affects part of the swarm at a given timestep.

        Params:
            - startTimestep (int): the first timestep at which the stimulus is presented and affects the swarm
            - endTimestep (int): the last timestep at which the stimulus is presented and affects the swarm
            - percentage (float, range: 0-100): how many percent of the swarm is directly affected by the event
            - angle (int, range: 1-359): how much the orientation of the affected particles is changed in a counterclockwise manner
            - eventEffect (EnumEventEffect): how the orientations should be affected
            - movementPattern (EnumMovementPattern): how the point of origin of the event moves during the duration of the event
            - movementSpeed (int): the speed at which the point of origin of the event moves if it moves
            - perceptionRadius (float) [optional]: defines how far the event is able to perceive particles
            - distributionType (EnumDistributionType) [optional]: how the directly affected particles are distributed, i.e. if the event occurs globally or locally
            - areas ([(centerXCoordinate, centerYCoordinate, radius)]) [optional]: list of areas in which the event takes effect. Should be specified if the distributionType is not GLOBAL and match the DistributionType
            - orientation ([u,v]-coordinates) [optional]: the initial orientation of the point of origin
            - domainSize (tuple of floats) [optional]: the size of the domain
            - targetSwitchValue (switchTypeValue) [optional]: the value that every affected particle should select
            - degreesOfVision (float, [0,360]) [optional]: the limitation of the field of vision
            
        Returns:
            No return.
        """
        super().__init__(startTimestep, endTimestep, percentage, angle, eventEffect, movementPattern, movementSpeed, perceptionRadius, distributionType, areas, orientation, domainSize, targetSwitchValue)      
        self.degreesOfVision = degreesOfVision  

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

        visibleCandidates = []
        for cand in candidates:
            minAngle, maxAngle = ServiceOrientations.determineMinMaxAngleOfVision(orientations[cand], self.degreesOfVision)
            # here, the candidate needs to be the central particle because the particle needs to be able to see the point of origin, not the other way round
            if ServiceOrientations.isInFieldOfVision(positions[cand], self.getOriginPoint(), minAngle, maxAngle):
                visibleCandidates.append(cand)
        return visibleCandidates 
 