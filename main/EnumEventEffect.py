from enum import Enum

"""
Indicates what should happen to the particles' orientation
"""
class EventEffect(str, Enum):
    TURN_BY_FIXED_ANGLE = "turn_fixed", # the provided angle is added to the current angle of each particle
    ALIGN_TO_FIXED_ANGLE = "align_fixed", # the same angle is imposed on all particles
    ALIGN_TO_FIRST_PARTICLE = "align_first", # the first particle's orientation is imposed on all
    AWAY_FROM_ORIGIN = "origin_away", # turn away from the point of origin of the event
    TOWARDS_ORIGIN = "origin_towards", # turn towards the point of origin of the event

