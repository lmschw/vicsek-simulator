import numpy as np
import random
import math
from heapq import nlargest
from heapq import nsmallest

from EnumNeighbourSelectionMode import NeighbourSelectionMode

"""
Service that includes general methods used by the Vicsek model.
"""

def normalizeOrientations(orientations):
    # TODO move to ServiceOrientations
    """
    Normalises the orientations of all particles for the current time step

    Parameters:
        - orientations (array): The current orientations of all particles

    Returns:
        The normalised orientations of all particles as an array.
    """
    return orientations/(np.sqrt(np.sum(orientations**2,axis=1))[:,np.newaxis])

def pickNeighbours(neighbourSelectionMode, k, candidates, currentParticlePosition, currentParticleOrientation, positions, orientations):
    match neighbourSelectionMode:
        case NeighbourSelectionMode.RANDOM:
            random.shuffle(candidates)
            pickedNeighbours = candidates[:k]
        case NeighbourSelectionMode.NEAREST:
            candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
            pickedNeighbours = nsmallest(k, candidateDistances, candidateDistances.get)
        case NeighbourSelectionMode.FARTHEST:
            candidateDistances = {candidateIdx: math.dist(currentParticlePosition, positions[candidateIdx]) for candidateIdx in candidates}
            pickedNeighbours = nlargest(k, candidateDistances, candidateDistances.get)
        case NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE:
            candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
            pickedNeighbours = nsmallest(k, candidateDistances, candidateDistances.get)
        case NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE:
            candidateDistances = {candidateIdx: math.dist(currentParticleOrientation, orientations[candidateIdx]) for candidateIdx in candidates}
            pickedNeighbours = nlargest(k, candidateDistances, candidateDistances.get)
        case _:  # select all neighbours
            pickedNeighbours = candidates
    return pickedNeighbours
