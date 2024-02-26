import codecs, json
import numpy as np
"""
Service contains static methods to save and load models to/from json files.
"""

def saveModel(simulationData, path="sample.json", modelParams=None, saveInterval=1):
    """
    Saves a model trained by the Viscek simulator implementation.

    Parameters:
        - path (string) [optional]: the location and name of the target file
        - modelParams (dict) [optional]: a summary of the model's params such as n, k, neighbourSelectionMode etc.
        - saveInterval (int) [optional]: specifies the interval at which the saving should occur, i.e. if any time steps should be skipped
    
    Returns:
        Nothing. Creates or overwrites a file.
    """
    time, positions, orientations, colours = simulationData
    dict = {"time": __getSpecifiedIntervals(saveInterval, time.tolist()), 
            "positions": __getSpecifiedIntervals(saveInterval, positions.tolist()), 
            "orientations": __getSpecifiedIntervals(saveInterval, orientations.tolist()), 
            "colours": __getSpecifiedIntervals(saveInterval, colours)}

    if modelParams != None:
        paramsDict = {"modelParams": modelParams}
        paramsDict.update(dict)
        dict = paramsDict
        
    with open(path, "w") as outfile:
        json.dump(dict, outfile)

def loadModel(path):
    """
    Loads a single model from a single file.

    Parameters:
        - path (string): the location and file name of the file containing the model data

    Returns:
        The model's params as well as the simulation data containing the time, positions, orientations and colours.
    """
    obj_text = codecs.open(path, 'r', encoding='utf-8').read()
    loadedJson = json.loads(obj_text)

    modelParams = loadedJson["modelParams"]
    time = np.array(loadedJson["time"])
    positions = np.array(loadedJson["positions"])
    orientations = np.array(loadedJson["orientations"])
    colours = np.array(loadedJson["colours"])
    return modelParams, (time, positions, orientations, colours)

def loadModels(paths):
    """
    Loads multiple models from multiple files.

    Parameters:
        - paths (array of strings): An array containing the locations and names of the files containing a single model each

    Returns:
        Returns an array containing the model params for each model and a second array containing the simulation data for each model. Co-indexed.
    """
    data = []
    params = []
    for path in paths:
        modelParams, simulationData = loadModel(path)
        params.append(modelParams)
        data.append(simulationData)
    return params, data
    
def __getSpecifiedIntervals(interval, lst):
    """
    Selects the data within the list which coincides with the specified interval, e.g. every third data point.

    Parameters:
        - interval (int): which data points should be considered, e.g. 3 would indicate indices 0, 3, 6 etc.
        - lst (list): the data to be reduced according to the intervals
    
    Returns:
        A reduced list containing only the data points of the original list at the specified intervals.
    """
    return [lst[idx] for idx in range(0, len(lst)) if idx % interval == 0]