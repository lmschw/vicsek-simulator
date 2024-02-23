import codecs, json
import numpy as np

def saveModel(simulationData, path="sample.json", modelParams=None):
    time, positions, orientations, colours = simulationData
    dict = {"time": time.tolist(), "positions": positions.tolist(), "orientations": orientations.tolist(), "colours": colours}

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
    