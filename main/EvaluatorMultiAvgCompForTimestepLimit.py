import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd

import Evaluator
import EnumMetrics

class EvaluatorMultiAvgComp(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for comparison of multiple models.
    """
    def __init__(self, modelParams, metric, simulationData=None, evaluationTimestepInterval=1, threshold=0.01, switchTypeValues=None, 
                 switchTypeOptions=None, startTimestep=0, endTimestep=None):
        """
        Initialises the evaluator.

        Parameters:
            - modelParams (array of dictionaries): contains the model parameters for each model
            - metric (EnumMetrics.Metrics) [optional]: the metric according to which the models' performances should be evaluated
            - simulationData (array of (time array, positions array, orientation array, colours array)) [optional]: contains all the simulation data for each model
            - evaluationTimestepInterval (int) [optional]: the interval of the timesteps to be evaluated. By default, every time step is evaluated
            - threshold (float) [optional]: the threshold for the AgglomerativeClustering cutoff
            - switchTypeValues (array of arrays of switchTypeValues) [optional]: the switch type value of every particle at every timestep
            - switchTypeOptions (tuple) [optional]: the two possible values for the switch type value
        
        Returns:
            Nothing.
        """
        self.simulationData = simulationData
        self.modelParams = modelParams
        self.metric = metric
        self.evaluationTimestepInterval = evaluationTimestepInterval
        self.threshold = threshold
        self.switchTypeValues = switchTypeValues
        self.switchTypeOptions = switchTypeOptions
        self.startTimestep = startTimestep
        self.endTimestep = endTimestep

    def evaluate(self):
        """
        Evaluates all models according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for each model at every time step.
        """
        dd = defaultdict(list)
        for model in range(len(self.simulationData)):
            #print(f"evaluating {model}/{len(self.simulationData)}")
            results = []
            for individualRun in range(len(self.simulationData[model])):
                #print(f"step {individualRun}/{len(self.simulationData[model])}")
                if self.switchTypeValues == None:
                    evaluator = Evaluator.Evaluator(self.modelParams[model][individualRun], self.metric, self.simulationData[model][individualRun], self.evaluationTimestepInterval, self.threshold)
                else:    
                    evaluator = Evaluator.Evaluator(self.modelParams[model][individualRun], self.metric, self.simulationData[model][individualRun], self.evaluationTimestepInterval, self.threshold, self.switchTypeValues[model][individualRun], self.switchTypeOptions)
                result = evaluator.evaluate(startTimestep=self.startTimestep, endTimestep=self.endTimestep)
                results.append(result)
            
            ddi = defaultdict(list)
            for d in results: 
                for key, value in d.items():
                    ddi[key].append(value)
            if self.metric == EnumMetrics.Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
                for m in range(len(ddi)):
                    idx = m * self.evaluationTimestepInterval
                    dd[idx].append(ddi[idx][0][0])
                    dd[idx].append(ddi[idx][0][1])
            elif self.metric == EnumMetrics.Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS:
                for m in range(len(ddi)):
                    idx = m * self.evaluationTimestepInterval
                    dd[idx].append(ddi[idx][0][0])
                    dd[idx].append(ddi[idx][0][1])
                    dd[idx].append(ddi[idx][0][2])
            else:
                for m in range(len(ddi)):
                    idx = self.startTimestep + (m * self.evaluationTimestepInterval)
                    if self.metric == EnumMetrics.Metrics.CLUSTER_SIZE:
                        for i in range(len(ddi[idx])):
                            ddi[idx][i] = np.max(ddi[idx][i])
                    dd[idx].append(np.average(ddi[idx]))
        return dd

    
    def visualize(self, data, labels, xLabel=None, yLabel=None, subtitle=None, colourBackgroundForTimesteps=None, savePath=None):
        """
        Visualizes and optionally saves the results of the evaluation as a graph.

        Parameters:
            - data (dictionary): a dictionary with the time step as key and an array of each model's result as values
            - labels (array of strings): the label for each model
            - xLabel (string) [optional]: the label for the x-axis
            - yLabel (string) [optional]: the label for the y-axis
            - subtitle (string) [optional]: subtitle to be included in the title of the visualisation
            - colourBackgroundForTimesteps ([start, stop]) [optional]: the start and stop timestep for the background colouring for the event duration
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        match self.metric:
            case EnumMetrics.Metrics.ORDER:
                self.__createOrderPlot(data, labels)
            case EnumMetrics.Metrics.CLUSTER_NUMBER:
                self.__createClusterNumberPlot(data, labels)
            case EnumMetrics.Metrics.CLUSTER_SIZE:
                self.__createClusterSizePlot(data, labels)
            case EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME:
                self.__createClusterNumberOverParticleLifetimePlot(data, labels)
            case EnumMetrics.Metrics.ORDER_VALUE_PERCENTAGE:
                self.__createSwitchValuePlot(data, labels)
            case EnumMetrics.Metrics.DUAL_OVERLAY_ORDER_AND_PERCENTAGE:
                self.__createDualOrderPlot(data)
            case EnumMetrics.Metrics.AVERAGE_NUMBER_NEIGHBOURS:
                self.__createAverageNumberNeighboursPlot(data, labels)
            case EnumMetrics.Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS:
                self.__createMinAvgMaxNumberNeighboursPlot(data, labels)
            case EnumMetrics.Metrics.AVG_DISTANCE_NEIGHBOURS:
                self.__createAverageDistanceNeighboursPlot(data, labels)
            case EnumMetrics.Metrics.AVG_CENTROID_DISTANCE:
                self.__createAverageDistanceFromCentroidPlot(data, labels)

        if xLabel != None:
            plt.xlabel(xLabel)
        if yLabel != None:
            plt.ylabel(yLabel)
        if subtitle != None:
            plt.title(f"""{subtitle}""")
        if not any(ele is None for ele in colourBackgroundForTimesteps):
            ax = plt.gca()
            y = np.arange(0, 1, 0.01)
            ax.fill_betweenx(y, colourBackgroundForTimesteps[0], colourBackgroundForTimesteps[1], facecolor='green', alpha=0.5)
        if savePath != None:
            plt.savefig(savePath)
        #plt.show()
        plt.close()

    
    def evaluateAndVisualize(self, labels, xLabel=None, yLabel=None, subtitle=None, colourBackgroundForTimesteps=(None,None), savePath=None):
        """
        Evaluates and subsequently visualises the results for multiple models.

        Parameters:
            - labels (array of strings): the label for each model
            - subtitle (string) [optional]: subtitle to be included in the title of the visualisation
            - savePath (string) [optional]: the location and name of the file where the model should be saved. Will not be saved unless a savePath is provided

        Returns:
            Nothing.
        """
        self.visualize(self.evaluate(), labels, xLabel=xLabel, yLabel=yLabel, subtitle=subtitle, colourBackgroundForTimesteps=colourBackgroundForTimesteps, savePath=savePath)

    def __createOrderPlot(self, data, labels):
        """
        Creates a line plot for the order in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the order value for all models as its value

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line(ylim=(0,1.1))
        
    def __createClusterNumberPlot(self, data, labels):
        """
        Creates a bar plot for the number of clusters in the system for every model at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the number of clusters for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot()

    def __createClusterSizePlot(self, data, labels):
        """
        Creates a line plot for the average size of clusters in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and the size of every cluster of every model as its value

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line()

    def __createClusterNumberOverParticleLifetimePlot(self, data, labels):
        """
        Creates a bat plot for the number of clusters that every particle of every model has belonged to over the course of the whole run

        Parameters:
            - data (dictionary): a dictionary with the particle index as its key and number of clusters it has belonged to as its value
            - labels (list of strings): labels for the models

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line()

    def __createSwitchValuePlot(self, data, labels):
        """
        Creates a line plot for the percentage of particles choosing the order switch type value at any given timestep.

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the number of clusters for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot(ylim=(0,100.1))

    def __createDualOrderPlot(self, data):
        """
        Creates a line plot overlaying the percentage of particles choosing the order switch type value and the order value. 

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the number of clusters for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=["order", "percentage of order value"]).T
        df.plot(ylim=(0,1.1))

    def __createAverageNumberNeighboursPlot(self, data, labels):
        """
        Creates a line plot for the average number of neighbours in the system for every model at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the average number of neighbours for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot()

    def __createMinAvgMaxNumberNeighboursPlot(self, data):
        """
        Creates a line plot overlaying minimum, average and maximum number of neighbours.

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the min, avg and max number of neighbours for every model as its value
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=["min", "avg", "max"]).T
        df.plot()

            
    def __createAverageDistanceNeighboursPlot(self, data, labels):
        """
        Creates a line plot for the average number of neighbours in the system for every model at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the average number of neighbours for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line(ylim=(0,10))

    def __createMinAvgMaxNumberNeighboursPlot(self, data):
        """
        Creates a line plot overlaying minimum, average and maximum number of neighbours.

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the min, avg and max number of neighbours for every model as its value
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=["min", "avg", "max"]).T
        df.plot()

    def __createAverageDistanceFromCentroidPlot(self, data, labels):
        """
        Creates a line plot for the average number of neighbours in the system for every model at every timestep

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the average number of neighbours for every model as its value
            - labels (list of strings): labels for the models
            
        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line(ylim=(0,50))

    def getMinAvgMaxNumberOfNeighboursOverWholeRun(self):
        self.metric = EnumMetrics.Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS
        dataDict = self.evaluate()
        mins = []
        avgs = []
        maxs = []
        for val in dataDict.values():
            mins.append(val[0])
            avgs.append(val[1])
            maxs.append(val[2])
        return np.min(mins), np.average(avgs), np.max(maxs)
