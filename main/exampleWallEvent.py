import numpy as np

from ExternalEventStimulusWallEvent import ExternalEventStimulusWallEvent
from VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDurationWithWallEvents import VicsekWithNeighbourSelection
import WallTypeBehaviour
import AnimatorMatplotlib
import Animator2DCircle

from EnumWallInfluenceType import WallInfluenceType
from EnumNeighbourSelectionMode import NeighbourSelectionMode

import ServicePreparation
import ServiceSavedModel
import ServiceOrientations

tmax = 1000

domainSize = (50, 50)
n = 5
density = ServicePreparation.getDensity(domainSize, n)
speed = 0.1
radius = 10
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)
k = 1
nsm = NeighbourSelectionMode.FARTHEST

wallCenter = (20, 20)
wallRadius = 10

circle = WallTypeBehaviour.WallTypeCircle("circle", 
                                          WallInfluenceType.CLOSE_TO_BORDER, 
                                          focusPoint=wallCenter, 
                                          radius=wallRadius, 
                                          influenceDistance=5)

wallEvent = ExternalEventStimulusWallEvent(startTimestep=0,
                                           endTimestep=tmax,
                                           wallTypeBehaviour=circle)

simulator = VicsekWithNeighbourSelection(
                             neighbourSelectionModel=nsm,
                             domainSize=domainSize,
                             speed=speed,
                             radius=radius,
                             noise=noise,
                             numberOfParticles=n,
                             k=k,
                             switchingActive=False)

initialState = ServicePreparation.createInitialStateInCircle(domainSize=domainSize, center=wallCenter, radius=wallRadius, isOrdered=False, numberOfParticles=n, startSwitchTypeValue=None)
simulationData, colours, switchValues = simulator.simulate(
                                        tmax=tmax,
                                        wallEvents=[wallEvent],
                                        initialState=initialState
                                        )

savePath = f"test_with_wallevent"
modelParams = simulator.getParameterSummary()
ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=modelParams)

# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(), frames=tmax)
preparedAnimator.setParams(modelParams)

preparedAnimator.saveAnimation(f"{savePath}.mp4")