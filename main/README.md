# vicsek-simulator

Implements the 2D Vicsek model with modifications. Allows specification of which and how many neighbours of a particle will influence the update of its orientation at every time step on a global or local level. In addition, allows adding events to influence a subselection of particles.

Requires:
- numpy
- pandas
- matplotlib
- sklearn (for AgglomarativeClustering)
- ffmpeg (for video creation)