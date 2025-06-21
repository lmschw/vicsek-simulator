import ServiceOrientations

import ServiceVicsekHelper
import ServiceSavedModel
import ServiceMetric
import ServicePreparation

import numpy as np

"""
orientations = ServiceVicsekHelper.normalizeOrientations(np.random.rand(1, 2)-0.5)
print(orientations)
angle = ServiceOrientations.computeCurrentAngle(orientations[0])
print(angle)
print(ServiceOrientations.computeUvCoordinates(angle))

# add the event angle to the current angle
newAngle = (angle + 2*np.pi) % (2 *np.pi)

print(ServiceOrientations.computeUvCoordinates(newAngle))
"""


modelParams, simulationData, colours, switchTypeValues = ServiceSavedModel.loadModel("test_debug-ordered_align_fixed_angle=pi_tmax=1500_speed=1_psteps=1_1.json", loadSwitchValues=True)
times, positions, orientations = simulationData
fixedAngle = np.pi
noise = ServicePreparation.getNoiseAmplitudeValueForPercentage(1)

print(ServiceMetric.checkTurnSuccess(orientations=orientations, fixedAngle=fixedAngle, noise=noise, eventStartTimestep=1000, interval=100))