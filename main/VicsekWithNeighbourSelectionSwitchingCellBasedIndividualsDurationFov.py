import numpy as np

import DefaultValues as dv
import ServiceOrientations

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration

"""
Version of the modified Vicsek model tthat includes an option for setting the field of vision for every particle.
"""
class VicsekWithNeighbourSelection(VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection):

    def __init__(self, neighbourSelectionModel, domainSize=dv.DEFAULT_DOMAIN_SIZE_2D, speed=dv.DEFAULT_SPEED, 
                 radius=dv.DEFAULT_RADIUS, noise=dv.DEFAULT_NOISE, numberOfParticles=dv.DEFAULT_NUM_PARTICLES, 
                 k=dv.DEFAULT_K_NEIGHBOURS, showExample=dv.DEFAULT_SHOW_EXAMPLE_PARTICLE, numCells=None, 
                 switchType=None, switchValues=(None, None), thresholdType=None, orderThresholds=None, 
                 numberPreviousStepsForThreshold=10, switchBlockedAfterEventTimesteps=-1,
                 degreesOfVision=2*np.pi, occlusionActive=False, switchingActive=True, returnHistories=True, 
                 logPath=None, logInterval=1):
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
            - degreesOfVision (int) [optional]: the angle of the field of vision. The center of the field of vision is always the direction of the orientation
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
                         switchingActive=switchingActive,
                         returnHistories=returnHistories,
                         logPath=logPath,
                         logInterval=logInterval)
        self.degreesOfVision = degreesOfVision
    
    def isVisibleToParticle(self, particleIdx, candidateIdx, positions, orientations, neighbourCandidates):
        """
        Checks if another particle is visible to the current particle. Checks if the other particle is within the field of vision.
        Optionally also checks if the particle is hidden.

        Params:
            - particleIdx (int): The index of the current particle
            - candidateIdx (int): The index of the other particle that should be checked
            - positions (array of arrays of floats): the position of every particle at the current timestep
            - orientations (array of arrays of floats): the orientation of every particle at the current timestep
            - neighbourCandidates (array of int): all particles within the radius

        Returns:
            A boolean describing whether the other particle can be seen by the current particle.
        """
        minAngle, maxAngle = ServiceOrientations.determineMinMaxAngleOfVision(orientations[particleIdx], self.degreesOfVision)
        isVisible = ServiceOrientations.isInFieldOfVision(positionParticle=positions[particleIdx], positionCandidate=positions[candidateIdx], minAngle=minAngle, maxAngle=maxAngle)
        if self.occlusionActive:
            isVisible = isVisible and not ServiceOrientations.isParticleOccluded(particleIdx=particleIdx, otherIdx=candidateIdx, positions=positions, candidates=neighbourCandidates)
        return isVisible
