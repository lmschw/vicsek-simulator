import SavedModelService
import EvaluatorMulti
import EnumMetrics
import EnumNeighbourSelectionMode
import EvaluationMethodService


# All by MODE 
#EvaluationMethodService.evaluateAllModes(n=500, k=3, noise=0, radius=20)


# mode by N 
#EvaluationMethodService.evaluateN(EnumNeighbourSelectionMode.NeighbourSelectionMode.NEAREST, k=3, noise=0, radius=20)


# mode by K
EvaluationMethodService.evaluateK(EnumNeighbourSelectionMode.NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE, n=200, noise=0, radius=20)

# mode by noise
#EvaluationMethodService.evaluateNoise(EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM, n=200, k=3, radius=20)

# mode by radius
#EvaluationMethodService.evaluateRadius(EnumNeighbourSelectionMode.NeighbourSelectionMode.RANDOM, n=200, k=5, noise=0)