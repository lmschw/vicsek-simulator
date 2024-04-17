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

xOffsetsByNCol = {1: 0, 2: -0.5, 3: -0.8, 4: -1.5, 5: -2.2, 6: -3}


def createMultiPlotFromImages(title, nRows, nCols, rowLabels, colLabels, imgPaths):
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

def createNeighbourScatterplotVideo(positions, orientations,  radius=10, ylim=(-1.1,1.1), savePath=None):
    i = 1
    pointsForI = []
    times = []
    for timestep in range(len(positions)):
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