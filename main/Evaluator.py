import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import ServiceSavedModel
import ServiceMetric
import EnumMetrics

class Evaluator(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for a single model.
    """
    def __init__(self, modelParams, metric, simulationData=None, evaluationTimestepInterval=1, threshold=0.01, switchTypeValues=None, switchTypeOptions=None):
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
        self.evaluationTimestepInterval = evaluationTimestepInterval
        self.threshold = threshold
        self.switchTypeValues = switchTypeValues
        self.switchTypeOptions = switchTypeOptions

        if metric in [EnumMetrics.Metrics.CLUSTER_NUMBER, 
                      EnumMetrics.Metrics.CLUSTER_SIZE, 
                      EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME,
                      EnumMetrics.Metrics.CLUSTER_CONSISTENCY_AVERAGE_STEPS,
                      EnumMetrics.Metrics.CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES]:
            self.radius = modelParams["radius"]
        else:
            self.radius = None
            

    def evaluate(self, saveTimestepsResultsPath=None):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
        if len(self.time) < 1:
            print("ERROR: cannot evaluate without simulationData. Please supply simulationData, modelParams and metric at Evaluator instantiation.")
            return
        valuesPerTimeStep = {}
        for i in range(len(self.time)):
            #if i % 100 == 0:
                #print(f"evaluating {i}/{len(self.time)}")
            if i % self.evaluationTimestepInterval == 0:
                #if self.switchTypeValues != None:
                if any(ele is None for ele in self.switchTypeValues):
                    valuesPerTimeStep[self.time[i]] = ServiceMetric.evaluateSingleTimestep(self.positions[i], self.orientations[i], self.metric, self.radius, threshold=self.threshold)
                else:
                    valuesPerTimeStep[self.time[i]] = ServiceMetric.evaluateSingleTimestep(self.positions[i], self.orientations[i], self.metric, self.radius, threshold=self.threshold, switchTypeValues=self.switchTypeValues[i], switchTypeOptions=self.switchTypeOptions)

        #print("Evaluation completed.")
        if(self.metric == EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME):
            valuesPerTimeStep = ServiceMetric.computeClusterNumberOverParticleLifetime(valuesPerTimeStep)
        if(self.metric == EnumMetrics.Metrics.CLUSTER_CONSISTENCY_AVERAGE_STEPS):
            valuesPerTimeStep = ServiceMetric.identifyClusters(valuesPerTimeStep, self.orientations)
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
        sorted(data.items())
        df = pd.DataFrame(data, index=[1]).T
        df.plot.line()
        
    def __createClusterNumberPlot(self, data):
        """
        Creates a bar plot for the number of clusters in the system at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the number of clusters as its value

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=[1]).T
        df.plot(kind='bar')

    def __createClusterSizePlot(self, data):
        """
        Creates a line plot for the minimum, average and maximum size of clusters in the system at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the size of every cluster as its value

        Returns:
            Nothing.
        """
        time, num = zip(*sorted(data.items()))
        mins = len(time) * [0]
        avgs = len(time) * [0]
        maxs = len(time) * [0]
        for i in range(len(time)):
            mins[i] = np.min(num[i][1:])
            avgs[i] = np.average(num[i][1:])
            maxs[i] = np.max(num[i][1:])
        minAvgMax = [mins, avgs, maxs]
        df = pd.DataFrame(minAvgMax, index=["min", "avg", "max"]).T
        df.plot.line()
    
    def __createClusterNumberOverParticleLifetimePlot(self, data):
        """
        Creates a bat plot for the number of clusters that every particle has belonged to over the course of the whole run

        Parameters:
            - data (dictionary): a dictionary with the particle index as its key and number of clusters it has belonged to as its value

        Returns:
            Nothing.
        """
        #particles, num = zip(*sorted(data.items()))
        #plt.bar(particles, num)
        sorted(data.items())
        df = pd.DataFrame([data]).T
        df.plot(kind='bar')
