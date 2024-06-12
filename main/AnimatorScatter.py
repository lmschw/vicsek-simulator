from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

class Animator(object):

    """
    Animates the scatterplots for the neighbours of a particle.
    """

    def prepareAnimation(self, matplotlibFigure, ax, particleIdx, title=None, xlim=(0,10), ylim=(-1.1, 1.1), frames=100, frameInterval = 10):
        """
        Prepares the animator object for the scatterplot animation.

        parameters:
            - matplotlibFigure (Matplotlib Figure): Matplotlib figure object.
            - ax (array of Axes): all the relevant axes of the Matplotlib figure object
            - title (string) [optional]: title to be included in the animation
            - xlim (tuple of int: (min, max)) [optional]: the lower and upper limit of the x-axis
            - ylim (tuple of int: (min, max)) [optional]: the lower and upper limit of the y-axis
            - frames (int): The number of frames used in the animation.
            - frameInterval (int): The interval between two frames.

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
        Sets the simulation data
        
        Parameters:
            - simulationData: The simulation data array.
            - domainSize: The tuple that represents the lenghts of the square domain in each dimension.

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