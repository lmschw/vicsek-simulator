import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
import math
import random

import ServicePreparation
import EvaluatorMultiAvgComp
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics
import ServiceMetric
import ServiceGeneral
import AnimatorScatter
import AnimatorScatterMulti
import DefaultValues as dv
from matplotlib.ticker import MultipleLocator  # <- HERE

xOffsetsByNCol = {1: 0, 2: -0.5, 3: -0.8, 4: -1.5, 5: -2.2, 6: -3}


def createMultiPlotFromImages(title, nRows, nCols, rowLabels, colLabels, imgPaths):
    """
    Creates a plot with multiple subplots from pre-existing images.

    Params:
        - title (string): the title of the overall plot
        - nRows (int): the number of rows of subplots
        - nCols (int): the number of columns of subplots
        - rowLabels (array of strings): the labels for the rows
        - colLabels (array of strings): the labels for the columns
        - imgPaths (array of strings): the paths for all pre-existing images to be included

    Returns:
        Nothing.
    """
    if len(imgPaths) != (nRows * nCols):
        print("ERROR: wrong number of image paths supplied")

    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    fig.suptitle(title)
    for idx, ax in enumerate(axes.flat):
        img = np.asarray(Image.open(imgPaths[idx]))
        ax.imshow(img)
        
    for ax, col in zip(axes[0, :], colLabels):
        ax.set_title(col)
    for ax, row in zip(axes[:, 0], rowLabels):
        ax.set_ylabel(row)

    plt.tight_layout()
    plt.show()

def createMultiPlotFromScratch(xLabels, yLabels, data, index, title=None, xAxisLabel=None, yAxisLabel=None, savePath=None, xlim =(0,1000), ylim=None, legendRows=1):
    """
    Creates a plot with multiple subplots from data.

    Params:
        - xLabels (array of strings): the labels for the x-axis
        - yLabels (array of strings): the labels for the y-axis
        - data (dictionary with keys "x-y"): the data to be visualised as line plots
        - index (array of strings): the index of the data
        - title (string) [optional]: the title of the overall plot
        - xAxisLabel (string) [optional]: the label of the x-axis of the overall plot
        - yAxisLabel (string) [optional]: the label of the y-axis of the overall plot
        - savePath (string) [optional]: the path of the file where the resulting plot should be saved
        - xlim (tuple: (min, max)) [optional]: the min and max of values on the x-axis for every subplot
        - ylim (tuple: (min, max)) [optional]: the min and max of values on the y-axis for every subplot
        - legendRows (int) [optional]: the number of rows for the legend

    Returns:
        Nothing.
    """
    
    fontsize = 8
    nRows = len(yLabels)
    nCols = len(xLabels)
    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    if title != None:
        fig.suptitle(title)
    for x in range(nRows):
        for y in range(nCols):
            df = pd.DataFrame(data.get(f"{x}-{y}"), index=index).T  
            if nRows == 1:
                df.plot(ax=axes[y], legend=False)
            else:
                df.plot(ax=axes[x][y], legend=False)

    if nRows == 1:
        #axes[0].set_title(xLabels[0], fontsize=fontsize)
        #axes[0].set_xlim(xlim)
        for ax, col in zip(axes, xLabels):
            ax.set_title(col, fontsize=fontsize)
            ax.set_xlim(xlim)

        for ax, row in zip(axes, yLabels):
            ax.set_ylabel(row, fontsize=fontsize)
            if ylim != None:
                ax.set_ylim(ylim)

    else:
        for ax, col in zip(axes[0, :], xLabels):
            ax.set_title(col, fontsize=fontsize)
            ax.set_xlim(xlim)
        for ax, row in zip(axes[:, 0], yLabels):
            ax.set_ylabel(row, fontsize=fontsize)
            if ylim != None:
                ax.set_ylim(ylim)
        
    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    xOffset = xOffsetsByNCol.get(nCols)
    plt.legend(loc='upper center', bbox_to_anchor=(xOffset, -0.3),fancybox=False, shadow=False, ncol=len(index)/legendRows)
    if xAxisLabel != None:
        fig.supxlabel(xAxisLabel, va="bottom")
        #plt.xlabel(xLabel)
    if yAxisLabel != None:
        fig.supylabel(yAxisLabel)
        #plt.ylabel(yLabel)
    plt.tight_layout()
    if savePath != None:
        plt.savefig(savePath)
    plt.show()

# SCATTERPLOT OF NEIGHBOURS
def createNeighbourScatterplot(positions, orientations, numberOfExampleParticles, index, title=None, selectRandomly=True, numberOfSteps=10, steps=None, radius=10, ylim=(-1.1,1.1), savePath=None):
    """
    Creates a plot containing a scatterplot of the neighbours of every selected example particle at regular intervals or at the specified steps.

    Params:
        - positions (array of arrays of [x,y]-coordinates): The position of every particle at every timestep
        - orientations (array of arrays of [u,v]-coordinates): The orientation of every particle at every timestep
        - numberOfExampleParticles (int): the number of particles to be displayed
        - index (array of strings): the index for the data
        - title (string) [optional]: the title for the overall plot
        - selectRandomly (boolean) [optional]: should the example particles be selected randomly or should the first x particles be used
        - numberOfSteps (int) [optional]: the number of evaluation points within the total duration
        - steps (array of ints) [optional]: the time steps at which the data should be evaluated
        - radius (int) [optional]: the perception radius of the particles
        - ylim (tuple: (min, max)) [optional]: the minimum and maximum value for the y-axis of every subplot
        - savePath (string) [optional]: the path of the file where the resulting plot should be saved
    
    Returns:
        Nothing.
    """
    if selectRandomly == True:
        selectedIndices = random.sample(range(len(positions[0])), numberOfExampleParticles)
    else:
        selectedIndices = range(numberOfExampleParticles)
    
    if steps == None:
        steps = range(0, len(positions), int(len(positions)/numberOfSteps))

    plotData = {}
    print(f"selectedIndices={selectedIndices}, steps={steps}")
    for i in selectedIndices:
        ServiceGeneral.logWithTime(f"Evaluating particle {i}")
        pointsForI = []
        for timestep in steps:
            neighbours = ServiceMetric.findNeighbours(i, positions[timestep], radius)
            pointsForTimestep = []
            for neighbourIdx in neighbours:
                orientationDifference = ServiceMetric.cosAngle(orientations[timestep][i], orientations[timestep][neighbourIdx])
                distance = math.sqrt((positions[timestep][i][0]-positions[timestep][neighbourIdx][0])**2 + (positions[timestep][i][1]-positions[timestep][neighbourIdx][1])**2)
                pointsForTimestep.append([distance, orientationDifference])
            pointsForI.append(pointsForTimestep)
        plotData[i] = pointsForI

    fontsize = 8

    ServiceGeneral.logWithTime(f"Creating the plots...")
    nRows = numberOfExampleParticles
    nCols = len(steps)
    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    if title != None:
        fig.suptitle(title)
    for x, partIdx in enumerate(selectedIndices):
        for y in range(len(steps)):
            df = pd.DataFrame(plotData.get(partIdx)[y], columns=index)  
            if nRows == 1:
                df.plot.scatter(ax=axes[y], legend=False)
            else:
                df.plot.scatter(x=index[0], y=index[1], ax=axes[x][y], legend=False)

    ServiceGeneral.logWithTime("Created the subplots. Adding decorations...")
    if nRows == 1:
        #axes[0].set_title(xLabels[0], fontsize=fontsize)
        #axes[0].set_xlim(xlim)
        for ax, col in zip(axes, steps):
            ax.set_title(col, fontsize=fontsize)

        for ax, row in zip(axes, selectedIndices):
            ax.set_ylabel(row, fontsize=fontsize)
            ax.set_ylim(ylim)
    else:
        for ax, col in zip(axes[0, :], steps):
            ax.set_title(col, fontsize=fontsize)
            #ax.set_xlim((0,5000))
        for ax, row in zip(axes[:, 0], selectedIndices):
            ax.set_ylabel(row, fontsize=fontsize)
            ax.set_ylim(ylim)
    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    xOffset = xOffsetsByNCol.get(nCols)
    #plt.legend(loc='upper center', bbox_to_anchor=(xOffset, -0.3),fancybox=False, shadow=False, ncol=len(index))
    fig.supxlabel(index[0], va="bottom")
    fig.supylabel(index[1])
    plt.tight_layout()
    if savePath != None:
        plt.savefig(savePath)
    plt.show()

def createNeighbourScatterplotVideo(positions, orientations, startTime=0, endTime=None, radius=10, ylim=(-1.1,1.1), savePath=None):
    # TODO allow specifying which particle should be shown/selectRandomly
    """
    Creates a video of the distance-orientation difference scatterplot for the neighbours of a selected example particle.

    Params:
        - positions (array of arrays of [x,y]-coordinates): The position of every particle at every timestep
        - orientations (array of arrays of [u,v]-coordinates): The orientation of every particle at every timestep
        - startTime (int) [optional]: the first time step to be considered (inclusive)
        - endTime (int) [optional]: the last time step to be considered (inclusive)
        - radius (int) [optional]: the perception radius of the particles
        - ylim (tuple: (min, max)) [optional]: the minimum and maximum value for the y-axis of every subplot
        - savePath (string) [optional]: the path of the file where the resulting plot should be saved
    
    Returns:
        Nothing.
    """
    if endTime == None:
        endTime = len(positions)
    else:
        endTime += 1 # to include the last time step

    i = 1
    pointsForI = []
    times = []
    for timestep in range(startTime, endTime):
        neighbours = ServiceMetric.findNeighbours(i, positions[timestep], radius)
        times.append(timestep)
        pointsForTimestep = []
        for neighbourIdx in neighbours:
            orientationDifference = ServiceMetric.cosAngle(orientations[timestep][i], orientations[timestep][neighbourIdx])
            distance = math.sqrt((positions[timestep][i][0]-positions[timestep][neighbourIdx][0])**2 + (positions[timestep][i][1]-positions[timestep][neighbourIdx][1])**2)
            pointsForTimestep.append([distance, orientationDifference])
        pointsForI.append(pointsForTimestep)

    nRows = 1
    nCols = 1
    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    # Initalise the animator
    animator = AnimatorScatter.Animator()

    # prepare the animator
    preparedAnimator =  animator.prepareAnimation(fig, axes, particleIdx=i, xlim=(0,radius), ylim=ylim, frames=len(times))
    preparedAnimator.setSimulationData(neighbourData=(times, pointsForI))

    if savePath != None:
        preparedAnimator.saveAnimation(savePath)

    # Display Animation
    preparedAnimator.showAnimation()

def createNeighbourScatterplotVideoMulti(positions, orientations, startTime=0, endTime=None, numberOfExampleParticles=5, selectRandomly=True, title=None, radius=10, ylim=(-1.5,1.5), savePath=None):
    """
    Creates a video of the distance-orientation difference scatterplot for the neighbours of a selected example particle.

    Params:
        - positions (array of arrays of [x,y]-coordinates): The position of every particle at every timestep
        - orientations (array of arrays of [u,v]-coordinates): The orientation of every particle at every timestep
        - startTime (int) [optional]: the first time step to be considered (inclusive)
        - endTime (int) [optional]: the last time step to be considered (inclusive)
        - numberOfExampleParticles (int): the number of particles to be displayed
        - selectRandomly (boolean) [optional]: should the example particles be selected randomly or should the first x particles be used
        - title (string) [optional]: the title for the overall plot
        - radius (int) [optional]: the perception radius of the particles
        - ylim (tuple: (min, max)) [optional]: the minimum and maximum value for the y-axis of every subplot
        - savePath (string) [optional]: the path of the file where the resulting plot should be saved
    
    Returns:
        Nothing.
    """
    
    if selectRandomly == True:
        selectedIndices = random.sample(range(len(positions[0])), numberOfExampleParticles)
    else:
        selectedIndices = range(numberOfExampleParticles)
    

    if endTime == None or (endTime+1) > len(positions):
        endTime = len(positions)
    else:
        endTime += 1 # to include the last time step

    plotData = {}
    times = []
    for i in selectedIndices:
        pointsForI = []
        for timestep in range(startTime, endTime):
            if i == selectedIndices[0]:
                times.append(timestep)
            neighbours = ServiceMetric.findNeighbours(i, positions[timestep], radius)
            pointsForTimestep = []
            for neighbourIdx in neighbours:
                orientationDifference = ServiceMetric.cosAngle(orientations[timestep][i], orientations[timestep][neighbourIdx])
                distance = math.sqrt((positions[timestep][i][0]-positions[timestep][neighbourIdx][0])**2 + (positions[timestep][i][1]-positions[timestep][neighbourIdx][1])**2)
                pointsForTimestep.append([distance, orientationDifference])
            pointsForI.append(pointsForTimestep)
        plotData[i] = pointsForI

    nRows = numberOfExampleParticles
    nCols = 1
    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    # Initalise the animator
    animator = AnimatorScatterMulti.Animator()

    # prepare the animator
    preparedAnimator =  animator.prepareAnimation(fig, axes, particleIdx=None, title=title, xlim=(0,radius), ylim=ylim, frames=len(times))
    preparedAnimator.setSimulationData(neighbourData=(times, plotData))

    if savePath != None:
        preparedAnimator.saveAnimation(savePath)

    # Display Animation
    #preparedAnimator.showAnimation()

def createNeighourDistributionPlotDistance(positions, orientations, startTime=0, endTime=None, numberOfExampleParticles=5, selectRandomly=True, title=None, radius=10, savePath=None):
    if selectRandomly == True:
        i = random.choice(range(len(positions[0])))
    else:
        i = range(numberOfExampleParticles)
    

    if endTime == None or (endTime+1) > len(positions):
        endTime = len(positions)
    else:
        endTime += 1 # to include the last time step

    times = []
    pointsForI = []
    for timestep in range(startTime, endTime):
        times.append(timestep)
        neighbours = ServiceMetric.findNeighbours(i, positions[timestep], radius)
        pointsForTimestep = radius * [0]
        for neighbourIdx in neighbours:
            distance = math.sqrt((positions[timestep][i][0]-positions[timestep][neighbourIdx][0])**2 + (positions[timestep][i][1]-positions[timestep][neighbourIdx][1])**2)
            pointsForTimestep[math.floor(distance)] += 1
        pointsForI.append(pointsForTimestep)


    figure = plt.figure()
    axes = figure.add_subplot(111)
    
    # using the matshow() function 
    caxes = axes.matshow(np.array(pointsForI), interpolation ='nearest')
    figure.colorbar(caxes)

    axes.yaxis.set_major_locator(MultipleLocator(1))  # <- HERE
    axes.xaxis.set_major_locator(MultipleLocator(5))  # <- HERE
    plt.show()
    print(pointsForTimestep[0])

# ANALYSIS
def createSwitchAnalysisPlot(positions, orientations, switchValues, startTime=0, endTime=None, previousSteps=1, idx=None, radius=10, orderValue=5,savePath=None):
    n = len(positions[0])
    if idx == None:
        i = random.choice(range(n))
    else:
        i = idx
    
    if endTime == None or (endTime+1) > len(positions):
        endTime = len(positions)
    else:
        endTime += 1 # to include the last time step

    times = []
    pointsForI = []

    numPrevSteps = startTime - max(0, startTime-previousSteps)
    previousLocalOrders = []
    if numPrevSteps > 0:
        for ts in range(max(0, startTime-previousSteps), startTime):
            neighbours = ServiceMetric.findNeighbours(i, positions[ts], radius)
            neighbourOrientations = [orientation for idx, orientation in enumerate(orientations[ts]) if idx in neighbours]
            localOrder = ServiceMetric.computeOrder(neighbourOrientations)
            previousLocalOrders.append(localOrder)

    for timestep in range(startTime, endTime):
        times.append(timestep)
        neighbours = ServiceMetric.findNeighbours(i, positions[timestep], radius)
        neighbourOrientations = [orientation for idx, orientation in enumerate(orientations[timestep]) if idx in neighbours]
        if switchValues[timestep][i] == orderValue:
            switchVal = 1
        else:
            switchVal = 0
        localOrder = ServiceMetric.computeOrder(neighbourOrientations)
        if timestep == 0:
            avgPreviousLocalOrder = 0
        else:
            avgPreviousLocalOrder = np.average(previousLocalOrders[max(len(previousLocalOrders)-previousSteps, 0):])
        previousLocalOrders.append(localOrder)
        numNeighbours = len(neighbours)
        neighbourLocalOrders = []
        for neighbour in neighbours:
            neighs = ServiceMetric.findNeighbours(neighbour, positions[timestep], radius)
            orients = [orientation for idx, orientation in enumerate(orientations[timestep]) if idx in neighs]
            neighbourLocalOrders.append(ServiceMetric.computeOrder(orients))
        avgNeighbourLocalOrders = np.average(neighbourLocalOrders)

        pointsForI.append([switchVal, localOrder, avgPreviousLocalOrder, avgNeighbourLocalOrders, numNeighbours])

    df = pd.DataFrame(np.array(pointsForI), columns=["value", "local order", "avg previous local order", "avg neighbour local order", "number neighbours"])
    norm_df = df.copy()
    norm_df["number neighbours"] = (df["number neighbours"] - df["number neighbours"].min(0)) / (df["number neighbours"].max(0) - df["number neighbours"].min(0))
    norm_df.plot.line()

    if savePath != None:
        plt.savefig(savePath)
    plt.show()
