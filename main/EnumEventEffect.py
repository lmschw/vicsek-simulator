from enum import Enum

"""
Indicates what should happen to the particles' orientation
"""
class EventEffect(Enum):
    TURN_BY_FIXED_ANGLE = "turn_fixed", "TURN", # the provided angle is added to the current angle of each particle
    ALIGN_TO_FIXED_ANGLE = "align_fixed", "DISTANT", # the same angle is imposed on all particles
    ALIGN_TO_FIXED_ANGLE_NOISE = "align_noise", "DISTANT WITH NOISE", # the same angle is imposed on all particles but subject to noise
    ALIGN_TO_FIRST_PARTICLE = "align_first", "LEADER", # the first particle's orientation is imposed on all
    AWAY_FROM_ORIGIN = "origin_away", "PREDATOR", # turn away from the point of origin of the event
    TOWARDS_ORIGIN = "origin_to", "FOOD", # turn towards the point of origin of the event
    RANDOM = "random", "RANDOM" # sets the orientations to a random value, intended for baseline
    ENFORCE_VALUE_ONLY = "enforce", "ENFORCE VALUE ONLY" # does not affect the orientation but imposes value selection on the affected particles

    def __init__(self, val, label):
        self.val = val
        self.label = label