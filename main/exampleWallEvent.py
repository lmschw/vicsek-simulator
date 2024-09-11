import numpy as np
import codecs, json

from ExternalEventStimulusWallEvent import ExternalEventStimulusWallEvent
from VicsekWithNeighbourSelectionSwitchingCellBasedIndividualsDurationWithWallEvents import VicsekWithNeighbourSelection
import WallTypeBehaviour
import AnimatorMatplotlib
import Animator2DCircle

from EnumWallInfluenceType import WallInfluenceType
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumSwitchType import SwitchType
from EnumThresholdType import ThresholdType

import ServicePreparation
import ServiceSavedModel
import ServiceOrientations
import ServiceGeneral

path = "lei_2020/lei_2020_speeds.json"
obj_text = codecs.open(path, 'r', encoding='utf-8').read()
speeds = json.loads(obj_text)


expId = 11
speed = speeds[str(expId)]


domainSize = (2, 2)
n = 5
density = ServicePreparation.getDensity(domainSize, n)
radius = 20
#noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)
#eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)
noise = 0
eventNoise = None
k = 2
#nsm = NeighbourSelectionMode.FARTHEST

wallCenter = (1, 1)
wallRadius = 0.25
turnBy = 1

ks = [0, 1, 2, 3, 4]
noisePercentages = [0]
eventNoisePercentages = noisePercentages
turnByValues = [0.1, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]

iStart = 1
iStop = 11

for i in range(iStart, iStop):
        
        for k in ks:
                for noisePercentage in noisePercentages:
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                        for eventNoisePercentage in eventNoisePercentages:
                                eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
                                for turnBy in turnByValues:
                                        for nsm in [NeighbourSelectionMode.ALL,
                                                NeighbourSelectionMode.RANDOM,
                                                NeighbourSelectionMode.NEAREST,
                                                NeighbourSelectionMode.FARTHEST,
                                                NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
                                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
                                                ServiceGeneral.logWithTime(f"k={k}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}, nsm={nsm.value}")
                                                
                                                modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"lei_2020_expId={expId}.json", loadSwitchValues=False)
                                                times, pos, orients = simulationData
                                                tmax = len(times)
                                                circle = WallTypeBehaviour.WallTypeCircle("circle", 
                                                                                        WallInfluenceType.CLOSE_TO_BORDER, 
                                                                                        focusPoint=wallCenter, 
                                                                                        radius=wallRadius, 
                                                                                        influenceDistance=0.5)

                                                wallEvent = ExternalEventStimulusWallEvent(startTimestep=0,
                                                                                        endTimestep=tmax,
                                                                                        wallTypeBehaviour=circle,
                                                                                        noise=eventNoise,
                                                                                        turnBy=turnBy)

                                                simulator = VicsekWithNeighbourSelection(
                                                                                neighbourSelectionModel=nsm,
                                                                                domainSize=domainSize,
                                                                                speed=speed,
                                                                                radius=radius,
                                                                                noise=noise,
                                                                                numberOfParticles=n,
                                                                                k=k,
                                                                                switchingActive=False)



                                                switchTypeValues = n * [None]
                                                
                                                # savePath = f"test_lei_2020_expId=1-complete"

                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (2,2,2), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=23)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                

                                                initialState = (pos[0], orients[0], switchTypeValues)


                                                #initialState = ServicePreparation.createInitialStateInCircle(domainSize=domainSize, center=wallCenter, radius=wallRadius, isOrdered=False, numberOfParticles=n, startSwitchTypeValue=None)
                                                simulationData, colours, switchValues = simulator.simulate(
                                                                                        tmax=tmax,
                                                                                        wallEvents=[wallEvent],
                                                                                        initialState=initialState
                                                                                        )

                                                savePath = f"test_lei_2020_expId={expId}-start_nosw_{nsm.value}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}_{i}"
                                                modelParams = simulator.getParameterSummary()
                                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=modelParams)

                                                
                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=tmax)
                                                # preparedAnimator.setParams(modelParams)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                

        for k in ks:
                for noisePercentage in noisePercentages:
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                        for eventNoisePercentage in eventNoisePercentages:
                                eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
                                for turnBy in turnByValues:
                                        for nsmCombo in [[NeighbourSelectionMode.FARTHEST, NeighbourSelectionMode.NEAREST],
                                                [NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE]]:
                                                
                                                modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"lei_2020_expId={expId}.json", loadSwitchValues=False)
                                                times, pos, orients = simulationData
                                                tmax = len(times)
                                                orderValue, disorderValue = nsmCombo
                                                startValue = orderValue
                                                ServiceGeneral.logWithTime(f"nsmsw, k={k}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}, nsmo={orderValue.value}, nsmdo={disorderValue.value}")
                                                circle = WallTypeBehaviour.WallTypeCircle("circle", 
                                                                                        WallInfluenceType.CLOSE_TO_BORDER, 
                                                                                        focusPoint=wallCenter, 
                                                                                        radius=wallRadius, 
                                                                                        influenceDistance=0.5)

                                                wallEvent = ExternalEventStimulusWallEvent(startTimestep=0,
                                                                                        endTimestep=tmax,
                                                                                        wallTypeBehaviour=circle,
                                                                                        noise=eventNoise,
                                                                                        turnBy=turnBy)

                                                simulator = VicsekWithNeighbourSelection(
                                                                                neighbourSelectionModel=startValue,
                                                                                domainSize=domainSize,
                                                                                speed=speed,
                                                                                radius=radius,
                                                                                noise=noise,
                                                                                numberOfParticles=n,
                                                                                k=k,
                                                                                switchType=SwitchType.NEIGHBOUR_SELECTION_MODE,
                                                                                switchValues=(orderValue, disorderValue),
                                                                                thresholdType=ThresholdType.HYSTERESIS,
                                                                                orderThresholds=[0.1],
                                                                                numberPreviousStepsForThreshold=100
                                                                                )
                                                
                                                switchTypeValues = n * [startValue]

                                                savePath = f"test_lei_2020_expId=1-complete"

                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (2,2,2), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=23)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                

                                                initialState = (pos[0], orients[0], switchTypeValues)


                                                #initialState = ServicePreparation.createInitialStateInCircle(domainSize=domainSize, center=wallCenter, radius=wallRadius, isOrdered=False, numberOfParticles=n, startSwitchTypeValue=None)
                                                simulationData, colours, switchValues = simulator.simulate(
                                                                                        tmax=tmax,
                                                                                        wallEvents=[wallEvent],
                                                                                        initialState=initialState
                                                                                        )

                                                savePath = f"test_lei_2020_expId={expId}-start_nsmsw_o={orderValue.value}_do={disorderValue.value}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_k={k}_{i}"
                                                modelParams = simulator.getParameterSummary()
                                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=modelParams)

                                                
                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=tmax)
                                                # preparedAnimator.setParams(modelParams)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                
        
        for kCombo in [[5,1]]:
                for noisePercentage in noisePercentages:
                        noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)
                        for eventNoisePercentage in eventNoisePercentages:
                                eventNoise = ServicePreparation.getNoiseAmplitudeValueForPercentage(eventNoisePercentage)
                                for turnBy in turnByValues:
                                        for nsm in [NeighbourSelectionMode.ALL,
                                                NeighbourSelectionMode.RANDOM, 
                                                NeighbourSelectionMode.FARTHEST,
                                                NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]:
                                                modelParams, simulationData, colours = ServiceSavedModel.loadModel(f"lei_2020_expId={expId}.json", loadSwitchValues=False)
                                                times, pos, orients = simulationData
                                                tmax = len(times)
                                                
                                                orderValue, disorderValue = kCombo
                                                startValue = orderValue
                                                ServiceGeneral.logWithTime(f"ksw, nsm={nsm.value}, noise={noisePercentage}, eN={eventNoisePercentage}, turnBy={turnBy}, nsmo={orderValue}, nsmdo={disorderValue}")
                                                circle = WallTypeBehaviour.WallTypeCircle("circle", 
                                                                                        WallInfluenceType.CLOSE_TO_BORDER, 
                                                                                        focusPoint=wallCenter, 
                                                                                        radius=wallRadius, 
                                                                                        influenceDistance=0.5)

                                                wallEvent = ExternalEventStimulusWallEvent(startTimestep=0,
                                                                                        endTimestep=tmax,
                                                                                        wallTypeBehaviour=circle,
                                                                                        noise=eventNoise,
                                                                                        turnBy=turnBy)

                                                simulator = VicsekWithNeighbourSelection(
                                                                                neighbourSelectionModel=nsm,
                                                                                domainSize=domainSize,
                                                                                speed=speed,
                                                                                radius=radius,
                                                                                noise=noise,
                                                                                numberOfParticles=n,
                                                                                k=startValue,
                                                                                switchType=SwitchType.K,
                                                                                switchValues=(orderValue, disorderValue),
                                                                                thresholdType=ThresholdType.HYSTERESIS,
                                                                                orderThresholds=[0.1],
                                                                                numberPreviousStepsForThreshold=100
                                                                                )

                                                switchTypeValues = n * [startValue]

                                                # savePath = f"test_lei_2020_expId=1-complete"

                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (2,2,2), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=23)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                

                                                initialState = (pos[0], orients[0], switchTypeValues)


                                                #initialState = ServicePreparation.createInitialStateInCircle(domainSize=domainSize, center=wallCenter, radius=wallRadius, isOrdered=False, numberOfParticles=n, startSwitchTypeValue=None)
                                                simulationData, colours, switchValues = simulator.simulate(
                                                                                        tmax=tmax,
                                                                                        wallEvents=[wallEvent],
                                                                                        initialState=initialState
                                                                                        )

                                                savePath = f"test_lei_2020_expId={expId}-start_ksw_o={orderValue}_do={disorderValue}_noise={noise}_eventNoise={eventNoise}_turnBy={turnBy}_nsm={nsm.value}_{i}"
                                                modelParams = simulator.getParameterSummary()
                                                ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, path=f"{savePath}.json", modelParams=modelParams)

                                                
                                                # # Initalise the animator
                                                # animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

                                                # # prepare the animator
                                                # preparedAnimator = animator.prepare(Animator2DCircle.Animator2D(wallCenter, wallRadius), frames=tmax)
                                                # preparedAnimator.setParams(modelParams)

                                                # preparedAnimator.saveAnimation(f"{savePath}.mp4")
                                                