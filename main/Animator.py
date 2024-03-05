from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import DefaultValues as dv

class Animator(object):

    def prepareAnimation(self, matplotlibFigure, frames=100, frameInterval = 10):
        """
        Prepares the 2D animator object for animation.

        parameters:
        matplotlibFigure: Matplotlibs figure object.
        frameInterval -- The interval between two frames.
        frames -- The number of frames used in the animation.

        returns self
        """
        self._matplotlibFigure = matplotlibFigure
        self._frames = frames
        self._frameInterval = frameInterval

        return self

    def setSimulationData(self, simulationData, domainSize, colours=None):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self._time, self._positions, self._orientations = simulationData
        self._domainSize = domainSize

        if colours is None:
            self._colours = len(self._time) * [len(self._positions[0]) * ['k']]
        else:
            self._colours = colours

        return self
    
    def setParameters(self, n=dv.DEFAULT_NUM_PARTICLES, k=dv.DEFAULT_K_NEIGHBOURS, noise=dv.DEFAULT_NOISE, radius=dv.DEFAULT_RADIUS, speed=dv.DEFAULT_SPEED, showParameters=dv.DEFAULT_SHOW_PARAMETERS):
        self._n = n
        self._k = k
        self._noise = noise
        self._radius = radius
        self._speed = speed
        self._showParameters = showParameters

    def setParams(self, modelParams):
        self._n = modelParams["n"]
        self._k = modelParams["k"]
        self._noise = modelParams["noise"]
        self._radius = modelParams["radius"]
        self._speed = modelParams["speed"]
        self._neighbourSelectionMode = modelParams["neighbourSelectionMode"]
        self._domainSize = modelParams["domainSize"]
        

    def showAnimation(self):
        """
        Shows the animation

        returns self
        """
        self._getAnimation()
        plt.show()

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
