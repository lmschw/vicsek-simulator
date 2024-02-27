import EvaluationMethodService


# All by MODE 
EvaluationMethodService.evaluateAllModes(n=500, k=5, noise=0.3, radius=10)


# mode by N 
#EvaluationMethodService.evaluateN(EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST, k=3, noise=0, radius=20)


# mode by K
#EvaluationMethodService.evaluateK(EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, n=500, noise=0.3, radius=10)

# mode by noise
#EvaluationMethodService.evaluateNoise(EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM, n=200, k=3, radius=20)

# mode by radius
#EvaluationMethodService.evaluateRadius(EnumNeighbourSelectionMode.NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE, n=500, k=5, noise=0)
