import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEventDuration import ExternalStimulusOrientationChangeEventDuration
import AnimatorMatplotlib
import Animator2D

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType
from EnumEventEffect import EventEffect
from EnumThresholdType import ThresholdType
from EnumMovementPattern import MovementPattern

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates data with a moving predator.
--------------------------------------------------------------------------------
"""

# base setup
tmax = 15000 # how many timesteps will be performed
domainSize = (100, 100) # the x and y dimensions of the domain
density = 0.01 # how densely the particles are packed into the domain
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize)) # the total number of particles in the domain
radius = 10 # the perception radius
noisePercentage = 1 # how much noise is present in percent
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
thresholdType = ThresholdType.HYSTERESIS # how the individual particles decide if they should update their switch value selection
thresholds = [0.1] # defines the lower and upper thresholds or the difference depending on the thresholdType
blockSteps = -1 # how many timesteps have to pass before a particle can change their mind again after the event has affected it
numberOfPreviousSteps = 100 # how many previous steps are considered to compute the average of the local order. This is used to compare with the thresholds
initialStateString = "random" # either "random" or "ordered", indicates how the particles are aligned initially

# switch type configuration
switchType = SwitchType.NEIGHBOUR_SELECTION_MODE # what value we are switching on, either the neighbour selection mode or k
k = 1 # any value, k = 1 usually yields good results
orderValue = NeighbourSelectionMode.FARTHEST # example value. ALL, RANDOM, HIGHEST_ORIENTATION_DIFFERENCE and FARTHEST cause order
disorderValue = NeighbourSelectionMode.NEAREST # example value. LEAST_ORIENTATION_DIFFERENCE and NEAREST cause disorder

"""
# example if you want to switch on k
switchType = SwitchType.K # what value we are switching on, either the neighbour selection mode or k
neighbourSelectionMode = NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE # this needs to be either LEAST_ORIENTATION_DIFFERENCE or NEAREST when switching on k otherwise the swarm cannot decide to go to disorder
orderValue = 5 # higher values of k tend to cause order but feel free to experiment
disorderValue = 1 # lower values of k tend to cause disorder but feel free to experiment
"""

# event setup
eventEffect = EventEffect.AWAY_FROM_ORIGIN # this is the PREDATOR behaviour, so this should not be changed
distributionType = DistributionType.LOCAL_SINGLE_SITE # if the effect is global, particles are picked out randomly unless you set percentage = 100. then the whole swarm will be affected
areas = [(20, 20, radius)] # the area that is affected by the event initially: [(xPointOfOriginAtStart, xPointOfOriginAtStart, radius)]
percentage = 100 # how much of the swarm is potentially affected. You can play with this. However, it is the percentage compared to the whole swarm. So if the event area only contains 30% of all particles and you set it to 30%, all of them will be affected currently
angle = 180 # not necessary for predator behaviour but currently not optional for the event specification
movementPattern = MovementPattern.PURSUIT_NEAREST # how the predator moves
startTimestep = 0 # first timestep at which the predator appears
endTimestep = tmax # last timestep where the predator is active

for i in range(1,2):
    if initialStateString == "ordered":
        startValue = orderValue
    else:
        startValue = disorderValue

    event1 = ExternalStimulusOrientationChangeEventDuration(
                                        startTimestep=startTimestep, 
                                        endTimestep=endTimestep,
                                        percentage=percentage,
                                        angle=angle,
                                        eventEffect=eventEffect,
                                        movementPattern=movementPattern,
                                        movementSpeed=1,
                                        perceptionRadius=radius,
                                        domainSize=domainSize,
                                        distributionType=distributionType,
                                        areas=areas
                                    )

    events = [event1]

    startRun = time.time()

    if initialStateString == "ordered":
        initialState = ServicePreparation.createOrderedInitialDistributionEquidistancedIndividual(startValue, domainSize, n)

    simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDuration.VicsekWithNeighbourSelection(
                                                                    neighbourSelectionModel=startValue, # if you switch on k, this needs to be neighbourSelectionModel=neighbourSelectionMode
                                                                    domainSize=domainSize, 
                                                                    numberOfParticles=n, 
                                                                    k=k, # if you switch on k, this needs to be k=startValue
                                                                    noise=noise, 
                                                                    radius=radius,
                                                                    switchType=switchType,
                                                                    switchValues=(orderValue, disorderValue),
                                                                    thresholdType=thresholdType,
                                                                    orderThresholds=thresholds,
                                                                    numberPreviousStepsForThreshold=numberOfPreviousSteps,
                                                                    switchBlockedAfterEventTimesteps=blockSteps
                                                                    )
    if initialStateString == "ordered":
        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, initialState=initialState, events=events)
    else:
        simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

    # Save model values for future use
    eventsString = "_".join([event.getShortPrintVersion() for event in events])
    savePath = f"test_predator_{eventsString}_{i}" # if you get a bug about not finding the file, the savePath is too long

    ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"{savePath}.json", modelParams=simulator.getParameterSummary())

    """
    # CREATE VIDEO
    # Initalise the animator
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
    preparedAnimator.setParams(simulator.getParameterSummary())
    preparedAnimator.saveAnimation(f"{savePath}.mp4")
    """

    endRun = time.time()
    ServiceGeneral.logWithTime(f"Completed i={i}, r={radius}, thresholds={thresholds}, density={density} in {ServiceGeneral.formatTime(endRun-startRun)}")
