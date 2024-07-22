import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import pandas as pd

import EvaluatorTrackingInfo
from EnumMetricsTrackingInfo import Metrics

class EvaluatorTrackingInfoMultiAvgComp(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for comparison of multiple models.
    """
    def __init__(self, metric, tmax, numberOfRuns, numberOfModels=1, neighbours=None, distances=None, 
                 localOrders=None, orientationDifferences=None, selected=None, evaluationTimestepInterval=1, 
                 threshold=0.01):
        """
        Initialises the evaluator.

        Parameters:
            - metric (EnumMetrics.Metrics) [optional]: the metric according to which the models' performances should be evaluated
            - evaluationTimestepInterval (int) [optional]: the interval of the timesteps to be evaluated. By default, every time step is evaluated
            - threshold (float) [optional]: the threshold for the AgglomerativeClustering cutoff

        Returns:
            Nothing.
        """
        self.metric = metric
        self.tmax = tmax
        self.numberOfRuns = numberOfRuns
        self.numberOfModels = numberOfModels
        self.neighbours = neighbours
        self.distances = distances
        self.localOrders = localOrders
        self.orientationDifferences = orientationDifferences
        self.selected = selected
        self.evaluationTimestepInterval = evaluationTimestepInterval
        self.threshold = threshold

    def evaluate(self):
        """
        Evaluates all models according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for each model at every time step.
        """
        dd = defaultdict(list)
        results = []
        for model in range(self.numberOfModels):
            for individualRun in range(self.numberOfRuns):
                evaluator = EvaluatorTrackingInfo.Evaluator(metric=self.metric, 
                                                            timesteps=range(self.tmax), 
                                                            neighbours=self.neighbours[model][individualRun], 
                                                            distances=self.distances[model][individualRun], 
                                                            localOrders=self.localOrders[model][individualRun], 
                                                            orientationDifferences=self.orientationDifferences[model][individualRun], 
                                                            selected=self.selected[model][individualRun], 
                                                            evaluationTimestepInterval=self.evaluationTimestepInterval, 
                                                            threshold=self.threshold)
                result = evaluator.evaluate()
                results.append(result)
        
            ddi = defaultdict(list)
            for d in results: 
                for key, value in d.items():
                    ddi[key].append(value)

            if self.metric in [Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS,
                            Metrics.MIN_AVG_MAX_DISTANCE_NEIGHBOURS]:
                    for m in range(len(ddi)):
                        idx = m * self.evaluationTimestepInterval
                        dd[idx].append(ddi[idx][0][0])
                        dd[idx].append(ddi[idx][0][1])
                        dd[idx].append(ddi[idx][0][2])
            else: 
                for m in range(len(ddi)):
                    idx = m * self.evaluationTimestepInterval
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
            case Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS:
                self.__createMinAvgMaxLinePlot(data)
            case Metrics.MIN_AVG_MAX_DISTANCE_NEIGHBOURS:
                self.__createMinAvgMaxLinePlot(data)
            case _:
                self.__createLinePlot(data, labels)

        if xLabel != None:
            plt.xlabel(xLabel)
        if yLabel != None:
            plt.ylabel(yLabel)
        if subtitle != None:
            plt.title(f"""{subtitle}""")
        if not any(ele is None for ele in colourBackgroundForTimesteps):
            ax = plt.gca()
            y = np.arange(0, 1, 0.01)
            ax.fill_betweenx(y, colourBackgroundForTimesteps[0], colourBackgroundForTimesteps[1], facecolor='light green', alpha=0.5)
        if savePath != None:
            plt.savefig(savePath)
        plt.show()
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

    def __createLinePlot(self, data, labels):
        """
        Creates a line plot for the order in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the order value for all models as its value

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=labels).T
        df.plot.line(ylim=(0, 20))
 
    def __createMinAvgMaxLinePlot(self, data):
        """
        Creates a line plot for the order in the system at every timestep for every model

        Parameters:
            - data (dictionary): a dictionary with the time step as its key and a list of the order value for all models as its value

        Returns:
            Nothing.
        """
        sorted(data.items())
        df = pd.DataFrame(data, index=["min", "average", "max"]).T
        df.plot.line(ylim=(0, 20))