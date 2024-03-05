import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

import Evaluator
import EnumMetrics

class EvaluatorMulti(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for comparison of multiple models.
    """
    def __init__(self, modelParams, metric, simulationData=None):
        """
        Initialises the evaluator.

        Parameters:
            - simulationData (array of (time array, positions array, orientation array, colours array)): contains all the simulation data for each model
            - modelParams (array of dictionaries): contains the model parameters for each model
            - metric (EnumMetrics.Metrics): the metric according to which the models' performances should be evaluated
        
        Returns:
            Nothing.
        """
        self.simulationData = simulationData
        self.modelParams = modelParams
        self.metric = metric

    def evaluate(self):
        """
        Evaluates all models according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for each model at every time step.
        """
        results = []
        for i in range(len(self.simulationData)):
            print(f"evaluating {i}/{len(self.simulationData)}")
            evaluator = Evaluator.Evaluator(self.simulationData[i], self.modelParams[i], self.metric)
            results.append(evaluator.evaluate())
        
        dd = defaultdict(list)
        for d in results: 
            for key, value in d.items():
                dd[key].append(value)
        print("Evaluation complete.")
        return dd

    
    def visualize(self, data, labels, subtitle='', savePath=None):
        """
        Visualizes and optionally saves the results of the evaluation as a graph.

        Parameters:
            - data (dictionary): a dictionary with the time step as key and an array of each model's result as values
            - labels (array of strings): the label for each model
            - subtitle (string) [optional]: subtitle to be included in the title of the visualisation
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

        plt.title(f"""Model comparison: \n{subtitle}""")
        plt.gca().legend((labels))
        if savePath != None:
            plt.savefig(savePath)

        plt.show()

    
    def evaluateAndVisualize(self, labels, subtitle='', savePath=None):
        """
        Evaluates and subsequently visualises the results for multiple models.

        Parameters:
            - labels (array of strings): the label for each model
            - subtitle (string) [optional]: subtitle to be included in the title of the visualisation
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        self.visualize(self.evaluate(), labels, subtitle=subtitle, savePath=savePath)

    def __createOrderPlot(self, data):
        """
        Creates a line plot for the order in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the order value for all models as its value

        Returns:
            Nothing.
        """
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.ylim(0,1)
        
    def __createClusterNumberPlot(self, data):
        """
        Creates a bar plot for the number of clusters in the system for every model at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the number of clusters for every model as its value

        Returns:
            Nothing.
        """
        width = 0.25  # the width of the bars
        multiplier = 0
        sorted(data.items())
        for time, vals in data.items():
            for val in vals:
                offset = width * multiplier
                rects = plt.bar(time + offset, val, width, label=val)
                #plt.bar_label(rects, padding=3)
                multiplier += 1    

    def __createClusterSizePlot(self, data):
        """
        Creates a line plot for the average size of clusters in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the size of every cluster of every model as its value

        Returns:
            Nothing.
        """
        x, y = zip(*sorted(data.items()))
        avgs = []
        for vals in y:
            stepAvgs = []
            for val in vals:
                stepAvgs.append(np.average(val))
            avgs.append(stepAvgs)
        plt.plot(x, avgs)

    def __createClusterNumberOverParticleLifetimePlot(self, data):
        """
        Creates a bat plot for the number of clusters that every particle of every model has belonged to over the course of the whole run

        Parameters:
            - data (dictionary): a dictionary with the particle index as its key and number of clusters it has belonged to as its value

        Returns:
            Nothing.
        """
        width = 0.25  # the width of the bars
        multiplier = 0
        sorted(data.items())
        for time, vals in data.items():
            for val in vals:
                offset = width * multiplier
                rects = plt.bar(time + offset, val, width, label=val)
                #plt.bar_label(rects, padding=3)
                multiplier += 1   