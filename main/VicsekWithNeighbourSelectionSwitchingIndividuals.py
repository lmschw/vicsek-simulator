import numpy as np
import random
import math
from heapq import nlargest
from heapq import nsmallest

import DefaultValues as dv
import EnumNeighbourSelectionMode
import EnumSwitchType

class VicsekWithNeighbourSelection:

    COLOUR_MAPPING = {EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM: 'k',
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST: 'r',
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST: 'b',
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE: 'g',
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE: 'y'}

    def __init__(self, defaultNeighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, k=dv.DEFAULT_K_NEIGHBOURS, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE):
        """
        Initialize the model with all its parameters

        Params:
            - defaultNeighbourSelectionMode (EnumNeighbourSelectionMode.NeighbourSelectionMode): how the particles select which of the other particles within their perception radius influence their orientation at the start
            - domainSize (tuple x,y) [optional]: the size of the domain for the particle movement
            - speed (int) [optional]: how fast the particles move
            - radius (int) [optional]: defines the perception field of the individual particles, i.e. the area in which it can perceive other particles
            - noise (float) [optional]: noise amplitude. adds noise to the orientation adaptation
            - numberOfParticles (int) [optional]: the number of particles within the domain, n
            - k (int) [optional]: the number of neighbours a particle considers when updating its orientation at every time step
            - showExample (bool) [optional]: whether a random example particle should be coloured in red with its influencing neighbours in yellow

        Returns:
            No return.
        """
        self.neighbourSelectionMode = defaultNeighbourSelectionModel
        self.domainSize = np.asarray(domainSize)
        self.speed = speed
        self.radius = radius
        self.noise = noise
        self.numberOfParticles = numberOfParticles
        self.k = k
        self.showExample = showExample

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
    
    
    def calculateMeanOrientations(self, positions, orientations, modeDistribution):
        """
        Updates the orientations of all particles based on the model parameters.

        Parameters:
            - positions (arr): the positions of all particles at the current timestep
            - orientations (arr): the orientations of all particles at the current timestep

        Returns:
            An array of the adapted orientations.
        """
        rij=positions[:,np.newaxis,:]-positions
    
        rij = rij - self.domainSize*np.rint(rij/self.domainSize) #minimum image convention

        rij2 = np.sum(rij**2,axis=2)
        neighbourCandidates = (rij2 <= self.radius**2)

        modeDistribution = self.__updateModeDistribution(neighbourCandidates, modeDistribution)
        
        neighbours = self.__selectNeighbours(neighbourCandidates, positions, orientations)
        summedOrientations = np.sum(neighbours[:,:,np.newaxis]*orientations[np.newaxis,:,:],axis=1)

        return self.__normalizeOrientations(summedOrientations), modeDistribution

    def generateNoise(self):
        """
        Generates noise to dislodge the system from local optima.

        Returns:
            A single noise value.
        """
        return np.random.normal(scale=self.noise, size=(self.numberOfParticles, len(self.domainSize)))

    def simulate(self, initialState=(None, None), dt=None, tmax=None, initialModeDistribution=None):
        """
        Runs the simulation experiment.
        First the parameters are computed if they are not passed. Then the positions, orientations and colours are computed for each particle at each time step.

        Parameters:
            - initialState (tuple of arrays) [optional]: A tuple containing the initial positions of all particles and their initial orientations
            - dt (int) [optional]: time step
            - tmax (int) [optional]: the total number of time steps of the experiment
            - switchType (EnumSwitchType) [optional]: the type of switching, e.g. noise value, neighbour selection mode
            - switches (array of arrays) [optional]: first subelement of every element signifies the timestep for the switch, second subelement signifies the new value. Should be ordered according to the time stamps

        Returns:
            time points, positionsHistory, orientationsHistory, coloursHistory. All of them as ordered arrays so that they can be matched by index matching
        """

        # Preparations and setting of parameters if they are not passed to the method
        positions, orientations = initialState
        
        if any(ele is None for ele in initialState):
            positions, orientations = self.__initializeState(self.domainSize, self.numberOfParticles)
            
        if dt is None and tmax is not None:
            dt = 1
        
        if tmax is None:
            tmax = (10**3)*dt
            dt = 10**(-2)*(np.max(self.domainSize)/self.speed)

        if initialModeDistribution is None:
            modeDistribution = self.numberOfParticles * [self.neighbourSelectionMode]
        else:
            modeDistribution = initialModeDistribution

        self.tmax = tmax
        self.dt = dt
        
        # Initialisations for the loop and the return variables
        t=0
        numIntervals=int(tmax/dt+1)
        
        positionsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        orientationsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        coloursHistory = numIntervals * [self.numberOfParticles * [None]]
        modeHistory = numIntervals * [self.numberOfParticles * [self.neighbourSelectionMode]]

        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        modeHistory[0]=modeDistribution
        
        # for every time step, the positions, orientations and colours for each particle are updated and added to the histories
        for it in range(numIntervals):
            print(f"t={t}/{numIntervals-1}")

            if it == 100:
                attackerPoint = [30,30]
                affectedIndices = [idx for idx in range(self.numberOfParticles) if self.__isNeighbour(attackerPoint[0], attackerPoint[1], positions, idx, self.radius)]
                for affectedIdx in affectedIndices:
                    modeDistribution[affectedIdx] = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
                #modeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
                #odeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
                #modeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST
            """
            if it == 1500:
                modeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST
                modeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST
                modeDistribution[random.randint(0, self.numberOfParticles)] = EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST
            """

            positions += dt*(self.speed*orientations)
            positions += -self.domainSize*np.floor(positions/self.domainSize)

            orientations, modeDistribution = self.calculateMeanOrientations(positions, orientations, modeDistribution)
            orientations = self.__normalizeOrientations(orientations+self.generateNoise())

            colours = [self.COLOUR_MAPPING[mode] for mode in modeDistribution]

            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations
            coloursHistory[it]=colours
            modeHistory[it]=modeDistribution

            t+=dt

        return (dt*np.arange(numIntervals), positionsHistory, orientationsHistory), coloursHistory, modeHistory
    

    def __isNeighbour(self, x, y, positions, idx, radius):
        return ((positions[idx][0] - x)**2 + (positions[idx][1] - y)**2) <= radius **2 
    
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
        
        return positions, orientations
    
    def __updateModeDistribution(self, neighbourCandidates, oldModeDistribution):
        modeDistribution = oldModeDistribution
        for idx in range(self.numberOfParticles):
            neighbours = [neighIdx for neighIdx in range(self.numberOfParticles) if neighbourCandidates[idx][neighIdx] == True and neighIdx != idx]
            counts = {EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM: 0,
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST: 0,
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST: 0,
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE: 0,
                      EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE: 0}
            for neighbourIdx in neighbours:
                counts[oldModeDistribution[neighbourIdx]] += 1
            newMode = nlargest(self.k, counts, counts.get)
            
            # makes a particle more likely to change its mode if any other modes are around
            if newMode[0] == oldModeDistribution[idx] and counts[newMode[1]] != 0:
                if newMode[1] == EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    print(counts)
                modeDistribution[idx] = newMode[1]
            elif counts[newMode[0]] != 0:
                if newMode[0] == EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    print(counts)
                modeDistribution[idx] = newMode[0]
            else:
                modeDistribution[idx] = oldModeDistribution[idx]
            """
            selectionVal = random.random()
            if counts[newMode[0]] == 0:
                modeDistribution[idx] = oldModeDistribution[idx]
            elif selectionVal >= 0.8 and counts[newMode[1]] > 0:
                modeDistribution[idx] = newMode[1]
            else:
                modeDistribution[idx] = newMode[0]
            """
        return modeDistribution

    def __selectNeighbours(self, neighbourCandidates, positions, orientations):
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
            candidates = [candIdx for candIdx in range(len(positions)) if neighbourCandidates[i][candIdx] == True and candIdx != i]
            iNeighbours = self.numberOfParticles * [False]
            currentParticlePosition = positions[i]
            currentParticleOrientation = orientations[i]
            match self.neighbourSelectionMode:
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    random.shuffle(candidates)
                    pickedNeighbours = candidates[:self.k]
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST:
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nsmallest(self.k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST:
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nlargest(self.k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE:
                    candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nsmallest(self.k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE:
                    candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nlargest(self.k, candidateDistances, candidateDistances.get)
                case _:  # select all neighbours
                    pickedNeighbours = candidates
            iNeighbours[i] = True # should always consider the current orientation regardless of k or the neighbour selection method
            for neighbour in pickedNeighbours:
                iNeighbours[neighbour] = True
            neighbours.append(iNeighbours)
        return np.array(neighbours)