from enum import Enum

class ParticleContainmentMode(Enum):
    STANDARD = 1, # particles circle around once they cross the border of the domain
    CONTAINED = 2, # no leaving
    LEAVING = 3 # upon crossing the border of the domain, the particles are lost