import numpy as np

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
            - modelParams (array of dictionaries): contains the model parameters for the current model
            - metric (EnumMetrics.Metrics) [optional]: the metric according to which the models' performances should be evaluated
            - simulationData (array of (time array, positions array, orientation array, colours array)) [optional]: contains all the simulation data
            - evaluationTimestepInterval (int) [optional]: the interval of the timesteps to be evaluated. By default, every time step is evaluated
            - threshold (float) [optional]: the threshold for the AgglomerativeClustering cutoff
            - switchTypeValues (array of arrays of switchTypeValues) [optional]: the switch type value of every particle at every timestep
            - switchTypeOptions (tuple) [optional]: the two possible values for the switch type value
        
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
                      EnumMetrics.Metrics.CLUSTER_NUMBER_WITH_RADIUS,
                      EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME,
                      EnumMetrics.Metrics.CLUSTER_CONSISTENCY_AVERAGE_STEPS,
                      EnumMetrics.Metrics.CLUSTER_CONSISTENCY_NUMBER_OF_CLUSTER_CHANGES,
                      EnumMetrics.Metrics.AVERAGE_NUMBER_NEIGHBOURS,
                      EnumMetrics.Metrics.MIN_AVG_MAX_NUMBER_NEIGHBOURS,
                      EnumMetrics.Metrics.AVG_DISTANCE_NEIGHBOURS]:
            self.radius = modelParams["radius"]
        else:
            self.radius = None
            

    def evaluate(self, startTimestep=0, endTimestep=None, saveTimestepsResultsPath=None):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
        if len(self.time) < 1:
            print("ERROR: cannot evaluate without simulationData. Please supply simulationData, modelParams and metric at Evaluator instantiation.")
            return
        times = np.array(self.time)
        maxT = np.max(times)
        if endTimestep == None:
            endTimestep = max(len(self.time), maxT)
        valuesPerTimeStep = {}
        for i in times:
            #if i % 100 == 0:
                #print(f"evaluating {i}/{len(self.time)}")
            if i % self.evaluationTimestepInterval == 0 and i >= startTimestep and i <= endTimestep:
                idx = np.where(times == i)[0][0]
                #if self.switchTypeValues == None:
                if any(ele is None for ele in self.switchTypeValues):
                    valuesPerTimeStep[i] = ServiceMetric.evaluateSingleTimestep(self.positions[idx], self.orientations[idx], self.metric, self.radius, threshold=self.threshold)
                else:
                    valuesPerTimeStep[i] = ServiceMetric.evaluateSingleTimestep(self.positions[i], self.orientations[i], self.metric, self.radius, threshold=self.threshold, switchTypeValues=self.switchTypeValues[i], switchTypeOptions=self.switchTypeOptions)

        #print("Evaluation completed.")
        if(self.metric == EnumMetrics.Metrics.CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME):
            valuesPerTimeStep = ServiceMetric.computeClusterNumberOverParticleLifetime(valuesPerTimeStep)
        if(self.metric == EnumMetrics.Metrics.CLUSTER_CONSISTENCY_AVERAGE_STEPS):
            valuesPerTimeStep = ServiceMetric.identifyClusters(valuesPerTimeStep, self.orientations)
        if saveTimestepsResultsPath != None:
            ServiceSavedModel.saveTimestepsResults(valuesPerTimeStep, saveTimestepsResultsPath, self.modelParams)
        return valuesPerTimeStep
    