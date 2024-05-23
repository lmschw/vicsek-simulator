import time

import ServiceImages
import ServiceGeneral

radiusVals = [5, 10, 20, 30, 50, 100]
densityVals = [0.01, 0.03, 0.05, 0.07, 0.09]
thresholdVals = [[0.1,0.9], [0.2, 0.9], [0.3, 0.9], [0.4, 0.9], [0.5, 0.9], [0.6,0.9], [0.7,0.9]]

type = "minorder"
initialState= "ordered"
startValue = 5

startTotal = time.time()
for i in range(1, 4):
    startI = time.time()
    for threshold in thresholdVals:
        startTh = time.time()
        ServiceGeneral.logWithTime(f"Started i={i}, threshold={threshold}")
        savePath = f"radius-vs-density-{type}-threshold={threshold}-i={i}.svg"
        ServiceImages.createDensityVsRadiusPlot(type=type, threshold=threshold, radiusVals=radiusVals, densityVals=densityVals, initialState=initialState, startValue=startValue, i=i, savePath=savePath)
        endTh = time.time()
        ServiceGeneral.logWithTime(f"Completed i={i}, threshold={threshold} in {ServiceGeneral.formatTime(endTh-startTh)}")
    endI = time.time()
    ServiceGeneral.logWithTime(f"Completed i={i} in {ServiceGeneral.formatTime(endI-startI)}")

endTotal = time.time()
ServiceGeneral.logWithTime(f"Completed in {ServiceGeneral.formatTime(endTotal-startTotal)}")


