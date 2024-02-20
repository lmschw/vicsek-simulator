"""
This class serves to instantiate a simulated standard Vicsek model.
"""

import numpy as np
import random

import DefaultValues as dv
import DisplayModes

class VicsekWithKNeighboursWithModes:
    def __init__(self, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, k1=dv.DEFAULT_K_MODE1, k2=dv.DEFAULT_K_MODE2, particlesAllowedToLeave=dv.DEFAULT_PARTICLES_ALLOWED_TO_LEAVE, displayMode=DisplayModes.DisplayModes.EXCITEMENT):
        """
        Initialize the model. Note that the domainSize does not have a default value as this model is used for both 2D and 3D
        """
        self.domainSize = np.asarray(domainSize)
        self.speed = speed
        self.radius = radius
        self.noise = noise
        self.numberOfParticles = numberOfParticles
        self.k1 = k1
        self.k2 = k2
        self.particlesAllowedToLeave = particlesAllowedToLeave
        self.displayMode = displayMode
        self.threshold = 0.5

    def simulate(self, initialState=(None, None), dt=None, tmax=None):
        """
        Simulates the Vicsek model
        """
        positions, orientations = initialState
        
        if None in initialState:
            positions, orientations = self.__initializeState(self.domainSize, self.numberOfParticles)
            excitations = self.numberOfParticles * [0]
            
        if dt is None:
            dt = 10**(-2)*(np.max(self.domainSize)/self.speed)
        
        if tmax is None:
            tmax = (10**3)*dt

        t=0
        numIntervals=int(tmax/dt+1)

        if self.displayMode == DisplayModes.DisplayModes.EXAMPLE:
            self._exampleIdx = random.randint(0, self.numberOfParticles-1)
        
        positionsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        orientationsHistory = np.zeros((numIntervals,self.numberOfParticles,len(self.domainSize)))
        coloursHistory = numIntervals * [self.numberOfParticles * ['k']]
        excitationHistory = numIntervals * [self.numberOfParticles * [0]]
        
        positionsHistory[0,:,:]=positions
        orientationsHistory[0,:,:]=orientations
        
        excitations[random.randint(0, self.numberOfParticles)] = 1 # excite one particle to start with

        for it in range(numIntervals):
            print("Time step: ", t)
            print("Excitations:", excitations)
            #print("Positions: ", positions)
            #print("Positions: ", [pos for pos in positions if pos[0] < 0 or pos[0] > self.domainSize[0] or pos[1] < 0 or pos[1] > self.domainSize[1]])
            colours=self.numberOfParticles * ['k']
            positions += dt*(self.speed*orientations)
            if not self.particlesAllowedToLeave:
                self.__repelLeavingParticles(positions, orientations)
                    
            self.updateParticleStats(positions, orientations, colours, excitations)
            orientations = self.__normalizeOrientations(orientations+self.generateNoise())

            positionsHistory[it,:,:]=positions
            orientationsHistory[it,:,:]=orientations
            coloursHistory[it]=colours
            excitationHistory[it]=excitations

            t+=dt


        return dt*np.arange(numIntervals), positionsHistory, orientationsHistory, coloursHistory

    def updateParticleStats(self, positions, orientations, colours, excitations):
        rij=positions[:,np.newaxis,:]-positions
    
        newOrientations = []
        for particleIdx in range(len(rij)):
            if excitations[particleIdx] > self.threshold:
                k = self.k2
            else:
                k = self.k1
            neighbourIndices = self.__chooseNeighbours(particleIdx, positions, k)
            if neighbourIndices != []:
                neighbourOrientations = [orientations[i] for i in neighbourIndices]
                newOrientations.append(np.average(neighbourOrientations, axis=0))
                neighbourExcitement = 0
                for neighbourIdx in neighbourIndices:
                    neighbourExcitement += excitations[neighbourIdx]
                if(neighbourExcitement > excitations[particleIdx]):
                    excitations[particleIdx] = min( excitations[particleIdx] + neighbourExcitement / 10, 1)
                else:
                    excitations[particleIdx] = max(excitations[particleIdx] - neighbourExcitement, 0)
            else:
                newOrientations.append(orientations[particleIdx])

            # set colours in case we want to see a highlighted example
            if self.displayMode == DisplayModes.DisplayModes.EXAMPLE and self._exampleIdx == particleIdx:
                colours[particleIdx] = 'r'
                for neighbourIdx in neighbourIndices:
                    colours[neighbourIdx] = 'y'
            elif self.displayMode == DisplayModes.DisplayModes.EXCITEMENT and excitations[particleIdx] > self.threshold:
                colours[particleIdx] = 'y'
        return newOrientations

    def generateNoise(self):
        return np.random.normal(scale=self.noise, size=(self.numberOfParticles, len(self.domainSize)))

    def __normalizeOrientations(self, orientations):
        return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

    def __initializeState(self, domainSize, numberOfParticles):
        positions = domainSize*np.random.rand(numberOfParticles,len(domainSize))
        orientations = self.__normalizeOrientations(np.random.rand(numberOfParticles, len(domainSize))-0.5)
        
        return positions, orientations

    def __chooseNeighbours(self, particleIdx, positions, k):
        """
        returns the indices of random k nearest neighbours
        """
        particlePosition = positions[particleIdx]

        candidates = [candIdx for candIdx in range(len(positions)-1) if self.__isNeighbour(particlePosition, positions[candIdx])]
        random.shuffle(candidates)
        return candidates[:k]


    def __isNeighbour(self, particle, candidate):
        # Two particles cannot be superposed in the same place. Therefore, if they share the same coordinates, they are identical.
        # Therefore, they cannot be neighbours
        if particle[0] == candidate[0] and particle[1] == candidate[1]:
            return False
        return ((candidate[0] - particle[0])**2 + (candidate[1] - particle[1])**2) <= self.radius

    def __repelLeavingParticles(self, positions, orientations):
        for posIdx in range(len(positions)):
            xMax = self.domainSize[0]
            xPos = positions[posIdx][0]
            yMax = self.domainSize[1]
            yPos = positions[posIdx][1]
            if xPos > xMax:
                orientations[posIdx][0] *= -1
                positions[posIdx][0] = xMax
            elif xPos < 0:
                orientations[posIdx][0] *= -1
                positions[posIdx][0] = 0
            if yPos > yMax:
                orientations[posIdx][1] *= -1
                positions[posIdx][1] = yMax
            elif yPos < 0:
                orientations[posIdx][1] *= -1
                positions[posIdx][1] = 0
