import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

import EnumMetrics as metrics
import Evaluator

class EvaluatorMulti(object):
    def __init__(self, simulationData, modelParams, metric):
        self.simulationData = simulationData
        self.modelParams = modelParams
        self.metric = metric

    def evaluate(self):
        results = []
        for i in range(len(self.simulationData)):
            evaluator = Evaluator.Evaluator(self.simulationData[i], self.modelParams[i], self.metric)
            results.append(evaluator.evaluate())
        
        dd = defaultdict(list)
        for d in results: 
            for key, value in d.items():
                dd[key].append(value)

        return dd

    
    def visualize(self, data, labels, subtitle='', savePath=None):
        x, y = zip(*sorted(data.items()))
        plt.plot(x, y)
        plt.gca().legend(labels)
        plt.title(f"""Model comparison: \n{subtitle}""")

        if savePath != None:
            plt.savefig(savePath)

        plt.show()

    
    def evaluateAndVisualize(self, labels, subtitle='', savePath=None):
        self.visualize(self.evaluate(), labels, subtitle=subtitle, savePath=savePath)

