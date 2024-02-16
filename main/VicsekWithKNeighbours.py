"""
This class serves to instantiate a simulated standard Vicsek model.
"""

import numpy as np
import random

import DefaultValues as dv

class VicsekWithKNeighbours:
    def __init__(self, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, k=dv.DEFAULT_K_NEIGHBOURS):
        """
        Initialize the model. Note that the domainSize does not have a default value as this model is used for both 2D and 3D
        """
        self.domainSize = np.asarray(domainSize)
        self.speed = speed
        self.radius = radius
        self.noise = noise
        self.numberOfParticles = numberOfParticles
        self.k = k

    def simulate(self, initialState=(None, None), dt=None, tmax=None):
        """
        Simulates the Vicsek model
        """
        positions, orientations = initialState
        
        if None in initialState:
            positions, orientations = self.__initializeState(self.domainSize, self.numberOfParticles);
            
        if dt is None:
            dt = 10**(-2)*(np.max(self.domainSize)/self.speed)
        
        if tmax is None:
            tmax = (10**3)*dt

        t=0
        num_intervals=int(tmax/dt+1)
        
        positionsHistory = np.zeros((num_intervals,self.numberOfParticles,len(self.domainSize)))
        orientationsHistory = np.zeros((num_intervals,self.numberOfParticles,len(self.domainSize)))
        
        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        
        for it in range(num_intervals):
            print("Time step: ", t)
            positions += dt*(self.speed*orientations)
            positions += -self.domainSize*np.floor(positions/self.domainSize)

            orientations = self.calculateMeanOrientations(positions, orientations)
            orientations = self.__normalizeOrientations(orientations+self.generateNoise())

            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations

            t+=dt


        return dt*np.arange(num_intervals), positionsHistory, orientationsHistory

    def calculateMeanOrientations(self, positions, orientations):
        rij=positions[:,np.newaxis,:]-positions
    
        newOrientations = []
        for particleIdx in range(len(rij)):
            neighbourIndices = self.__chooseNeighbours(particleIdx, positions)
            #newOrientations.append(self.__computeOrientation(particleIdx, neighbourIndices, orientations))
            if neighbourIndices != []:
                neighbourOrientations = [orientations[i] for i in neighbourIndices]
                newOrientations.append(np.average(neighbourOrientations, axis=0))
            else:
                newOrientations.append(orientations[particleIdx])
        #return self.__normalizeOrientations(newOrientations)
        return newOrientations


    """
        def calculateMeanOrientations(self, positions, orientations):
        rij=positions[:,np.newaxis,:]-positions
        #rij=rij[~np.eye(rij.shape[0],dtype=bool),:].reshape(rij.shape[0],rij.shape[0]-1,-1) #remove i<>i interaction
    
        rij = rij - self.domainSize*np.rint(rij/self.domainSize) #minimum image convention

        rij2 = np.sum(rij**2,axis=2)
        neighbours = (rij2 <= self.radius**2)
        summedOrientations = np.sum(neighbours[:,:,np.newaxis]*orientations[np.newaxis,:,:],axis=1)
        return self.__normalizeOrientations(summedOrientations)
    """
    def generateNoise(self):
        return np.random.normal(scale=self.noise, size=(self.numberOfParticles, len(self.domainSize)))

    def __normalizeOrientations(self, orientations):
        return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

    def __initializeState(self, domainSize, numberOfParticles):
        positions = domainSize*np.random.rand(numberOfParticles,len(domainSize))
        orientations = self.__normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        
        return positions, orientations

    def __chooseNeighbours(self, particleIdx, positions):
        """
        returns the indices of random k nearest neighbours
        """
        particlePosition = positions[particleIdx]

        candidates = [candIdx for candIdx in range(len(positions)-1) if self.__isNeighbour(particlePosition, positions[candIdx])]
        random.shuffle(candidates)
        return candidates[:self.k]


    def __isNeighbour(self, particle, candidate):
        # Two particles cannot be superposed in the same place. Therefore, if they share the same coordinates, they are identical.
        # Therefore, they cannot be neighbours
        if particle[0] == candidate[0] and particle[1] == candidate[1]:
            return False
        return ((candidate[0] - particle[0])**2 + (candidate[1] - particle[1])**2) <= self.radius

    def __computeOrientation(particleIndex, neighbourIndices, orientations):
        neighbourOrientations = [orientations[i] for i in neighbourIndices]
        return (np.average(neighbourOrientations, axis=0), np.average(neighbourOrientations, axis=1))
