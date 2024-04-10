import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd
import math

import ServicePreparation
import EvaluatorMultiAvgComp
import ServiceSavedModel
from EnumNeighbourSelectionMode import NeighbourSelectionMode
from EnumMetrics import Metrics

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

def createMultiPlotFromScratch(xLabels, yLabels, data, index, title=None, xAxisLabel=None, yAxisLabel=None, savePath=None, xlim =(0,1000), ylim=None):
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
        axes[0].set_title(xLabels[0], fontsize=fontsize)
        axes[0].set_xlim(xlim)

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
    plt.legend(loc='upper center', bbox_to_anchor=(xOffset, -0.3),fancybox=False, shadow=False, ncol=len(index))
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