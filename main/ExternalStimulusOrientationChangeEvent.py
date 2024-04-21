import random
import math
import numpy as np

from EnumDistributionType import DistributionType

class ExternalStimulusOrientationChangeEvent:
    # TODO refactor to allow areas with a radius bigger than the radius of a particle, i.e. remove neighbourCells and determine all affected cells here
    """
    Representation of an event occurring at a specified time and place within the domain and affecting 
    a specified percentage of particles. After creation, the check()-method takes care of everything.
    """
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
        if self.checkTimestep(currentTimestep):
            orientations = self.executeEvent(totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution)
        return orientations

    def checkTimestep(self, currentTimestep):
        """
        Checks if the event should be triggered.

        Params:
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered

        Returns:
            A boolean representing whether or not the event should be triggered.
        """
        return self.timestep == currentTimestep
    
    def executeEvent(self, totalNumberOfParticles, positions, orientations, cells, neighbouringCells, cellToParticleDistribution):
        """
        Executed the event.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - orientations (array of tuples (u,v)): the orientation of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - neighbouringCells (dictionary {cellIdx: array of indices of neighbouring cells}): A dictionary of all neighbouring cells for every cell
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            The orientations of all particles after the event has been executed.
        """
        selectedIndices = self.__determineAffectedParticles(totalNumberOfParticles, positions, cells, neighbouringCells, cellToParticleDistribution)
        for idx in selectedIndices:
            orientations[idx] = self.__computeNewOrientation(orientations[idx])
        return orientations

    def __determineAffectedParticles(self, totalNumberOfParticles, positions, cells, neighbouringCells, cellToParticleDistribution):
        """
        Determines which particles should be affected by the event.

        Params:
            - totalNumberOfParticles (int): the total number of particles within the domain. Used to compute the number of affected particles
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - neighbouringCells (dictionary {cellIdx: array of indices of neighbouring cells}): A dictionary of all neighbouring cells for every cell
            - cellToParticleDistribution (dictionary {cellIdx: array of indices of all particles within the cell}): A dictionary containing the indices of all particles within each cell

        Returns:
            An array of the indices of the affected particles.
        """
        # determine which particles might potentially be affected
        candidateIndices = self.__determineCandidates(positions, cells, neighbouringCells, cellToParticleDistribution)
        
        # how many particles will be affected
        numberOfAffectedParticles = math.ceil((self.percentage / 100) * totalNumberOfParticles)
        if numberOfAffectedParticles > len(candidateIndices):
            numberOfAffectedParticles = len(candidateIndices) # can't affect particles that don't exist
        
        # select the particle for the event to affect
        return random.sample(candidateIndices, numberOfAffectedParticles)
        

    def __determineCandidates(self, positions, cells, neighbouringCells, cellToParticleDistribution):
        """
        Determines which particles could potentially be affected based on the distributionType and the areas if relevant.

        Params:
            - positions (array of tuples (x,y)): the position of every particle in the domain at the current timestep
            - cells (array: [(minX, minY), (maxX, maxY)]): the cells within the cellbased domain
            - neighbouringCells (dictionary {cellIdx: array of indices of neighbouring cells}): A dictionary of all neighbouring cells for every cell
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
                    cellIdx = self.__findCell(area, cells)
                    for cellToCheck in neighbouringCells[cellIdx]:
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
    
    def __computeNewOrientation(self, orientation):
        """
        Determines the new uv-coordinates after turning the particle by the specified angle.
        The new angle is the equivalent of the old angle plus the angle specified by the event.

        Params:
            orientation ([U,V]): the current orientation of a single particle
        
        Returns:
            The new uv-coordinates for the orientation of the particle.
        """
        # determine the current angle
        previousU = orientation[0]
        previousAngle = np.arccos(previousU) * 180 / np.pi

        # add the event angle to the current angle
        newAngle = (previousAngle + self.angle) % 360

        # compute the uv-coordinates
        U = np.cos(newAngle*np.pi/180)
        V = np.sin(newAngle*np.pi/180)
        
        return [U,V]

