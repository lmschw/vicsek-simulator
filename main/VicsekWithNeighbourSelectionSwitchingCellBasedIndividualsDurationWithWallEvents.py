import numpy as np

import DefaultValues as dv
import ServiceVicsekHelper

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals

"""
Version of the modified Vicsek model that is adapted for events with a duration > 1 timestep.
"""
class VicsekWithNeighbourSelection(VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection):

    def __init__(self, neighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, 
                 radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, 
                 k=dv.DEFAULT_K_NEIGHBOURS, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE, numCells=None, 
                 switchType=None, switchValues=(None, None), thresholdType=None, orderThresholds=None, 
                 numberPreviousStepsForThreshold=10, switchBlockedAfterEventTimesteps=-1, occlusionActive=False,
                 switchingActive=True):
        """
        Initialize the model with all its parameters

        Params:
            - neighbourSelectionModel (EnumNeighbourSelectionMode.NeighbourSelectionMode): how the particles select which of the other particles within their perception radius influence their orientation at any given time step
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
                    If only one number is supplied (as an array with one element), will be used to check if the difference between the previous and the current local order is greater than the threshold or as the lower threshold with the upper threshold being (1-orderThreshold)
                    If two numbers are supplied, will be used as a lower and an upper threshold that triggers a switch: [lowerThreshold, upperThreshold]
            - numberPreviousStepsForThreshold (int) [optional]: the number of previous timesteps that are considered for the average to be compared to the threshold value(s)
            - switchBlockedAfterEventTimesteps (int) [optional]: the number of timesteps that a selected particle will not be able to change its value
            - occlusionActive (boolean) [optional]: whether particles can see particles that are hidden behind other particles
            - switchingActive (boolean) [optional]: if False, the particles cannot update their values
   
        Returns:
            No return.
        """
        super().__init__(neighbourSelectionModel=neighbourSelectionModel,
                         domainSize=domainSize,
                         speed=speed,
                         radius=radius,
                         noise=noise,
                         numberOfParticles=numberOfParticles,
                         k=k,
                         showExample=showExample,
                         numCells=numCells,
                         switchType=switchType,
                         switchValues=switchValues,
                         thresholdType=thresholdType,
                         orderThresholds=orderThresholds,
                         numberPreviousStepsForThreshold=numberPreviousStepsForThreshold,
                         switchBlockedAfterEventTimesteps=switchBlockedAfterEventTimesteps,
                         occlusionActive=occlusionActive,
                         switchingActive=switchingActive)
        
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
    


    def simulate(self, initialState=(None, None, None), dt=None, tmax=None, events=None, wallEvents=None):
        """
        Runs the simulation experiment.
        First the parameters are computed if they are not passed. Then the positions, orientations and colours are computed for each particle at each time step.

        Parameters:
            - initialState (tuple of arrays) [optional]: A tuple containing the initial positions of all particles, their initial orientations and their initial switchTypeValues
            - dt (int) [optional]: time step
            - tmax (int) [optional]: the total number of time steps of the experiment
            - events (array of ExternalStimulusOrientationChangeEvents): the events that occur within the simulation

        Returns:
            times, positionsHistory, orientationsHistory, coloursHistory, switchTypeValuesHistory. All of them as ordered arrays so that they can be matched by index matching
        """

        if events == None:
            self.events = None
        else:
            self.events = events

        self.wallEvents = wallEvents

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
        eventPositionHistory = np.zeros((numIntervals,1,len(self.domainSize)))
        eventOrientationHistory = np.zeros((numIntervals,1,len(self.domainSize)))

        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        switchTypeValuesHistory[0]=switchTypeValues


        self.cells = self.initialiseCells()
        self.neighbouringCells = self.determineNeighbouringCells()

        cellToParticleDistribution, particleToCellDistribution = self.createCellDistributions(positions)

        localOrders = self.__initialiseLocalOrders(positions, orientations, cellToParticleDistribution, particleToCellDistribution)
        self.localOrderHistory[0,:]=localOrders

        # for every time step, the positions, orientations, switchTypeValues and colours for each particle are updated and added to the histories
        for it in range(1, numIntervals):
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
                    orientations, switchTypeValues, self.selectedIndices[it], eventPositionHistory[it], eventOrientationHistory[it] = event.check(self.numberOfParticles, it, positions, orientations, switchTypeValues, self.cells, self.cellDims, cellToParticleDistribution)
            if wallEvents != None:
                for wallEvent in wallEvents:
                    orientations = wallEvent.check(it, positions, orientations, self.speed, dt)

            # update switch type values
            previousLocalOrders = localOrders
            localOrders = self.__getLocalOrders(orientations, neighbourCandidates)
            if self.switchingActive == True:
                switchTypeValues = self.computeSwitchTypeValues(timestep=it, previousSwitchTypeValues=switchTypeValues, neighbours=neighbourCandidates, localOrders=localOrders, previousLocalOrders=previousLocalOrders)

            # update colours
            colours = self.__colourGroups(switchTypeValues)

            # update orientations
            for i in range(len(positions)):
                do = [dt*self.speed*o for o in orientations[i]]
                positions[i] = [positions[i][0] + do[0], positions[i][1] + do[1]]
                cellToParticleDistribution, particleToCellDistribution = self.updateCellForParticle(i, positions, cellToParticleDistribution, particleToCellDistribution)
                positions[i] += -self.domainSize*np.floor(positions[i]/self.domainSize)
            
            # update orientations
            orientations = self.calculateMeanOrientations(positions, orientations, switchTypeValues, neighbourCandidates)
            orientations = ServiceVicsekHelper.normalizeOrientations(orientations+self.generateNoise())

            # update histories
            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations
            self.localOrderHistory[it,:]=localOrders
            switchTypeValuesHistory[it]=switchTypeValues
            coloursHistory[it]=colours

            t+=dt

        # in case there is a moving event, e.g. a moving predator, the point of origin's values are appended as the last element to the histories before returning to preserve their movement data
        if events != None:
            positionsHistory, orientationsHistory, coloursHistory, switchTypeValuesHistory = self.addEventEntityToHistories(numIntervals, eventPositionHistory, eventOrientationHistory, positionsHistory, orientationsHistory, coloursHistory, switchTypeValuesHistory)

        return (dt*np.arange(numIntervals), positionsHistory, orientationsHistory), coloursHistory, switchTypeValuesHistory
    
    def addEventEntityToHistories(self, numIntervals, eventPositionHistory, eventOrientationHistory, positionsHistory, orientationsHistory, coloursHistory, switchTypeValuesHistory):
        """
        Adds the information (positions, orientations) of the point of origin of an event as the last element of the histories.
        For the coloursHistory, the event's point of origin is always set to yellow. The switchTypeValue is always set to the disorder value.
        
        Parameters:
            - numIntervals (int): the number of time steps within the experiment
            - eventPositionHistory (array of arrays of float): the position of the event's point of origin at every timestep
            - eventOrientationHistory (array of arrays of float): the orientation of the event's point of origin at every timestep
            - positionsHistory (array of arrays of float): the position of every particle at every timestep
            - orientationsHistory (array of arrays of float): the orientation of every particle at every timestep
            - coloursHistory (array of arrays of string): the colour value of every particle at every timestep
            - switchTypeValuesHistory (array of arrays): the switch type value of every particle at every timestep

        Returns:
            The updated positionsHistory, orientationsHistory, coloursHistory and switchTypeValuesHistory.
        """
        # TODO: adjust for multiple events
        newPositionsHistory = np.zeros((numIntervals,self.numberOfParticles+1,len(self.domainSize))) 
        newOrientationsHistory = np.zeros((numIntervals,self.numberOfParticles+1,len(self.domainSize))) 

        for t in range(len(positionsHistory)):
            if any(ele is None for ele in eventPositionHistory[t]):
                newPositionsHistory[t] = np.concatenate((positionsHistory[t], [[-1,-1]]), axis=0)
            else:
                newPositionsHistory[t] = np.concatenate((positionsHistory[t], eventPositionHistory[t]), axis=0)

            newOrientationsHistory[t] = np.concatenate((orientationsHistory[t], eventOrientationHistory[t]), axis=0)

            coloursHistory[t].append('y')
            switchTypeValuesHistory[t].append(self.disorderSwitchValue)
        return newPositionsHistory, newOrientationsHistory, coloursHistory, switchTypeValuesHistory
