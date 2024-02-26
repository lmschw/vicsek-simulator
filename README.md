# vicsek-simulator

Implements the Vicsek model. Allows specification of which and how many neighbours of a particle will influence the update of its orientation at every time step.

Features: - Optional specification of neighbour selection mode - RANDOM, NEAREST, FARTHEST, LEAST_ORIENTATION_DIFFERENCE, HIGHEST_ORIENTATION_DIFFERENCE - Saving and loading of experiment results - Evaluation of model results using an Evaluator for a single model or for comparative purposes - metrics: ORDER
