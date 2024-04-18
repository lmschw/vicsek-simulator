from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

import DefaultValues as dv

class Animator(object):

    def prepareAnimation(self, matplotlibFigure, ax, particleIdx, title=None, xlim=(0,10), ylim=(-1.1, 1.1), frames=100, frameInterval = 10):
        """
        Prepares the 2D animator object for animation.

        parameters:
        matplotlibFigure: Matplotlibs figure object.
        frameInterval -- The interval between two frames.
        frames -- The number of frames used in the animation.

        returns self
        """
        self._matplotlibFigure = matplotlibFigure
        self._ax = ax
        self._particleIdx = particleIdx
        self._title = title
        self._xlim = xlim
        self._ylim = ylim
        self._frames = frames
        self._frameInterval = frameInterval

        return self

    def setSimulationData(self, neighbourData):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self._time, self._positions = neighbourData

        return self

    def showAnimation(self):
        """
        Shows the animation

        returns self
        """
        self._getAnimation()
        plt.show()
        
        return self
    
    def saveAnimation(self, filename):
        """
        Saves the animation. Requires FFMPEG

        returns
        Animator
        """
        print("Saving commenced...")
        animation = self._getAnimation()
        animation.save(filename=filename, writer="ffmpeg")
        print("Saving completed.")
        return self
    
    def _getAnimation(self):
        return self.animation if 'animation' in self.__dict__ else self._generateAnimation()

    def _generateAnimation(self):
        """
        Generate the animation.
        
        returns
        animation object
        """
        self.animation = FuncAnimation(self._matplotlibFigure, self._animate, interval=self._frameInterval, frames = self._frames)

        return self.animation
    
    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """

        self._ax.clear()
        self._ax.set_xlim(self._xlim)
        self._ax.set_ylim(self._ylim)
        self._ax.set_xlabel('distance')
        self._ax.set_ylabel('cos angle (orientation alignment)')
        posX = [el[0] for el in self._positions[i]]
        posY = [el[1] for el in self._positions[i]]
        scatter = self._ax.scatter(posX, posY)
        if self._title == None:
            plt.title(f"particle={self._particleIdx}, $t$={self._time[i]:.2f}")
        else:
            plt.title(f"{self._title}\nparticle={self._particleIdx}, $t$={self._time[i]:.2f}")

        return scatter