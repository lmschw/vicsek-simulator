
import numpy as np
import EnumMetrics as metrics

def evaluateSingleTimestep(positions, orientations, metric):
     n = len(positions)
     match metric:
        case metrics.Metrics.ORDER:
            sumOrientation = orientations[0]
            for j in range(1, n):
                sumOrientation += orientations[j]
            return np.sqrt(sumOrientation[0]**2 + sumOrientation[1]**2) / n