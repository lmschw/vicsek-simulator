import ServiceSavedModel
import ServiceImages
import ServiceAnalysis

from EnumEventEffect import EventEffect

"""
--------------------------------------------------------------------------------
PURPOSE 
Creates a plot analysing switch value selection, local order, previous local order,
average local order of the neighbours and number of neighbours for a small timeframe
and a single particle.
--------------------------------------------------------------------------------
"""

initialState = "ordered"
startValue = 5
eventEffect = EventEffect.TURN_BY_FIXED_ANGLE
percentage = 50
modelParams, simulationData, colours, switchTypeValues = ServiceSavedModel.loadModel(f"ind_avg_tt_{initialState}_st=K_o=5_do=1_s={startValue}_d=0.01_LOD_noise=1_th=[0.1]_psteps=100_e-t5000e{eventEffect.val}p{percentage}a180dtGaNone_1.json"
                                                                                     , loadSwitchValues=True)
steps, positions, orientations = simulationData

start = 5100
stop = 5150
#switchers = ServiceAnalysis.findParticlesSwitchingValues(len(positions[0]), switchTypeValues, startTime=4500, endTime=5700)
#print(switchers)
#print(ServiceAnalysis.findParticleWithMaxSwitches(len(positions[0]), switchTypeValues, startTime=5000, endTime=5100))
#print(ServiceAnalysis.findNumberOfSwitchesForParticle(58, len(positions[0]), switchTypeValues, startTime=start, endTime=stop))

ServiceImages.createSwitchAnalysisPlot(positions, orientations, switchTypeValues, startTime=start, endTime=stop, previousSteps=100, idx=58, savePath=f"testAnalysis_{initialState}_{eventEffect.value}_p={percentage}_{start}_{stop}.svg")