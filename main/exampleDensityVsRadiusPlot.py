import time

import ServiceImages
import ServiceGeneral

from EnumThresholdType import ThresholdType

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates comparison matrix with minimum/maximum local order for radius vs. density,
threshold vs. density and threshold vs. radius
--------------------------------------------------------------------------------
"""

radiusVals = [5, 10, 20, 30, 50, 100]
densityVals = [0.01, 0.03, 0.05, 0.07, 0.09]
thresholdVals = [[0.1], [0.2], [0.3], [0.4], [0.5]]


startTotal = time.time()
for thresholdType in [ThresholdType.TWO_THRESHOLDS, ThresholdType.TWO_THRESHOLDS_SIMPLE, ThresholdType.TWO_THRESHOLDS_SIMPLE_REVERSE]:
    for initialState in ["ordered", "random"]:
        if initialState == "ordered":
            type = "minorder"
            startValue = 5
        else:
            type = "maxorder"
            startValue = 1

        for i in range(1, 3):
            startI = time.time()
            for threshold in thresholdVals:
                startTh = time.time()
                ServiceGeneral.logWithTime(f"Started i={i}, threshold={threshold}")
                savePath = f"radius-vs-density-{initialState}-{type}-{thresholdType.value}-threshold={threshold}-i={i}.svg"
                ServiceImages.createDensityVsRadiusPlot(type=type, thresholdType=thresholdType, threshold=threshold, radiusVals=radiusVals, densityVals=densityVals, initialState=initialState, startValue=startValue, i=i, savePath=savePath)
                endTh = time.time()
                ServiceGeneral.logWithTime(f"Completed i={i}, threshold={threshold} in {ServiceGeneral.formatTime(endTh-startTh)}")
            endI = time.time()
            ServiceGeneral.logWithTime(f"Completed radius-vs-density i={i} in {ServiceGeneral.formatTime(endI-startI)}")

            startI = time.time()
            for radius in radiusVals:
                startTh = time.time()
                ServiceGeneral.logWithTime(f"Started i={i}, threshold={threshold}")
                savePath = f"threshold-vs-density-{initialState}-{type}-{thresholdType.value}-radius={radius}-i={i}.svg"
                ServiceImages.createDensityVsThresholdPlot(type=type, thresholdType=thresholdType, radius=radius, thresholdVals=thresholdVals, densityVals=densityVals, initialState=initialState, startValue=startValue, i=i, savePath=savePath)
                endTh = time.time()
                ServiceGeneral.logWithTime(f"Completed threshold-vs-density i={i}, threshold={threshold} in {ServiceGeneral.formatTime(endTh-startTh)}")
            endI = time.time()
            ServiceGeneral.logWithTime(f"Completed i={i} in {ServiceGeneral.formatTime(endI-startI)}")

            startI = time.time()
            for density in densityVals:
                startTh = time.time()
                ServiceGeneral.logWithTime(f"Started i={i}, threshold={threshold}")
                savePath = f"threshold-vs-radius-{initialState}-{type}-{thresholdType.value}-radius={radius}-i={i}.svg"
                ServiceImages.createThresholdVsRadiusPlot(type=type, thresholdType=thresholdType, density=density, thresholdVals=thresholdVals, radiusVals=radiusVals, initialState=initialState, startValue=startValue, i=i, savePath=savePath)
                endTh = time.time()
                ServiceGeneral.logWithTime(f"Completed threshold-vs-radius  i={i}, threshold={threshold} in {ServiceGeneral.formatTime(endTh-startTh)}")
            endI = time.time()
            ServiceGeneral.logWithTime(f"Completed i={i} in {ServiceGeneral.formatTime(endI-startI)}")

endTotal = time.time()
ServiceGeneral.logWithTime(f"Completed in {ServiceGeneral.formatTime(endTotal-startTotal)}")


