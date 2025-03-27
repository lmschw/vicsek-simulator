import ServiceSavedModel
import main.ServiceTrackingInformation as ServiceTrackingInformation
import EnumMetricsTrackingInfo

class Evaluator(object):
    """
    Implementation of the evaluation mechanism for the Vicsek model for a single model.
    """
    def __init__(self, metric, timesteps, neighbours, distances, localOrders, 
                 orientationDifferences, selected, evaluationTimestepInterval=1, 
                 threshold=0.01):
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
        self.metric = metric
        self.timesteps = timesteps
        self.neighbours = neighbours
        self.distances = distances
        self.localOrders = localOrders
        self.orientationDifferences = orientationDifferences
        self.selected = selected
        self.evaluationTimestepInterval = evaluationTimestepInterval
        self.threshold = threshold
            

    def evaluate(self, startTimestep=0, endTimestep=None, saveTimestepsResultsPath=None):
        """
        Evaluates the model according to the metric specified for the evaluator.

        Returns:
            A dictionary with the results for the model at every time step.
        """
        if len(self.timesteps) < 1:
            print("ERROR: cannot evaluate without data. Please supply the appropriate data and metric at Evaluator instantiation.")
            return
        if endTimestep == None:
            endTimestep = len(self.timesteps)
        valuesPerTimeStep = {}
        for i in range(len(self.timesteps)):
            if i % self.evaluationTimestepInterval == 0 and i >= startTimestep and i <= endTimestep:
                iStr = str(i)
                valuesPerTimeStep[self.timesteps[i]] = ServiceTrackingInformation.evaluateSingleTimestep(self.metric, neighbours=self.neighbours[iStr], distances=self.distances[iStr], localOrders=self.localOrders[iStr], orientationDifferences=self.orientationDifferences[iStr], selected=self.selected[iStr], threshold=self.threshold)

        #print("Evaluation completed.")
        # if saveTimestepsResultsPath != None:
        #     ServiceSavedModel.saveTimestepsResults(valuesPerTimeStep, saveTimestepsResultsPath, self.modelParams)
        return valuesPerTimeStep
    