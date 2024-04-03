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

xOffsetsByNCol = {3: -0.8, 4: -1.5, 5: -2.2, 6: -3}


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

def createMultiPlotFromScratch(title, nRows, nCols, rowLabels, colLabels, data, savePath=None):
    fig, axes = plt.subplots(nrows=nRows, ncols=nCols, sharex=True, sharey=True)

    fig.suptitle(title)
    for x in range(nRows):
        for y in range(nCols):
            df = pd.DataFrame(data.get(f"{x}-{y}"), index=["RANDOM", "NEAREST", "FARTHEST", "LEAST ORIENTATION DIFFERENCE", "HIGHEST ORIENTATION DIFFERENCE", "ALL"]).T  
            df.plot(ax=axes[x][y], legend=False)

    for ax, col in zip(axes[0, :], colLabels):
        ax.set_title(col)
        ax.set_xlim((0,1000))
    for ax, row in zip(axes[:, 0], rowLabels):
        ax.set_ylabel(row)
        ax.set_ylim((0,1.1))
        
    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    xOffset = xOffsetsByNCol.get(nCols)
    plt.legend(loc='upper center', bbox_to_anchor=(xOffset, -0.3),fancybox=False, shadow=False)

    plt.tight_layout()
    if savePath != None:
        plt.savefig(savePath)
    plt.show()