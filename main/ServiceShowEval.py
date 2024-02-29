import random
import numpy as np
from random import randbytes
import matplotlib.colors as mcolors


import ServiceSavedModel
import ServiceMetric
import AnimatorMatplotlib
import Animator2D

def visualiseClusters(path, numberIntervals, numberOfColouredClusters=-1):
    modelParams, simulationData, colours = ServiceSavedModel.loadModel(path)
    time, positions, orientations = simulationData
    colours = colours.astype('<U30')
    lastColouredClusters = []
    for i in range(numberIntervals):
        print(f"{i}/{len(time)}")
        numClusters, clusters = ServiceMetric.findClusters(positions[i], orientations[i], radius=10)
        if numberOfColouredClusters == -1 or numberOfColouredClusters > numClusters:
            numberOfColouredClusters = numClusters
        clusterColours = numberOfColouredClusters * [None] 
        for colouredCluster in range(numberOfColouredClusters):
            if len(lastColouredClusters) > colouredCluster:
                clusterColours[colouredCluster] = lastColouredClusters[colouredCluster]
            else:
                clusterColours[colouredCluster] = generateRandomColour()
        for j in range(len(clusters)):
            colours[i][j] = clusterColours[int(clusters[j])]
        lastColouredClusters = clusterColours
    print(colours)
    # Initalise the animator
    animator = AnimatorMatplotlib.MatplotlibAnimator(simulationData, (100,100,100), colours)

    # prepare the animator
    preparedAnimator = animator.prepare(Animator2D.Animator2D(), frames=numberIntervals)
    preparedAnimator.setParams(modelParams)

    # Display Animation
    preparedAnimator.showAnimation()

def generateRandomColour():
    color = random.choice(list(mcolors.CSS4_COLORS.keys()))
    return color
