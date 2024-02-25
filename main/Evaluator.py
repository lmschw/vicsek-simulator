import numpy as np
import matplotlib.pyplot as plt

import EnumMetrics as metrics

class Evaluator(object):
    def __init__(self, simulationData, modelParams, metric):
        self.time, self.positions, self.orientations, self.colours = simulationData
        self.modelParams = modelParams
        self.metric = metric

    def evaluate(self):
        valuesPerTimeStep = {}
        n = self.modelParams["n"]
        for i in range(len(self.time)):
            match self.metric:
                case metrics.Metrics.ORDER:
                    sumOrientation = self.orientations[i][0]
                    for j in range(1, n):
                        sumOrientation += self.orientations[i][j]
                    valuesPerTimeStep[self.time[i]] = np.sqrt(sumOrientation[0]**2 + sumOrientation[1]**2) / n
        return valuesPerTimeStep
    
    def visualize(self, data, savePath=None):
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.title(f"""Model: n={self.modelParams["n"]}, k={self.modelParams["k"]}, noise={self.modelParams["noise"]}, radius={self.modelParams["radius"]}, speed={self.modelParams["speed"]}, \nneighbour selection: {self.modelParams["neighbourSelectionMode"]}\nMetric: {self.metric.name}""")
        
        if savePath != None:
            plt.savefig(savePath)
        
        plt.show()
    
    def evaluateAndVisualize(self, savePath=None):
        self.visualize(self.evaluate(), savePath)

