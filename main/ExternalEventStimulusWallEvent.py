import numpy as np

import ServiceVicsekHelper

class ExternalEventStimulusWallEvent(object):
    def __init__(self, startTimestep, endTimestep, wallTypeBehaviour, noise=None, turnBy=0.3):
        """
        Creates an external stimulus event that affects part of the swarm at a given timestep.

        Params:
            - startTimestep (int): the first timestep at which the stimulus is presented and affects the swarm
            - endTimestep (int): the last timestep at which the stimulus is presented and affects the swarm

        Returns:
            No return.
        """
        self.startTimestep = startTimestep
        self.endTimestep = endTimestep
        self.wallTypeBehaviour = wallTypeBehaviour
        self.noise = noise
        self.turnBy = turnBy

    def getParameterSummary(self):
        summary = {
            "startTimestep": self.startTimestep,
            "endTimestep": self.endTimestep,
            "wallTypeBehaviour": self.wallTypeBehaviour
            }
        return summary
    
    def check(self, currentTimestep, positions, orientations, speed, dt):
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
        if self.checkTimestep(currentTimestep):
            orientations = self.executeEvent(positions, orientations, speed, dt)
        return orientations

    def checkTimestep(self, currentTimestep):
        """
        Checks if the event should be triggered.

        Params:
            - currentTimestep (int): the timestep within the experiment run to see if the event should be triggered

        Returns:
            A boolean representing whether or not the event should be triggered.
        """
        return self.startTimestep <= currentTimestep and currentTimestep <= self.endTimestep

    def executeEvent(self, positions, orientations, speed, dt):
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
        for idx in range(len(positions)):
            if self.wallTypeBehaviour.checkClosenessToBorder(positions[idx]):
                orientations[idx] = self.__applyNoiseDistribution(self.wallTypeBehaviour.getAvoidanceOrientation(positions[idx], orientations[idx], speed, dt, self.turnBy))
        orientations = ServiceVicsekHelper.normalizeOrientations(orientations)
        return orientations
    
    def __applyNoiseDistribution(self, orientation):
        if self.noise == None:
            return orientation
        return orientation + np.random.normal(scale=self.noise, size=(1, 2))
