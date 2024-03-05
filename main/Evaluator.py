import numpy as np
import matplotlib.pyplot as plt

import ServiceSavedModel
import ServiceMetric
import EnumMetrics

class Evaluator(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for a single model.
    """
    def __init__(self, modelParams, metric, simulationData=None):
        """
        Initialises the evaluator.

        Parameters:
            - simulationData (time array, positions array, orientation array, colours array): contains all the simulation data
            - modelParams (dictionary): contains the model parameters
            - metric (EnumMetrics.Metrics): the metric according to which the model's performances should be evaluated
        
        Returns:
            Nothing.
        """
        if simulationData != None:
            self.time, self.positions, self.orientations = simulationData
        self.modelParams = modelParams
        self.metric = metric

        if metric in [EnumMetrics.Metrics.CLUSTER_NUMBER, 
                      EnumMetrics.Metrics.CLUSTER_SIZE, 
                      EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME]:
            self.radius = modelParams["radius"]
        else:
            self.radius = None
            

    def evaluate(self, saveTimestepsResultsPath=None):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
        if self.time == None:
            print("ERROR: cannot evaluate without simulationData. Please supply simulationData, modelParams and metric at Evaluator instantiation.")
            return
        valuesPerTimeStep = {}
        for i in range(len(self.time)):
            if i % 100 == 0:
                print(f"evaluating {i}/{len(self.time)}")
            valuesPerTimeStep[self.time[i]] = ServiceMetric.evaluateSingleTimestep(self.positions[i], self.orientations[i], self.metric, self.radius)
        print("Evaluation completed.")
        if(self.metric == EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME):
            valuesPerTimeStep = ServiceMetric.computeClusterNumberOverParticleLifetime(valuesPerTimeStep)
        if saveTimestepsResultsPath != None:
            ServiceSavedModel.saveTimestepsResults(valuesPerTimeStep, saveTimestepsResultsPath, self.modelParams)
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
            case EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME:
                self.__createClusterNumberOverParticleLifetimePlot(data)

        plt.title(f"""Model: n={self.modelParams["n"]}, k={self.modelParams["k"]}, noise={self.modelParams["noise"]}, radius={self.modelParams["radius"]}, speed={self.modelParams["speed"]}, \nneighbour selection: {self.modelParams["neighbourSelectionMode"]}\nMetric: {self.metric.name}""")
        

        if savePath != None:
            plt.savefig(savePath)
        
        plt.show()
    def evaluateAndVisualize(self, savePath=None, saveTimestepsResults=None):
        """
        Evaluates and subsequently visualises the results for a single model.

        Parameters:
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        self.visualize(self.evaluate(saveTimestepsResults), savePath)

    def __createOrderPlot(self, data):
        """
        Creates a line plot for the order in the system at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the order value as its value

        Returns:
            Nothing.
        """
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.ylim(0,1)
        
    def __createClusterNumberPlot(self, data):
        """
        Creates a bar plot for the number of clusters in the system at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the number of clusters as its value

        Returns:
            Nothing.
        """
        time, num = zip(*sorted(data.items()))
        plt.bar(time, num)

    def __createClusterSizePlot(self, data):
        """
        Creates a line plot for the minimum, average and maximum size of clusters in the system at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the size of every cluster as its value

        Returns:
            Nothing.
        """
        time, num = zip(*sorted(data.items()))
        minAvgMax = len(time) * [[0,0,0]]
        for i in range(len(time)):
            minAvgMax[i] = [np.min(num[i][1:]), np.average(num[i][1:]), np.max(num[i][1:])]
        plt.plot(time, minAvgMax)
        plt.gca().legend(("min", "avg", "max"))
    
    def __createClusterNumberOverParticleLifetimePlot(self, data):
        """
        Creates a bat plot for the number of clusters that every particle has belonged to over the course of the whole run

        Parameters:
            - data (dictionary): a dictionary with the particle index as its key and number of clusters it has belonged to as its value

        Returns:
            Nothing.
        """
        particles, num = zip(*sorted(data.items()))
        plt.bar(particles, num)
