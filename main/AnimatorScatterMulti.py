from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import DefaultValues as dv
import AnimatorScatter

class Animator(AnimatorScatter.Animator):
    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """
        print(i)
        for j, ax in enumerate(self._ax):
            particleIdx = list(self._positions.keys())[j]
            ax.clear()
            ax.set_xlim(self._xlim)
            ax.set_ylim(self._ylim)
            ax.set_ylabel(particleIdx)
            posX = [el[0] for el in self._positions.get(particleIdx)[i]]
            posY = [el[1] for el in self._positions.get(particleIdx)[i]]
            ax.scatter(posX, posY)
        self._matplotlibFigure.suptitle(f"$t$={self._time[i]:.2f}")
        self._matplotlibFigure.supxlabel("distance", va="bottom")
        self._matplotlibFigure.supylabel("cos angle (orientation alignment)")

        return self._ax