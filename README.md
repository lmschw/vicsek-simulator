# vicsek-simulator

Implements the 2D Vicsek model. Allows specification of which and how many neighbours of a particle will influence the update of its orientation at every time step.

Features:\

- Optional specification of neighbour selection mode (RANDOM, NEAREST, FARTHEST, LEAST_ORIENTATION_DIFFERENCE, HIGHEST_ORIENTATION_DIFFERENCE);\
- Generating equidistanced, ordered initial state;\
- Saving and loading of experiment and evaluation results;\
- Evaluation of model results using an Evaluator for a single model or for comparative purposes (metrics: ORDER, CLUSTER_NUMBER, CLUSTER_SIZE, CLUSTER_NUMBER_OVER_PARTICLE_LIFETIME)\
