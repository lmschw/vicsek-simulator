import numpy as np
import random

import DefaultValues as dv
import EnumNeighbourSelectionMode

class VicsekWithNeighbourSelection:

    def __init__(self, neighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, k=dv.DEFAULT_K_NEIGHBOURS, particleContainmentMode=dv.DEFAULT_PARTICLES_CONTAINMENT_MODE, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE):
        """
        Initialize the model
        """
        self.neighbourSelectionMode = neighbourSelectionModel
        self.domainSize = np.asarray(domainSize)
        self.speed = speed
        self.radius = radius
        self.noise = noise
        self.numberOfParticles = numberOfParticles
        self.k = k
        self.particleContainmentMode = particleContainmentMode
        self.showExample = showExample

    def __normalizeOrientations(self,orientations):
        return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

    def __initializeState(self, domainSize, numberOfParticles):
        positions = domainSize*np.random.rand(numberOfParticles,len(domainSize))
        orientations = self.__normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        
        return positions, orientations

    def calculateMeanOrientations(self, positions, orientations):
        rij=positions[:,np.newaxis,:]-positions
    
        rij = rij - self.domainSize*np.rint(rij/self.domainSize) #minimum image convention

        rij2 = np.sum(rij**2,axis=2)
        neighbourCandidates = (rij2 <= self.radius**2)

        neighbours = self.__selectNeighbours(positions, neighbourCandidates)
        summedOrientations = np.sum(neighbours[:,:,np.newaxis]*orientations[np.newaxis,:,:],axis=1)
        return self.__normalizeOrientations(summedOrientations)

    def generateNoise(self):
        return np.random.normal(scale=self.noise, size=(self.numberOfParticles, len(self.domainSize)))

    def simulate(self, initialState=(None, None), dt=None, tmax=None):
        positions, orientations = initialState
        
        if None in initialState:
            positions, orientations = self.__initializeState(self.domainSize, self.numberOfParticles);
            
        if dt is None:
            dt = 10**(-2)*(np.max(self.domainSize)/self.speed)
        
        if tmax is None:
            tmax = (10**3)*dt

        t=0
        numIntervals=int(tmax/dt+1)
        
        positionsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        orientationsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        coloursHistory = numIntervals * [self.numberOfParticles * ['k']]

        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        
        for it in range(numIntervals):
            print(f"t={t}/{numIntervals}")

            colours=self.numberOfParticles * ['k']

            positions += dt*(self.speed*orientations)
            positions += -self.domainSize*np.floor(positions/self.domainSize)

            orientations = self.calculateMeanOrientations(positions, orientations)
            orientations = self.__normalizeOrientations(orientations+self.generateNoise())

            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations
            coloursHistory[it]=colours

            t+=dt

        return dt*np.arange(numIntervals), positionsHistory, orientationsHistory, coloursHistory
    
    def __selectNeighbours(self, positions, neighbourCandidates):        
        neighbours = []
        for i in range(0, self.numberOfParticles):
            candidates = [candIdx for candIdx in range(len(positions)) if neighbourCandidates[i][candIdx] == True]
            iNeighbours = self.numberOfParticles * [False]
            match self.neighbourSelectionMode:
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    random.shuffle(candidates)
                    pickedNeighbours = candidates[:self.k]
                #case EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST:
                    #[candidate((candidate[0] - particle[0])**2 + (candidate[1] - particle[1])**2) for candidate in candidates]
                case _:  # select all neighbours
                    pickedNeighbours = candidates
            for neighbour in pickedNeighbours:
                iNeighbours[neighbour] = True
            neighbours.append(iNeighbours)
        return np.array(neighbours)