import numpy as np
import matplotlib.pyplot as plt

import EnumMetrics as metrics

class Evaluator(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for a single model.
    """
    def __init__(self, simulationData, modelParams, metric):
        """
        Initialises the evaluator.

        Parameters:
            - simulationData (time array, positions array, orientation array, colours array): contains all the simulation data
            - modelParams (dictionary): contains the model parameters
            - metric (EnumMetrics.Metrics): the metric according to which the model's performances should be evaluated
        
        Returns:
            Nothing.
        """
        self.time, self.positions, self.orientations, self.colours = simulationData
        self.modelParams = modelParams
        self.metric = metric

    def evaluate(self):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
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
        """
        Visualizes and optionally saves the results of the evaluation as a graph.

        Parameters:
            - data (dictionary): a dictionary with the time step as key and the model's result as values
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.title(f"""Model: n={self.modelParams["n"]}, k={self.modelParams["k"]}, noise={self.modelParams["noise"]}, radius={self.modelParams["radius"]}, speed={self.modelParams["speed"]}, \nneighbour selection: {self.modelParams["neighbourSelectionMode"]}\nMetric: {self.metric.name}""")
        
        if savePath != None:
            plt.savefig(savePath)
        
        plt.show()
    
    def evaluateAndVisualize(self, savePath=None):
        """
        Evaluates and subsequently visualises the results for a single model.

        Parameters:
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        self.visualize(self.evaluate(), savePath)

