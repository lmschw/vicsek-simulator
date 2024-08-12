import ServiceImages

from EnumNeighbourSelectionMode import NeighbourSelectionMode

ks = [0, 1, 2, 3, 4, 5, 10]
nsms = [NeighbourSelectionMode.ALL,
        NeighbourSelectionMode.RANDOM,
        NeighbourSelectionMode.NEAREST,
        NeighbourSelectionMode.FARTHEST,
        NeighbourSelectionMode.LEAST_ORIENTATION_DIFFERENCE,
        NeighbourSelectionMode.HIGHEST_ORIENTATION_DIFFERENCE]

density = 0.05
radius = 10
startTimestep = 6000
endTimestep = None
iStart = 1
iStop = 11
initialState = "ordered"

ServiceImages.createOrderForNsmVsKPlot(neighbourSelectionModes=nsms, 
                                       ks=ks,
                                       initialState=initialState,
                                       startTimestep=startTimestep,
                                       endTimestep=endTimestep,
                                       iStart=iStart,
                                       iStop=iStop,
                                       density=density,
                                       radius=radius,
                                       baseDataFilePath="",
                                       savePath=f"order-nsm-vs-k-plot_nsmsw_d={density}_r={radius}_{initialState}_i={iStart}-{iStop}_t={startTimestep}-{endTimestep}.svg")