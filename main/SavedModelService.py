import codecs, json
import numpy as np

def saveModel(simulationData, path="sample.json", modelParams=None, saveInterval=1):
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
    obj_text = codecs.open(path, 'r', encoding='utf-8').read()
    loadedJson = json.loads(obj_text)

    modelParams = loadedJson["modelParams"]
    time = np.array(loadedJson["time"])
    positions = np.array(loadedJson["positions"])
    orientations = np.array(loadedJson["orientations"])
    colours = np.array(loadedJson["colours"])
    return modelParams, (time, positions, orientations, colours)

def loadModels(paths):
    data = []
    params = []
    for path in paths:
        modelParams, simulationData = loadModel(path)
        params.append(modelParams)
        data.append(simulationData)
    return params, data
    
def __getSpecifiedIntervals(interval, lst):
    return [lst[idx] for idx in range(0, len(lst)) if idx % interval == 0]