import random
import matplotlib.colors as mcolors

import ServiceSavedModel
import ServiceMetric
import AnimatorMatplotlib
import Animator2D

"""
Service containing methods to visualise clusters
"""

def visualiseClusters(path, numberIntervals=-1, numberOfColouredClusters=-1, threshold=0.01, savePathVisualisation=None):
    """
    Visualises the clusters in a model saved in a JSON file. Colours are chosen randomly. Therefore, it can be wise not to
    colour all clusters if the simulation data contains a lot of clusters.

    Parameters:
        - path (string): the location and name of the file containing the simulation data
        - numberIntervals (int): the number of time steps that should be visualised
        - numberOfColouredClusters (int) [optional]: how many clusters should be coloured. 
            By default, all clusters are coloured (-1). If the supplied value is larger than the total number of clusters,
            all clusters are coloured
        - threshold (float): the threshold for AgglomerativeClustering
        - savePathVisualisation (string): the path where the resulting image should be saved

    Returns:
        Nothing. Renders the results.    
    """
    modelParams, simulationData, colours = ServiceSavedModel.loadModel(path)
    time, positions, orientations = simulationData
    colours = colours.astype('<U30')
    lastColouredClusters = []
    if numberIntervals == -1:
        numberIntervals = len(time)
    for i in range(numberIntervals):
        print(f"{i}/{len(time)}")
        numClusters, clusters = ServiceMetric.findClusters(positions[i], orientations[i], threshold=threshold)
        if numberOfColouredClusters == -1 or numberOfColouredClusters > numClusters:
            nColouredClusters = numClusters
        else:
            nColouredClusters = numberOfColouredClusters
        clusterColours = nColouredClusters * [None] 
        for colouredCluster in range(nColouredClusters):
            if len(lastColouredClusters) > colouredCluster:
                clusterColours[colouredCluster] = lastColouredClusters[colouredCluster]
            else:
                clusterColours[colouredCluster] = generateRandomColour()
        for j in range(len(clusters)):
            colours[i][j] = clusterColours[int(clusters[j])-1]
        lastColouredClusters = clusterColours
    print(colours)
    # Initalise the animator
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=numberIntervals)
    preparedAnimator.setParams(modelParams)

    if savePathVisualisation != None:
        preparedAnimator.saveAnimation(savePathVisualisation)

    # Display Animation
    preparedAnimator.showAnimation()

def generateRandomColour():
    """
    Generates a random colour.

    Returns:
        A random colour.
    """
    color = random.choice(list(mcolors.CSS4_COLORS.keys()))
    return color
