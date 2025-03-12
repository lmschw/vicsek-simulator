import numpy as np
import math

import DefaultValues as dv
from EnumSwitchType import SwitchType
from EnumThresholdType import ThresholdType
import ServiceMetric
import ServiceVicsekHelper
import ServiceOrientations
import ServiceSavedModel

"""
Version of the modified Vicsek model used for local updatese by individuals without events or with events with a duration of a single timestep.
"""
class VicsekWithNeighbourSelection:

    def __init__(self, neighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, 
                 radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, 
                 k=dv.DEFAULT_K_NEIGHBOURS, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE, numCells=None, 
                 switchType=None, switchValues=(None, None), thresholdType=None, orderThresholds=None, 
                 numberPreviousStepsForThreshold=10, switchBlockedAfterEventTimesteps=-1, occlusionActive=False,
                 switchingActive=True, returnHistories=True, logPath=None):
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
            - switchBlockedAfterEventTimesteps (int) [optional]: the number of timesteps that a selected particle will not be able to change its value
            - occlusionActive (boolean) [optional]: whether particles can see particles that are hidden behind other particles
            - switchingActive (boolean) [optional]: if False, the particles cannot update their values

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
        self.switchType = switchType
        self.orderSwitchValue, self.disorderSwitchValue = switchValues
        self.thresholdType = thresholdType
        self.orderThresholds = orderThresholds
        self.numberPreviousStepsForThreshold = numberPreviousStepsForThreshold
        self.switchBlockedAfterEventTimesteps = switchBlockedAfterEventTimesteps
        self.occlusionActive = occlusionActive
        self.switchingActive = switchingActive
        self.returnHistories = returnHistories
        self.logPath = logPath
        self.selectedIndices = {}

        if numCells == None:
            self.numCells = max(math.floor(math.sqrt((domainSize[0] * domainSize[1]) / (radius**2))) ** 2, 1)
            print(f"domainSize = {domainSize}, radius = {radius}, numCells = {self.numCells}")
        else:
            self.numCells = numCells

        self.events = None


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
                    "dt": self.dt,
                    "numCells": self.numCells,
                    "cellDims": self.cellDims,
                    "thresholdType": self.thresholdType.name,
                    "thresholds": self.orderThresholds,
                    "previousSteps": self.numberPreviousStepsForThreshold,
                    "blockedSteps": self.switchBlockedAfterEventTimesteps,
                    "occlusionActive": self.occlusionActive,
                    "switchingActive": self.switchingActive,
                    }
        if self.switchingActive:
            summary["switchType"] = self.switchType.name
            summary["orderValue"] = self.orderSwitchValue
            summary["disorderValue"] = self.disorderSwitchValue

        if self.events:
            eventsSummary = []
            for event in self.events:
                eventsSummary.append(event.getParameterSummary())
            summary["events"] = eventsSummary

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
            - switchTypeValues (arr): the switch type values of all particles at the current timestep
            - neighbourCandidates (arr): the indices of all neighbouring particles
        Returns:
            An array of the adapted orientations.
        """
        neighbours = self.__selectNeighbours(neighbourCandidates, positions, orientations, switchTypeValues)
        summedOrientations = np.sum(neighbours[:,:,np.newaxis]*orientations[np.newaxis,:,:],axis=1)
        return ServiceVicsekHelper.normalizeOrientations(summedOrientations)

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
            - initialState (tuple of arrays) [optional]: A tuple containing the initial positions of all particles, their initial orientations and their initial switch type values
            - dt (int) [optional]: time step
            - tmax (int) [optional]: the total number of time steps of the experiment

        Returns:
            times, positionsHistory, orientationsHistory, coloursHistory, switchTypeValueHistory. All of them as ordered arrays so that they can be matched by index matching
        """

        import time
        st = time.time()
        #if any(events):
        if events != None:
            self.events = events

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

        # preparing the cells
        self.cells = self.initialiseCells()
        self.neighbouringCells = self.determineNeighbouringCells()

        cellToParticleDistribution, particleToCellDistribution = self.createCellDistributions(positions)

        self.initialiseHistoriesAndLogs(numIntervals=numIntervals,
                                        positions=positions,
                                        orientations=orientations,
                                        switchTypeValues=switchTypeValues)
        
        localOrders = self.__initialiseLocalOrders(positions, orientations, cellToParticleDistribution, particleToCellDistribution)
        self.localOrderHistory[0,:]=localOrders

        # for every time step, the positions, orientations, switchTypeValues and colours for each particle are updated and added to the histories
        for it in range(numIntervals):
            self.t = it

            if t % 1000 == 0:
                print(f"t={t}/{numIntervals-1}")

            # find every particle within the perception radius
            neighbourCandidates = self.findNeighbours(positions, orientations, cellToParticleDistribution, particleToCellDistribution)

            # remove expired selected indices
            self.cleanSelectedIndices(it)

            # check if any events take effect at this timestep before anything except the positions is updates
            if events != None:
                for event in events:
                    orientations, switchTypeValues, self.selectedIndices[it] = event.check(self.numberOfParticles, it, positions, orientations, switchTypeValues, self.cells, self.cellDims, cellToParticleDistribution)

            # update switch type values
            previousLocalOrders = localOrders
            localOrders = self.__getLocalOrders(orientations, neighbourCandidates)
            if self.switchingActive == True:
                switchTypeValues = self.computeSwitchTypeValues(timestep=it, previousSwitchTypeValues=switchTypeValues, neighbours=neighbourCandidates, localOrders=localOrders, previousLocalOrders=previousLocalOrders)

            # update colours
            colours = self.__colourGroups(switchTypeValues)

            # update orientations
            orientations = self.calculateMeanOrientations(positions, orientations, switchTypeValues, neighbourCandidates)
            orientations = ServiceVicsekHelper.normalizeOrientations(orientations+self.generateNoise())

            # update positions so that the neighbourhood is already updated for the remaining computations
            for i in range(len(positions)):
                positions[i] += dt*(self.speed*orientations[i])
                cellToParticleDistribution, particleToCellDistribution = self.updateCellForParticle(i, positions, cellToParticleDistribution, particleToCellDistribution)
                positions[i] += -self.domainSize*np.floor(positions[i]/self.domainSize)

            self.updateHistoriesAndLogs(t=it,
                                        positions=positions,
                                        orientations=orientations,
                                        switchTypeValues=switchTypeValues,
                                        colours=colours,
                                        localOrders=localOrders)

            """
            if t >= tmax-5:
                print(f"t={t}")
                print("pos")
                print(positions)
                print("ori")
                print(orientations)
            """
            print(f"t={t}, order={ServiceMetric.computeOrder(orientations)}")

            
            t+=dt

        import ServiceGeneral
        et = time.time()
        ServiceGeneral.logWithTime(f"duration simulate(): {ServiceGeneral.formatTime(et-st)}")
        return (dt*np.arange(numIntervals), self.positionsHistory, self.orientationsHistory), self.coloursHistory, self.switchTypeValuesHistory
    

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
        self.cellDims = (self.domainSize[0]/length, self.domainSize[1]/length)
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
        orientations = ServiceVicsekHelper.normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        match self.switchType:
            case SwitchType.NEIGHBOUR_SELECTION_MODE:
                switchTypeValues = numberOfParticles * [self.neighbourSelectionMode]
            case SwitchType.K:
                switchTypeValues = numberOfParticles * [self.k]
            case _:
                switchTypeValues = numberOfParticles * [None]
        return positions, orientations, switchTypeValues
    
    def findNeighbours(self, positions, orientations, cellToParticleDistribution, particleToCellDistribution):
        """
        Finds all the neighbours for every particle.

        Params:
            - positions (array of (x,y)-coordinates): the current positions of all particles
            - orientations (array of (x,y)-coordinates): the current orientations of all particles
            - cellToParticleDistribution (dictionary cellIdx: [particleIndices]): the distribution of particles for each cell
            - particleToCellDistribution (dictionary particleIdx: cellidx): the cell in which any given particle is currently situated

        Returns:
            An array of arrays of the indices all neighbours for every particle.
        """
        neighbourCandidates = []
        for part, cell in particleToCellDistribution.items():
            cellsToCheck = self.neighbouringCells.get(cell)
            candidates = [cand for candCell in cellsToCheck for cand in cellToParticleDistribution[int(candCell)]]
            neighbourCandidates.append([candIdx for candIdx in candidates if ServiceMetric.isNeighbour(self.radius, positions, part, candIdx) and self.isVisibleToParticle(particleIdx=part, candidateIdx=candIdx, positions=positions, orientations=orientations, neighbourCandidates=neighbourCandidates)])
        return neighbourCandidates
    
    def isVisibleToParticle(self, particleIdx, candidateIdx, positions, orientations, neighbourCandidates):
        """
        Checks if another particle is visible to the current particle. Checks if the other particle is within the field of vision.

        Params:
            - particleIdx (int): The index of the current particle
            - candidateIdx (int): The index of the other particle that should be checked
            - positions (array of arrays of floats): the position of every particle at the current timestep
            - orientations (array of arrays of floats): the orientation of every particle at the current timestep
            - neighbourCandidates (array of int): all particles within the radius

        Returns:
            A boolean describing whether the other particle can be seen by the current particle.
        """
        isVisible = True
        if self.occlusionActive:
            isVisible = isVisible and not ServiceOrientations.isParticleOccluded(particleIdx=particleIdx, otherIdx=candidateIdx, positions=positions, orientations=orientations, candidates=neighbourCandidates)
        return isVisible
        

    def __selectNeighbours(self, neighbourCandidates, positions, orientations, switchTypeValues):
        """
        Decides which neighbours will be considered for the orientation update. Always includes the particle's own orientation.

        Parameters:
            - neighbourCandidates (array of arrays of bools): for every particle, contains a boolean specifying if the other particle is within the perception radius
            - positions (array of [int, int]): the current position of every particle
            - orientations (array of [int, int]): the current orientation of every particle
            - switchTypeValues (array): the current switch type values of every particle
        
        Returns:
            An array of arrays of booleans specifying which other particles have been selected as the relevant neighbours for every particle.
        """        
        neighbours = []
        for i in range(0, self.numberOfParticles):
            # individual selection for switch value
            neighbourSelectionMode = self.neighbourSelectionMode
            k = self.k
            if self.switchingActive == True:
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
            pickedNeighbours = ServiceVicsekHelper.pickNeighbours(neighbourSelectionMode, k, candidates, currentParticlePosition, currentParticleOrientation, positions, orientations)
            iNeighbours[i] = True # should always consider the current orientation regardless of k or the neighbour selection method
            for neighbour in pickedNeighbours:
                iNeighbours[neighbour] = True
            neighbours.append(iNeighbours)
        return np.array(neighbours)

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
                """
                # TODO: can be used if you want to implement a delay. Needs to be added properly with a parameter and everything in the future
                if switchTypeValues[i] != previousSwitchTypeValues[i]:
                    if timestep in self.selectedIndices.keys():
                        self.selectedIndices.get(timestep).append(i)
                    else:
                        self.selectedIndices[timestep] = [i]
                """
        return switchTypeValues
            
    def __getSingleSwitchTypeValue(self, idx, timestep, previousValue, hasNeighbours, localOrder):
        """
        Determines the switch type value for a single particle for the current timestep.

        Params:
            - idx (int): the index of the current particle
            - timestep (int): the current timestep
            - previousValue (switchTypeValue): the switch type value of the last timestep for the current particle
            - hasNeighbours (boolean): does the particle have any neighbours at this timestep
            - localOrder (float): the current local order within the perception radius of the particle

        Returns:
            The updated switch type value for the current timestep.
        """
        startAvg = max(timestep-self.numberPreviousStepsForThreshold, 0)
        endAvg = max(timestep, 1)
        previousLocalOrder = np.average(self.localOrderHistory[startAvg:endAvg][:,idx])

        # TODO: make this optional
        if hasNeighbours == False:
            return previousValue

        match self.thresholdType: 
            case ThresholdType.TWO_THRESHOLDS:
                # setting the two thresholds
                switchDifferenceThresholdLower, switchDifferenceThresholdUpper = self.__getLowerAndUpperThreshold()
                # determining the switchTypeValue
                if localOrder >= switchDifferenceThresholdUpper: 
                    # uppermost order zone
                    return self.orderSwitchValue
                elif localOrder <= switchDifferenceThresholdLower: 
                    # lowermost order zone
                    return self.disorderSwitchValue
                elif localOrder <= switchDifferenceThresholdUpper and previousLocalOrder > switchDifferenceThresholdUpper: 
                    # neutral middle zone coming from above
                    return self.disorderSwitchValue
                elif localOrder >= switchDifferenceThresholdLower and previousLocalOrder < switchDifferenceThresholdLower:
                    # neutral middle zone coming from below
                    return self.orderSwitchValue
            case ThresholdType.TWO_THRESHOLDS_SIMPLE:
                switchDifferenceThresholdLower, switchDifferenceThresholdUpper = self.__getLowerAndUpperThreshold()
                if localOrder >= switchDifferenceThresholdUpper: 
                    # uppermost order zone
                    return self.orderSwitchValue
                elif localOrder <= switchDifferenceThresholdLower: 
                    # lowermost order zone
                    return self.disorderSwitchValue
            case ThresholdType.TWO_THRESHOLDS_SIMPLE_REVERSE:
                switchDifferenceThresholdLower, switchDifferenceThresholdUpper = self.__getLowerAndUpperThreshold()
                if localOrder >= switchDifferenceThresholdUpper: 
                    # uppermost order zone
                    return self.disorderSwitchValue
                elif localOrder <= switchDifferenceThresholdLower: 
                    # lowermost order zone
                    return self.orderSwitchValue
            case ThresholdType.HYSTERESIS:
                switchDifferenceThresholdLower, switchDifferenceThresholdUpper = self.__getLowerAndUpperThreshold()
                if localOrder - previousLocalOrder > 0:
                    if localOrder >= switchDifferenceThresholdUpper:
                        return self.orderSwitchValue
                else:
                    if localOrder <= switchDifferenceThresholdLower:
                        return self.disorderSwitchValue
            case ThresholdType.HYSTERESIS_REVERSED:
                switchDifferenceThresholdLower, switchDifferenceThresholdUpper = self.__getLowerAndUpperThreshold()
                if localOrder - previousLocalOrder > 0:
                    if localOrder >= switchDifferenceThresholdUpper:
                        return self.disorderSwitchValue
                else:
                    if localOrder <= switchDifferenceThresholdLower:
                        return self.orderSwitchValue
            case ThresholdType.SINGLE_DIFFERENCE_THRESHOLD:
                absoluteDiff = np.absolute(localOrder - previousLocalOrder)
                if absoluteDiff > self.orderThresholds[0]:
                    if localOrder > previousLocalOrder:
                        return self.orderSwitchValue
                    elif localOrder < previousLocalOrder:
                        return self.disorderSwitchValue
        return previousValue
    
    def __getLowerAndUpperThreshold(self):
        """
        Determines the lower and upper threshold for updating the switch type values.

        Returns:
            Floats with values typically between 0 and 1 representing the lower and upper thresholds
        """
        if len(self.orderThresholds) == 1:
            switchDifferenceThresholdLower = self.orderThresholds[0]
            switchDifferenceThresholdUpper = 1 - self.orderThresholds[0]
        else:
            switchDifferenceThresholdLower = self.orderThresholds[0]
            switchDifferenceThresholdUpper = self.orderThresholds[1]
        return switchDifferenceThresholdLower, switchDifferenceThresholdUpper


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
        neighbourCandidates = self.findNeighbours(positions, orientations, cellToParticleDistribution, particleToCellDistribution)
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
        """
        Removes selected indices that have been updated too long ago to still be blocked.

        Params:
            - timestep (int): the current timestep

        Returns:
            Nothing.
        """
        self.selectedIndices = {k: v for k, v in self.selectedIndices.items() if (k + self.switchBlockedAfterEventTimesteps) > timestep}

    def initialiseHistoriesAndLogs(self, numIntervals, positions, orientations, switchTypeValues):
        self.localOrderHistory = np.zeros((numIntervals,self.numberOfParticles))        
       
        if self.returnHistories:
            self.positionsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
            self.orientationsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))  
            self.switchTypeValuesHistory = numIntervals * [self.numberOfParticles * [None]]
            self.coloursHistory = numIntervals * [self.numberOfParticles * ['k']]
            eventPositionHistory = np.zeros((numIntervals,1,len(self.domainSize)))
            eventOrientationHistory = np.zeros((numIntervals,1,len(self.domainSize)))

            self.positionsHistory[0,:,:]=positions
            self.orientationsHistory[0,:,:]=orientations
            self.switchTypeValuesHistory[0]=switchTypeValues

        if self.logPath:
            ServiceSavedModel.logModelParams(path=f"{self.logPath}_modelParams", modelParamsDict=self.getParameterSummary())
            ServiceSavedModel.initialiseCsvFileHeaders(path=self.logPath, addSwitchValueHeader=self.switchingActive)


    def updateHistoriesAndLogs(self, t, positions, orientations, switchTypeValues, colours, localOrders):
        if self.returnHistories:
            # update histories
            self.positionsHistory[t,:,:]=positions
            self.orientationsHistory[t,:,:]=orientations
            self.switchTypeValuesHistory[t]=switchTypeValues
            self.coloursHistory[t]=colours
        self.localOrderHistory[t,:]=localOrders

        if self.logPath:
            ServiceSavedModel.saveModelTimestep(timestep=t, 
                                                positions=positions, 
                                                orientations=orientations,
                                                colours=colours,
                                                path=self.logPath,
                                                switchValues=switchTypeValues,
                                                switchingActive=self.switchingActive)