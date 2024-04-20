import time

import VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
import ServicePreparation
import ServiceGeneral
from ExternalStimulusOrientationChangeEvent import ExternalStimulusOrientationChangeEvent
import AnimatorMatplotlib
import Animator2D

from EnumSwitchType import SwitchType
from EnumDistributionType import DistributionType

domainSize = (100, 100)
density = 0.01
radius = 10
noisePercentage = 0
neighbourSelectionMode = NeighbourSelectionMode.NEAREST
tmax = 2000
i = 1

switchType = SwitchType.K
orderValue = 5
disorderValue = 1
startValue = orderValue
orderThreshold = 0.05


# 180° switch: [1.5,0.5]

event1 = ExternalStimulusOrientationChangeEvent(timestep=1000,
                                                percentage=20,
                                                angle=180,
                                                distributionType=DistributionType.GLOBAL
                                                )

events = [event1]
# RANDOM START

startRun = time.time()
ServiceGeneral.logWithTime(f"Start random start i={i}, noiseP={noisePercentage}, density={density}, neighbourSelectionMode={neighbourSelectionMode.name}, orderVal={orderValue}, disorderVal={disorderValue}, threshold={orderThreshold}, startValue={startValue}")
n = int(ServicePreparation.getNumberOfParticlesForConstantDensity(density, domainSize))
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(noisePercentage)

simulator = VicsekWithNeighbourSelectionSwitchingCellBasedIndividuals.VicsekWithNeighbourSelection(neighbourSelectionMode, 
                                                                domainSize=domainSize, 
                                                                numberOfParticles=n, 
                                                                k=startValue, 
                                                                noise=noise, 
                                                                radius=radius,
                                                                switchType=switchType,
                                                                switchValues=(orderValue, disorderValue))
simulationData, colours, switchValues = simulator.simulate(tmax=tmax, events=events)

# Save model values for future use

#ServiceSavedModel.saveModel(simulationData=simulationData, colours=colours, switchValues=switchValues, path=f"individual_random-start_switchType={switchType.name}_orderV={orderValue}_disorderV={disorderValue}_startV={startValue}_tmax={tmax}_n={n}_density={density}_mode={neighbourSelectionMode.name}_noise={noisePercentage}%_orderthreshold={orderThreshold}_{i}.json", modelParams=simulator.getParameterSummary())
endRun = time.time()
ServiceGeneral.logWithTime(f"Completed random start i={i}, noiseP={noisePercentage}, density={density},  neighbourSelectionMode={neighbourSelectionMode.name}, orderK={orderValue}, disorderK={disorderValue}, threshold={orderThreshold}, startValue={startValue} in {ServiceGeneral.formatTime(endRun-startRun)}")
# Initalise the animator
animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

# prepare the animator
preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=tmax)
preparedAnimator.setParams(simulator.getParameterSummary())

preparedAnimator.saveAnimation('ind_switch_test.mp4')

# Display Animation
#preparedAnimator.showAnimation()