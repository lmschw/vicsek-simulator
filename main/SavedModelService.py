import codecs, json
import numpy as np

def saveModel(simulationData, path="sample.json"):
    time, positions, orientations, colours = simulationData
    dict = {"time": time.tolist(), "positions": positions.tolist(), "orientations": orientations.tolist(), "colours": colours}
    with open(path, "w") as outfile:
        json.dump(dict, outfile)

def loadModel(path):
    obj_text = codecs.open(path, 'r', encoding='utf-8').read()
    loadedJson = json.loads(obj_text)
    time = np.array(loadedJson["time"])
    positions = np.array(loadedJson["positions"])
    orientations = np.array(loadedJson["orientations"])
    colours = np.array(loadedJson["colours"])
    return time, positions, orientations, colours
    