import numpy as np
import random
import math
from heapq import nlargest
from heapq import nsmallest

import DefaultValues as dv
import EnumNeighbourSelectionMode
from EnumSwitchType import SwitchType
import ServiceMetric

class VicsekWithNeighbourSelection:

    def __init__(self, neighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, 
                 radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, 
                 k=dv.DEFAULT_K_NEIGHBOURS, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE, numCells=dv.DEFAULT_NUM_CELLS, 
                 switchType=None, switchValues=(None, None), orderThresholds=None, numberPreviousStepsForThreshold=10, 
                 switchBlockedAfterEventTimesteps=-1):
        """
        Initialize the model with all its parameters

        Params:
            - neighbourSelectionMode (EnumNeighbourSelectionMode.NeighbourSelectionMode): how the particles select which of the other particles within their perception radius influence their orientation at any given time step
            - domainSize (tuple x,y) [optional]: the size of the domain for the particle movement
            - speed (int) [optional]: how fast the particles move
            - radius (int) [optional]: defines the perception field of the individual particles, i.e. the area in which it can perceive other particles
            - noise (float) [optional]: noise amplitude. adds noise to the orientation adaptation
            - numberOfParticles (int) [optional]: the number of particles within the domain, n
            - k (int) [optional]: the number of neighbours a particle considers when updating its orientation at every time step
            - showExample (bool) [optional]: whether a random example particle should be coloured in red with its influencing neighbours in yellow
            - numCells (int) [optional]: the number of cells that make up the grid for the cellbased evaluation
            - switchType (EnumSwitchType) [optional]: The type of switching that should be performed
            - switchValues (tuple (orderValue, disorderValue)) [optional]: the value that is supposed to create order and the value that is supposed to create disorder.
                    Must be the same type as the switchType
            - orderThresholds (array) [optional]: the difference in local order compared to the previous timesteps that will cause a switch.
                    If only one number is supplied (as an array with one element), will be used to check if the difference between the previous and the current local order is greater than the threshold.
                    If two numbers are supplied, will be used as a lower and an upper threshold that triggers a switch: [lowerThreshold, upperThreshold]
            - numberPreviousStepsForThreshold (int) [optional]: the number of previous timesteps that are considered for the average to be compared to the threshold value(s)

        Returns:
            No return.
        """
        self.neighbourSelectionMode = neighbourSelectionModel
        self.domainSize = np.asarray(domainSize)
        self.speed = speed
        self.radius = radius
        self.noise = noise
        self.numberOfParticles = numberOfParticles
        self.k = k
        self.showExample = showExample
        self.numCells = numCells
        self.switchType = switchType
        self.orderSwitchValue, self.disorderSwitchValue = switchValues
        self.orderThresholds = orderThresholds
        self.numberPreviousStepsForThreshold = numberPreviousStepsForThreshold
        self.switchBlockedAfterEventTimesteps = switchBlockedAfterEventTimesteps
        self.selectedIndices = {}

    def getParameterSummary(self, asString=False):
        """
        Creates a summary of all the model parameters ready for use for conversion to JSON or strings.

        Parameters:
            - asString (bool, default False) [optional]: if the summary should be returned as a dictionary or as a single string
        
        Returns:
            A dictionary or a single string containing all model parameters.
        """
        summary = {"n": self.numberOfParticles,
                    "k": self.k,
                    "noise": self.noise,
                    "speed": self.speed,
                    "radius": self.radius,
                    "neighbourSelectionMode": self.neighbourSelectionMode.name,
                    "domainSize": self.domainSize.tolist(),
                    "tmax": self.tmax,
                    "dt": self.dt}
        if asString:
            strPrep = [tup[0] + ": " + tup[1] for tup in summary.values()]
            return ", ".join(strPrep)
        return summary
    
    
    def calculateMeanOrientations(self, positions, orientations, switchTypeValues, neighbourCandidates):
        """
        Updates the orientations of all particles based on the model parameters.

        Parameters:
            - positions (arr): the positions of all particles at the current timestep
            - orientations (arr): the orientations of all particles at the current timestep

        Returns:
            An array of the adapted orientations.
        """
        """
        rij=positions[:,np.newaxis,:]-positions
    
        rij = rij - self.domainSize*np.rint(rij/self.domainSize) #minimum image convention

        rij2 = np.sum(rij**2,axis=2)
        neighbourCandidates = (rij2 <= self.radius**2)
        """

        neighbours = self.__selectNeighbours(neighbourCandidates, positions, orientations, switchTypeValues)
        summedOrientations = np.sum(neighbours[:,:,np.newaxis]*orientations[np.newaxis,:,:],axis=1)
        return self.__normalizeOrientations(summedOrientations)

    def generateNoise(self):
        """
        Generates noise to dislodge the system from local optima.

        Returns:
            A single noise value.
        """
        return np.random.normal(scale=self.noise, size=(self.numberOfParticles, len(self.domainSize)))

    def simulate(self, initialState=(None, None, None), dt=None, tmax=None, events=None):
        """
        Runs the simulation experiment.
        First the parameters are computed if they are not passed. Then the positions, orientations and colours are computed for each particle at each time step.

        Parameters:
            - initialState (tuple of arrays) [optional]: A tuple containing the initial positions of all particles and their initial orientations
            - dt (int) [optional]: time step
            - tmax (int) [optional]: the total number of time steps of the experiment

        Returns:
            time points, positionsHistory, orientationsHistory, coloursHistory. All of them as ordered arrays so that they can be matched by index matching
        """

        # Preparations and setting of parameters if they are not passed to the method
        positions, orientations, switchTypeValues = initialState
        
        if any(ele is None for ele in initialState):
            positions, orientations, switchTypeValues = self.__initializeState(self.domainSize, self.numberOfParticles)
            
        if dt is None and tmax is not None:
            dt = 1
        
        if tmax is None:
            tmax = (10**3)*dt
            dt = 10**(-2)*(np.max(self.domainSize)/self.speed)

        self.tmax = tmax
        self.dt = dt

        # Initialisations for the loop and the return variables
        t=0
        numIntervals=int(tmax/dt+1)
        
        positionsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        orientationsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))  
        self.localOrderHistory = np.zeros((numIntervals,self.numberOfParticles))        
        switchTypeValuesHistory = numIntervals * [self.numberOfParticles * [None]]
        coloursHistory = numIntervals * [self.numberOfParticles * ['k']]

        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        switchTypeValuesHistory[0]=switchTypeValues


        self.cells = self.initialiseCells()
        self.neighbouringCells = self.determineNeighbouringCells()

        cellToParticleDistribution, particleToCellDistribution = self.createCellDistributions(positions)

        localOrders = self.__initialiseLocalOrders(positions, orientations, cellToParticleDistribution, particleToCellDistribution)
        self.localOrderHistory[0,:]=localOrders

        # for every time step, the positions, orientations, switchTypeValue and colours for each particle are updated and added to the histories
        for it in range(numIntervals):
            self.t = it

            if t % 1000 == 0:
                print(f"t={t}/{numIntervals-1}")

            for i in range(len(positions)):
                positions[i] += dt*(self.speed*orientations[i])
                cellToParticleDistribution, particleToCellDistribution = self.updateCellForParticle(i, positions, cellToParticleDistribution, particleToCellDistribution)
                positions[i] += -self.domainSize*np.floor(positions[i]/self.domainSize)
            
            neighbourCandidates = self.__findNeighbours(positions, cellToParticleDistribution, particleToCellDistribution)

            self.cleanSelectedIndices(it)
            # check if any events take effect at this timestep before anything except the positions is updates
            if events != None:
                for event in events:
                    orientations, switchTypeValues, self.selectedIndices[it] = event.check(self.numberOfParticles, it, positions, orientations, switchTypeValues, self.cells, self.cellDims, cellToParticleDistribution)

            previousLocalOrders = localOrders
            localOrders = self.__getLocalOrders(orientations, neighbourCandidates)
            switchTypeValues = self.computeSwitchTypeValues(timestep=it, previousSwitchTypeValues=switchTypeValues, neighbours=neighbourCandidates, localOrders=localOrders, previousLocalOrders=previousLocalOrders)

            colours = self.__colourGroups(switchTypeValues)

            orientations = self.calculateMeanOrientations(positions, orientations, switchTypeValues, neighbourCandidates)
            orientations = self.__normalizeOrientations(orientations+self.generateNoise())

            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations
            self.localOrderHistory[it,:]=localOrders
            switchTypeValuesHistory[it]=switchTypeValues
            coloursHistory[it]=colours

            t+=dt

        return (dt*np.arange(numIntervals), positionsHistory, orientationsHistory), coloursHistory, switchTypeValuesHistory
    

    def initialiseCells(self):
        """
        Initialises the cell grid for the current domain.

        Returns:
            The cell grid as an array of arrays [[(minX, minY), (maxX, maxY)]].
        """
        domainArea = self.domainSize[0] * self.domainSize[1]
        pointArea = domainArea / self.numCells
        length = np.sqrt(pointArea)

        cells = []
        self.cellDims = (int(self.domainSize[0]/length), int(self.domainSize[1]/length))
        for x in np.arange(0, self.domainSize[0], length):
            for y in np.arange(0, self.domainSize[1], length):
                cells.append([(x, y), (x+length, y+length)])
        return cells
    
    def determineNeighbouringCells(self):
        """
        Creates a dictionary of the neighbouring cells of every cell in the cell grid.

        Returns:
            A dictionary with an entry for every cell with an array of the indices of its neighbours as its value.
        """
        neighbouringCells = {}
        for cellIdx, _ in enumerate(self.cells):
            neighbours = [cellIdx] # always check the particle's own cell
            # top if not in top row
            if cellIdx % self.cellDims[1] != 0:
                neighbours.append(cellIdx-1)
                # corner up left
                if cellIdx >= self.cellDims[1]:
                    neighbours.append(cellIdx - self.cellDims[1] -1)
                # corner up right
                if cellIdx < ((self.cellDims[0]*self.cellDims[1]) - self.cellDims[1]):
                    neighbours.append(cellIdx + self.cellDims[1] - 1) 
            # bottom if not in bottom row
            if cellIdx % self.cellDims[1] != (self.cellDims[1]-1):
                neighbours.append(cellIdx+1)
                # corner bottom left
                if cellIdx >= self.cellDims[1]:
                    neighbours.append(cellIdx - self.cellDims[1] + 1)
                # corner bottom right
                if cellIdx < ((self.cellDims[0]*self.cellDims[1]) - self.cellDims[1]):
                    neighbours.append(cellIdx + self.cellDims[1] + 1)
            # left if not in leftmost row
            if cellIdx >= self.cellDims[1]:
                neighbours.append(cellIdx-self.cellDims[1])
            # right if not in rightmost row
            if cellIdx < ((self.cellDims[0]*self.cellDims[1]) - self.cellDims[1]):
                neighbours.append(cellIdx+self.cellDims[1])   
            neighbouringCells[cellIdx] = neighbours    
        return neighbouringCells
    
    def createCellDistributions(self, positions):
        """
        Initialises the distribution of particles within the cell grid.

        Params:
            - positions (array of (x,y)-coordinates): the initial positions of all particles within the domain

        Returns:
            Two dictionaries: the particles for every cell and the cell for every particle.
        """
        cellToParticleDistribution = {cellIdx: [] for cellIdx in range(len(self.cells))}
        particleToCellDistribution = {}
        for i in range(len(positions)):
            xPos = positions[i][0]
            yPos = positions[i][1]
            for cellIdx, cell in enumerate(self.cells):
                if cell[0][0] <= xPos and cell[0][1] <= yPos and cell[1][0] >= xPos and cell[1][1] >= yPos:
                    cellToParticleDistribution.get(cellIdx).append(i)
                    particleToCellDistribution[i] = cellIdx
        return cellToParticleDistribution, particleToCellDistribution

    def updateCellForParticle(self, i, positions, cellToParticleDistribution, particleToCellDistribution):
        """
        Update the mapping of the particle to the cell and vice versa.

        Params:
            - i (int): the index of the current particle
            - positions (array of (x,y)-coordinates): the current positions of all particles
            - cellToParticleDistribution (dictionary cellIdx: [particleIndices]): the distribution of particles for each cell
            - particleToCellDistribution (dictionary particleIdx: cellidx): the cell in which any given particle is currently situated

        Returns:
            The two updated dictionaries cellToParticleDistribution and particleToCellDistribution.
        """
        oldCellIdx = particleToCellDistribution[i]
        currentCell = self.cells[oldCellIdx]
        posX = positions[i][0]
        posY = positions[i][1]

        oldX = np.floor(oldCellIdx/self.cellDims[1])
        oldY = oldCellIdx % self.cellDims[1]
        if posX < 0:
            newX = self.cellDims[0] -1
        elif posX > self.domainSize[0]:
            newX = 0
        elif posX < currentCell[0][0]:
            newX = oldX - 1
        elif posX > currentCell[1][0]:
            newX = oldX + 1
        else:
            newX = oldX
        
        if posY < 0:
            newY = self.cellDims[1] -1
        elif posY > self.domainSize[1]:
            newY = 0
        elif posY < currentCell[0][1]:
            newY = oldY - 1
        elif posY > currentCell[1][1]:
            newY = oldY + 1
        else:
            newY = oldY

        newCellIdx = int((newX * self.cellDims[1]) + newY)

        particleToCellDistribution[i] = newCellIdx
        cellToParticleDistribution[oldCellIdx].remove(i)
        cellToParticleDistribution[newCellIdx].append(i)

        return cellToParticleDistribution, particleToCellDistribution


    def __normalizeOrientations(self,orientations):
        """
        Normalises the orientations of all particles for the current time step

        Parameters:
            - orientations (array): The current orientations of all particles

        Returns:
            The normalised orientations of all particles as an array.
        """
        return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])


    def __initializeState(self, domainSize, numberOfParticles):
        """
        Initialises random positions and orientations for all particles within the domain.

        Parameters.
            - domainSize (numpy array): the size of the domain, i.e. all possible positions must be within this domain
            - numberOfParticles (int): the number of particles to be placed within the domain
        
        Returns:
            2 arrays, the first containing the positions, the second containing the orientations. Initialised randomly.
        """
        positions = domainSize*np.random.rand(numberOfParticles,len(domainSize))
        orientations = self.__normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        match self.switchType:
            case SwitchType.NEIGHBOUR_SELECTION_MODE:
                switchTypeValues = numberOfParticles * [self.neighbourSelectionMode]
            case SwitchType.K:
                switchTypeValues = numberOfParticles * [self.k]
        return positions, orientations, switchTypeValues
    
        
    def __findNeighbours(self, positions, cellToParticleDistribution, particleToCellDistribution):
        """
        Finds all the neighbours for every particle.

        Params:
            - positions (array of (x,y)-coordinates): the current positions of all particles
            - cellToParticleDistribution (dictionary cellIdx: [particleIndices]): the distribution of particles for each cell
            - particleToCellDistribution (dictionary particleIdx: cellidx): the cell in which any given particle is currently situated

        Returns:
            An array of arrays of the indices all neighbours for every particle.
        """
        neighbourCandidates = []
        for part, cell in particleToCellDistribution.items():
            cellsToCheck = self.neighbouringCells.get(cell)
            candidates = [cand for candCell in cellsToCheck for cand in cellToParticleDistribution[candCell]]
            neighbourCandidates.append([candIdx for candIdx in candidates if ServiceMetric.isNeighbour(self.radius, positions, part, candIdx)])
        return neighbourCandidates

    def __selectNeighbours(self, neighbourCandidates, positions, orientations, switchTypeValues):
        """
        Decides which neighbours will be considered for the orientation update. Always includes the particle's own orientation.

        Parameters:
            - neighbourCandidates (array of arrays of bools): for every particle, contains a boolean specifying if the other particle is within the perception radius
            - positions (array of [int, int]): the current position of every particle
            - orientations (array of [int, int]): the current orientation of every particle
        
        Returns:
            An array of arrays of booleans specifying which other particles have been selected as the relevant neighbours for every particle.
        """        
        neighbours = []
        for i in range(0, self.numberOfParticles):
            # individual selection for switch value
            neighbourSelectionMode = self.neighbourSelectionMode
            k = self.k
            match self.switchType:
                case SwitchType.NEIGHBOUR_SELECTION_MODE:
                    neighbourSelectionMode = switchTypeValues[i]
                case SwitchType.K:
                    k = switchTypeValues[i]

            # neighbour selection
            candidates = neighbourCandidates[i]
            iNeighbours = self.numberOfParticles * [False]
            currentParticlePosition = positions[i]
            currentParticleOrientation = orientations[i]
            match neighbourSelectionMode:
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    random.shuffle(candidates)
                    pickedNeighbours = candidates[:k]
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST:
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nsmallest(k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST:
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nlargest(k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE:
                    candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nsmallest(k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE:
                    candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nlargest(k, candidateDistances, candidateDistances.get)
                case _:  # select all neighbours
                    pickedNeighbours = candidates
            iNeighbours[i] = True # should always consider the current orientation regardless of k or the neighbour selection method
            for neighbour in pickedNeighbours:
                iNeighbours[neighbour] = True
            neighbours.append(iNeighbours)
        return np.array(neighbours)
    
    """
    def computeSwitchTypeValues(self, previousSwitchTypeValues, orientations, neighbours, previousLocalOrders):
        switchTypeValues = self.numberOfParticles * [None]
        localOrders = self.numberOfParticles * [None]
        for i in range(len(orientations)):
            neighbourOrientations = [orientations[neighbourIdx] for neighbourIdx in neighbours[i]]
            hasNeighbours = len(neighbourOrientations) > 1
            localOrder = ServiceMetric.computeOrder(neighbourOrientations)
            localOrders[i] = localOrder # preparation for next time step
            switchTypeValues[i] = self.__getSingleSwitchTypeValue(previousSwitchTypeValues[i], hasNeighbours, previousLocalOrders[i], localOrder)
            
        return switchTypeValues, localOrders
"""
    def computeSwitchTypeValues(self, timestep, previousSwitchTypeValues, neighbours, localOrders, previousLocalOrders):
        """
        Determines the selected switch type value for every particle at the current timestep.

        Params:
            - previousSwitchTypeValues (array): The values for the last time step
            - neighbours (array of arrays): the neighbours of every particle
            - localOrders (array of floats): the current local order as perceived by every particle, indexed by particle index
            - previousLocalOrders (array of floats): the local order at the previous timestep as perceived by every particle, indexed by particle index

        Returns:
            An array with the switch type value selected for every particle at this timestep.
        """
        switchTypeValues = self.numberOfParticles * [None]
        for i in range(self.numberOfParticles):
            hasNeighbours = len(neighbours[i]) > 1
            # only update the switchTypeValue after the event lock has passed
            if any(i in val for val in self.selectedIndices.values()):
                switchTypeValues[i] = previousSwitchTypeValues[i]
            else:
                switchTypeValues[i] = self.__getSingleSwitchTypeValue(i, timestep, previousSwitchTypeValues[i], hasNeighbours, localOrders[i])
        return switchTypeValues
            
    def __getSingleSwitchTypeValue(self, idx, timestep, previousValue, hasNeighbours, localOrder):
        """
        Determines the switch type value for a single particle for the current timestep.

        Params:
            - previousValue (value of the switchType): the previous switch type value
            - hasNeighbours (boolean): does the particle have any neighbours at this timestep
            - localOrder (float): the current local order within the perception radius of the particle
            - previousLocalOrder (float): the local order within the perception radius of the particle at the last timestep

        Returns:
            The updated switch type value for the current timestep.
        """
        startAvg = max(timestep-self.numberPreviousStepsForThreshold, 0)
        endAvg = max(timestep, 1)
        previousLocalOrder = np.average(self.localOrderHistory[startAvg:endAvg][:,idx])

        if hasNeighbours == False:
            return previousValue

        if len(self.orderThresholds) > 1:       
            switchDifferenceThresholdLower = self.orderThresholds[0]
            switchDifferenceThresholdUpper = self.orderThresholds[1]
            hasPassedUpperThreshold = (localOrder >= switchDifferenceThresholdUpper and previousLocalOrder < switchDifferenceThresholdUpper) or (localOrder <= switchDifferenceThresholdUpper and previousLocalOrder > switchDifferenceThresholdUpper)
            hasPassedLowerThreshold = (localOrder <= switchDifferenceThresholdLower and previousLocalOrder > switchDifferenceThresholdLower) or (localOrder >= switchDifferenceThresholdLower and previousLocalOrder < switchDifferenceThresholdLower)

            if hasPassedUpperThreshold:
                if localOrder >= switchDifferenceThresholdUpper:
                    return self.orderSwitchValue
                else:
                    return self.disorderSwitchValue
            elif hasPassedLowerThreshold:
                if localOrder <= switchDifferenceThresholdLower:
                    return self.disorderSwitchValue
                else:
                    return self.orderSwitchValue
        elif len(self.orderThresholds) == 1:
            absoluteDiff = np.absolute(localOrder - previousLocalOrder)
            if absoluteDiff > self.orderThresholds[0]:
                if localOrder > previousLocalOrder:
                    return self.orderSwitchValue
                elif localOrder < previousLocalOrder:
                    return self.disorderSwitchValue
        return previousValue

            
    
    def __getLocalOrders(self, orientations, neighbours):
        """
        Computes the local order for every particle at the current time step.

        Params:
            - orientations (array of (u,v)-coordinates): the orientation of every particle at the current timestep
            - neighbours (array of arrays of int): the neighbours of every particle at the current timestep

        Returns:
            An array containing the local order as perceived by every particle.
        """
        localOrders = self.numberOfParticles * [None]
        for i in range(len(orientations)):
            neighbourOrientations = [orientations[neighbourIdx] for neighbourIdx in neighbours[i]]
            localOrder = ServiceMetric.computeOrder(neighbourOrientations)
            localOrders[i] = localOrder
        return localOrders
    
    def __initialiseLocalOrders(self, positions, orientations, cellToParticleDistribution, particleToCellDistribution):
        """
        Computes the initial local order for every particle in the domain.

        Params:
            - positions (array of (x,y)-coordinates): the position of every particle at the current timestep
            - orientations (array of (u,v)-coordinates): the orientation of every particle at the current timestep
            - cellToParticleDistribution (dictionary cellIdx: [particleIndices]): the distribution of particles for each cell
            - particleToCellDistribution (dictionary particleIdx: cellidx): the cell in which any given particle is currently situated

        Returns:
            An array containing the local order as perceived by every particle.
        """
        neighbourCandidates = self.__findNeighbours(positions, cellToParticleDistribution, particleToCellDistribution)
        return self.__getLocalOrders(orientations, neighbourCandidates)

    def __colourGroups(self, switchTypeValues):
        """
        Sets the colour for every particle based on which switch type value it has selected.

        Params:
            - switchTypeValues (array of switch type values): the current switch type value selected by every particle

        Returns:
            An array containing the colour of every particle for the current timestep.
        """
        # blue for order, red for disorder
        colours=self.numberOfParticles * ['k']
        for i in range(len(colours)):
            if any(i in val for val in self.selectedIndices.values()):
                colours[i] = 'g'
            elif switchTypeValues[i] == self.orderSwitchValue:
                colours[i] = 'b'
            elif switchTypeValues[i] == self.disorderSwitchValue:
                colours[i] = 'r'
        return colours
        
    def cleanSelectedIndices(self, timestep):
        self.selectedIndices = {k: v for k, v in self.selectedIndices.items() if (k + self.switchBlockedAfterEventTimesteps) >= timestep}