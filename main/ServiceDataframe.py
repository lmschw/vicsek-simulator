import pandas as pd

import ServiceSavedModel

def loadSimulationDataAsDataframe(path, loadSwitchValues=False):
    if loadSwitchValues == True:
        _, simulationData, _, switchValues = ServiceSavedModel.loadModel(path, loadSwitchValues)
    else:
        _, simulationData, _ = ServiceSavedModel.loadModel(path, loadSwitchValues)
    times, positions, orientations = simulationData

    cols = ['t', 'id', 'x', 'y', 'u', 'v']
    if loadSwitchValues == True:
        cols.append('val')

    data = []
    for t in times:
        for i in range(len(positions[0])):
            rowData = [t,  i, positions[t][i][0], positions[t][i][1],  orientations[t][i][0], orientations[t][i][0]]
            if loadSwitchValues == True:
                rowData.append(switchValues[t][i])
            data.append(rowData)

    df = pd.DataFrame(data, columns=cols)
    return df

def createDataframeOfResultsData(data):
    cols = ['time']
    for col in range(len(data[list(data.keys())[0]])):
        cols.append(f"results_{col}")
    transformedData = []
    for t in data.keys():
        dataT = [t]
        for result in data[t]:
            dataT.append(result)
        transformedData.append(dataT)

    df = pd.DataFrame(transformedData, columns=cols)
    return df