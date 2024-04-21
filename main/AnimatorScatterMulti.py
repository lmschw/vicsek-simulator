import AnimatorScatter


class Animator(AnimatorScatter.Animator):
    """
    Animates multiple scatterplots for neighbours of a particle within a single figure.
    """

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
        if self._title == None:
            self._matplotlibFigure.suptitle(f"$t$={self._time[i]:.2f}")
        else:
            self._matplotlibFigure.suptitle(f"{self._title}\n$t$={self._time[i]:.2f}")
        self._matplotlibFigure.supxlabel("distance", va="bottom")
        self._matplotlibFigure.supylabel("cos angle (orientation alignment)")

        return self._ax