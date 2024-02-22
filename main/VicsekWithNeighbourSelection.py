import numpy as np
import random
import math
from heapq import nlargest
from heapq import nsmallest

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

    def getParameterSummary(self, asString=False):
        summary = {"n": self.numberOfParticles,
                    "k": self.k,
                    "noise": self.noise,
                    "speed": self.speed,
                    "radius": self.radius,
                    "neighbourSelectionMode": self.neighbourSelectionMode,
                    "domainSize": self.domainSize.tolist(),
                    "particleContainmentMode": self.particleContainmentMode}
        if asString:
            strPrep = [tup[0] + ": " + tup[1] for tup in summary.values()]
            return ", ".join(strPrep)
        return summary
    
    
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
            print(f"t={t}/{numIntervals-1}")

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
    
    def __normalizeOrientations(self,orientations):
        return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

    def __initializeState(self, domainSize, numberOfParticles):
        positions = domainSize*np.random.rand(numberOfParticles,len(domainSize))
        orientations = self.__normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        
        return positions, orientations

    def __selectNeighbours(self, positions, neighbourCandidates):        
        neighbours = []
        for i in range(0, self.numberOfParticles):
            candidates = [candIdx for candIdx in range(len(positions)) if neighbourCandidates[i][candIdx] == True and candIdx != i]
            iNeighbours = self.numberOfParticles * [False]
            match self.neighbourSelectionMode:
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM:
                    random.shuffle(candidates)
                    pickedNeighbours = candidates[:self.k]
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST:
                    currentParticlePosition = positions[i]
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nsmallest(self.k, candidateDistances, candidateDistances.get)
                case EnumNeighbourSelectionMode.NeighbourSelectionMode.FARTHEST:
                    currentParticlePosition = positions[i]
                    candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
                    pickedNeighbours = nlargest(self.k, candidateDistances, candidateDistances.get)
                case _:  # select all neighbours
                    pickedNeighbours = candidates
            iNeighbours[i] = True # should always consider the current orientation regardless of k or the neighbour selection method
            for neighbour in pickedNeighbours:
                iNeighbours[neighbour] = True
            neighbours.append(iNeighbours)
        return np.array(neighbours)