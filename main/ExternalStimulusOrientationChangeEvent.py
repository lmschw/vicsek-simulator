import random
import math
import numpy as np

from EnumDistributionType import DistributionType

class ExternalStimulusOrientationChangeEvent:
    def __init__(self, timestep, percentage, angle, distributionType=DistributionType.GLOBAL, areas=None):
        """
        Creates an external stimulus event that affects part of the swarm at a given timestep.

        Params:
            - timestep (int): the timestep at which the stimulus is presented and affects the swarm
            - percentage (float, range: 0-100): how many percent of the swarm is directly affected by the event
            - angle (int, range: 1-359): how much the orientation of the affected particles is changed in a counterclockwise manner
            - distributionType (EnumDistributionType) [optional]: how the directly affected particles are distributed, i.e. if the event occurs globally or locally
            - areas ([(centerXCoordinate, centerYCoordinate, radius)]) [optional]: list of areas in which the event takes effect. Should be specified if the distributionType is not GLOBAL and match the DistributionType

        Returns:
            No return.
        """
        self.timestep = timestep
        self.percentage = percentage
        self.angle = angle
        self.distributionType = distributionType
        self.areas = areas

        if self.distributionType != DistributionType.GLOBAL and self.areas == None:
            raise Exception("Local effects require the area to be specified")
        
    def getShortPrintVersion(self):
        return f"t{self.timestep}p{self.percentage}a{self.angle}dt{self.distributionType.value}a{self.areas}"


    def check(self, totalNumberOfParticles, currentTimestep, positions, orientations, cells, neighbouringCells, cellToParticleDistribution):
        if self.checkTimestep(currentTimestep):
            orientations =self.executeEvent(totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution)
        return orientations

    def checkTimestep(self, currentTimestep):
        return self.timestep == currentTimestep
    
    def executeEvent(self, totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution):
        selectedIndices = self.__determineAffectedParticles(totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution)
        for idx in selectedIndices:
            orientations[idx] = self.__computeNewOrientation(orientations[idx])
        return orientations

    def __determineAffectedParticles(self, totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution):
        # determine which particles might potentially be affected
        candidateIndices = self.__determineCandidates(positions, cells, neighbouringCells, cellToParticleDistribution)
        
        # how many particles will be affected
        numberOfAffectedParticles = math.ceil((self.percentage / 100) * totalNumberOfParticles)
        if numberOfAffectedParticles > len(candidateIndices):
            numberOfAffectedParticles = len(candidateIndices) # can't affect particles that don't exist
        
        # select the particle for the event to affect
        return random.sample(candidateIndices, numberOfAffectedParticles)
        

    def __determineCandidates(self, positions, cells, neighbouringCells, cellToParticleDistribution):
        match self.distributionType:
            case DistributionType.GLOBAL:
                candidates = range(len(positions))
            case _: # all other options are local and can be handled in the same way
                candidateIndices = []
                for area in self.areas:
                    cellIdx = self.__findCell(area, cells)
                    for cellToCheck in neighbouringCells[cellIdx]:
                        for particleIdx in cellToParticleDistribution[cellToCheck]:
                            if ((area[0] - positions[particleIdx][0])**2 + (area[1] - positions[particleIdx][1])**2) <= area[2] **2:
                                candidateIndices.append(particleIdx)
                candidates = list(set(candidateIndices))
        return candidates



    def __findCell(self, area, cells):
        for cellIdx, cell in enumerate(cells):
            if cell[0][0] <= area[0] and cell[0][1] <= area[1] and cell[1][0] >= area[0] and cell[1][1] >= area[1]:
                targetCell = cellIdx
                break
        return targetCell
    
    def __computeNewOrientation(self, orientation):
        previousU = orientation[0]
        previousAngle = np.arccos(previousU) * 180 / np.pi
        newAngle = (previousAngle + self.angle) % 360
        U = np.cos(newAngle*np.pi/180)
        V = np.sin(newAngle*np.pi/180)
        return [U,V]

