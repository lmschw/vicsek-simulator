"""
Contains the default values for all parameters for both the 2D and the 3D implementation
"""

# GENERAL
DEFAULT_SPEED = 1
DEFAULT_RADIUS = 2
DEFAULT_NOISE = 0.3
DEFAULT_NUM_PARTICLES = 100

# neighbours behaviour
DEFAULT_K_NEIGHBOURS = -1 # all neighbours. set to 0 to completely ignore neighbours
DEFAULT_PARTICLES_ALLOWED_TO_LEAVE = True


# 2D
DEFAULT_DOMAIN_SIZE_2D = (100, 100)

# 3D
DEFAULT_DOMAIN_SIZE_3D = (100, 100, 100)
