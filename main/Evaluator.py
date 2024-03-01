import numpy as np
import matplotlib.pyplot as plt

import ServiceMetric
import EnumMetrics

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
        self.time, self.positions, self.orientations = simulationData
        self.modelParams = modelParams
        self.metric = metric

        if metric in [EnumMetrics.Metrics.CLUSTER_NUMBER, EnumMetrics.Metrics.CLUSTER_SIZE]:
            self.radius = modelParams["radius"]
        else:
            self.radius = None
            

    def evaluate(self):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
        valuesPerTimeStep = {}
        for i in range(len(self.time)):
            if i % 100 == 0:
                print(f"evaluating {i}/{len(self.time)}")
            valuesPerTimeStep[self.time[i]] = ServiceMetric.evaluateSingleTimestep(self.positions[i], self.orientations[i], self.metric, self.radius)
        print("Evaluation completed.")
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
        match self.metric:
            case EnumMetrics.Metrics.ORDER:
                self.__createOrderPlot(data)
            case EnumMetrics.Metrics.CLUSTER_NUMBER:
                self.__createClusterNumberPlot(data)
            case EnumMetrics.Metrics.CLUSTER_SIZE:
                self.__createClusterSizePlot(data)

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

    def __createOrderPlot(self, data):
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.ylim(0,1)
        
    def __createClusterNumberPlot(self, data):
        time, num = zip(*sorted(data.items()))
        plt.bar(time, num)

    def __createClusterSizePlot(self, data):
        time, num = zip(*sorted(data.items()))

        plt.boxplot(num)
    

