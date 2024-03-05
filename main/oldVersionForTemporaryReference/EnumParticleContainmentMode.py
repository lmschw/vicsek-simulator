from enum import Enum

class ParticleContainmentMode(str, Enum):
    STANDARD = "STANDARD", # particles circle around once they cross the border of the domain
    CONTAINED = "CONTAINED", # no leaving
    LEAVING = "LEAVING" # upon crossing the border of the domain, the particles are lost