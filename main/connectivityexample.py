
import numpy as np
import matplotlib.pyplot as plt

from EnumNeighbourSelectionMode import NeighbourSelectionMode

import ServiceSavedModel

neighbours = {'0': {'0': [1, 2], '1': [0, 3, 5], '2': [0, 4], '3': [1, 4], '4': [2, 3], '5': [1], '6': []}, 
              '1': {'0': [1, 6], '1': [0, 3, 5], '2': [4], '3': [1, 4], '4': [2, 3], '5': [1], '6': [0]},
              '2': {'0': [1, 6], '1': [0], '2': [4], '3': [4], '4': [2, 3, 5], '5': [4], '6': [0]},
              '3': {'0': [6], '1': [2], '2': [3], '3': [2], '4': [], '5': [6], '6': [5]}}


"""
def piccniccAlgo(neighbours, kmin=2, lmin=1):
    for t in range(len(neighbours.keys())):
        g = neighbours[str(t)]
        cc = findConnectedComponents(g)
        if t == 1:
  """          


def findConnectedComponents(neighbours):
    # INPUT
    #    G = an undirected graph with vertices V and edges E
    # OUTPUT
    #    The number of connected components in G

    componentCount = 0
    visited = {}
    #Visited <- an empty map from vertices to boolean values 

    for v in neighbours.keys():
        visited[v] = False

    for v in neighbours.keys():
        if visited[v] == False:
            performDfs(visited, neighbours, v)
            print(f"v={v}: {componentCount}")
            componentCount += 1

    print(componentCount)
    return componentCount

def performDfs(visited, neighbours, v):
    # INPUT
    #    V = the set of vertices in the graph
    #    k = the current vertex being explored
    # OUTPUT
    #    Executes a depth-first search starting from vertex k,
    #    marking all reachable vertices as visited.

    visited[str(v)] = True
    for p in neighbours.get(str(v)):
        if visited[str(p)] == False:
            performDfs(visited, neighbours, p)

#print(findConnectedComponents(neighbours.get('3')))

def createStaticTemporalGraph(neighbours):
    n = len(neighbours['0'].keys())
    g = {i: {j: [] for j in range(n)} for i in range(n)}
    for t in neighbours.keys():
        for i in range(n):
            for j in neighbours[t][str(i)]:
                g[i][j].append(int(t))
    #print(g)
    return g

def createDirectedStaticTemporalGraphSelected(selected):
    n = len(selected['0'].keys())
    g = {i: {j: [] for j in range(n)} for i in range(n)}
    for t in selected.keys():
        for i in range(n):
            for j in selected[t][str(i)]:
                g[j][i].append(int(t))
    #print(g)
    return g


def getAverageLengthOfChains(g, tmax, interval=1, useVisited=False, maxDepth=900):
    n = len(g)
    lengthsOfChains = []
    for tstart in range(0, tmax+1, interval):
        print(f"{tstart}/{tmax}")
        lengths = []
        for i in range(n):
            if useVisited == True:
                visited = {}
                for v in range(n):
                    visited[v] = False
            else:
                visited = None
            lengths.append(getLengthofLongestChain(g, i, tstart, visited, depth=0, maxDepth=maxDepth))
        lengthsOfChains.append(np.average(lengths))
    return lengthsOfChains
            
def getLengthofLongestChain(g, i, t, visited=None, depth=0, maxDepth=900):   
    # for each time step, check if there is a connection from the current node.
    # if so, continue. else, return the current length
    lengths = []
    depth += 1
    if visited != None:
        visited[i] = True
    for j in range(len(g)):
        if t in g[i][j] and (visited == None or visited[j] == False) and depth < maxDepth:
            lengths.append(getLengthofLongestChain(g, j, t+1, visited, depth=depth))
    length = 1
    if len(lengths) > 0:
        length += np.max(lengths)
    return length


def getMaxStabilityDurationForConnection(g):
    n = len(g)
    connectionDurations = []
    for i in range(n):
        iDurations = []
        for j in range(n):
            maxDuration = 0
            t = None
            for k in g[i][j]:
                if t == None:
                    t = k
                    start = k
                print(f"k={k}, t={t}, start={start}, maxDur={maxDuration}, g[i][j]={g[i][j]}")

                if k != t + 1:
                    print(f"k={k}, t={t}, start={start}")
                    duration = t-start+1
                    start = k
                if k == g[i][j][-1]:
                    
                    duration = k-start+1
                print(f"duration={duration}")

                if duration > maxDuration:
                    maxDuration = duration
                t = k

            iDurations.append(maxDuration)
        connectionDurations.append(iDurations)
    print(connectionDurations)
    return connectionDurations

def getTotalStabilityDurationForConnection(g):
    n = len(g)
    connectionDurations = []
    for i in range(n):
        iDurations = []
        for j in range(n):
            iDurations.append(len(g[i][j]))
        connectionDurations.append(iDurations)
    print(connectionDurations)
    return connectionDurations

def getPickedMatrix(selected):
    n = len(selected['0'].keys())
    g = {i: {j: 0 for j in range(n)} for i in range(n)}
    for t in selected.keys():
        for i in range(n):
            for j in selected[t][str(i)]:
                g[i][j] = g[i][j] + 1
    picked = []
    for i in range(n):
        pickedI = []
        for j in range(n):
            pickedI.append(g[i][j])
        picked.append(pickedI)
            
    #print(g)
    return picked

def pickedSameNeighbourAgainPercentage(selected):
    n = len(selected['0'])
    percentages = []
    for t in selected.keys():
        sameAgain = 0
        if t != '0':
            for i in range(n):
                if selected[t][str(i)] == selected[str(int(t)-1)]:
                    sameAgain += 1
        percentages.append(sameAgain/n*100)
    return percentages


def createNeighbourPlot(connectionDurations, savePath=None):
    """
    Creates a matrix plot showing the minimum or maximum of the local order for every combination of density and radius provided.

    Params:
        - type ("minorder" or "maxorder"): if the minimum or maximum of the local order should be displayed
        - thresholdType (ThresholdType): the type of threshold that is used for updating mechanism
        - threshold (array of float): the thresholds for the updating mechanism
        - radiusVals (array of floats): all considered values for the radius
        - densityVals (array of floats): all considered values for the density
        - initialState (string) [optional]: the initial state of the system: ordered or random
        - startValue (switchTypeValue) [optional]: the switch type value assigned to all particles at the start of the simulation
        - switchTypeOptions (tuple of switchTypeValues) [optional]: the two possible switch type values
        - i (int) [optional]: the number of the simulation run
        - savePath (string) [optional]: where the plot should be saved

    Returns:
        Nothing.
    """
    
    n = len(connectionDurations)
    figure = plt.figure()
    ax = figure.add_subplot(111)
    #ax.set_title(f"{thresholdType.name}, i={i}, thresholds={threshold}")
    
    # using the matshow() function 
    caxes = ax.matshow(np.array(connectionDurations), interpolation ='nearest')
    figure.colorbar(caxes)

    #axes.yaxis.set_major_locator(MultipleLocator(1))  # <- HERE
        #axes.xaxis.set_major_locator(MultipleLocator(5))  # <- HERE
    #ax.set_xticklabels(['']+range(n))
    #ax.set_yticklabels(['']+range)
    ax.set_xlabel("i")
    ax.set_ylabel("j")

    """
    for (i, j), z in np.ndenumerate(connectionDurations):
        ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    """
    if savePath != None:
        plt.savefig(savePath)
        plt.close()
    else:
        plt.show()

def getNumberOfConnectedComponentsForEveryTimestep(neighbours):
    return np.array([findConnectedComponents(neighbours[str(i)]) for i in range(len(neighbours.keys()))])

"""
for neighbourSelectionModeStr in ["HOD", "LOD", "F", "N"]:
    for start in ["ordered", "random"]:
        filenames = [f"D:/vicsek-data2/adaptive_radius/trackinginfo/global/trackinginfo_global_noev_nosw_d=0.05_r=5_{start}_nsm={neighbourSelectionModeStr}_k=1_n=125_noise=1_psteps=100_1.json"]

        neighbours, distances, localOrder, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformations(filenames)
 """           

        #g = createStaticTemporalGraph(neighbours[0])
        #cg = getMaxStabilityDurationForConnection(g)
        #cg = getTotalStabilityDurationForConnection(g)
        #createNeighbourPlot(cg)

        #cg = getPickedMatrix(selected[0])
        #createNeighbourPlot(cg)

        #plt.plot(np.array(pickedSameNeighbourAgainPercentage(selected[0])))
        #plt.show()


"""
savePath = f"number-of-connected-components-{neighbourSelectionModeStr}-{start}-selected.svg"
plt.plot(getNumberOfConnectedComponentsForEveryTimestep(selected[0]))
plt.ylim(0, 100)
plt.savefig(savePath)

plt.show()
"""
"""
savePath = f"avg-chain-length-{neighbourSelectionModeStr}-{start}-selected-maxDepth.svg"
g = createDirectedStaticTemporalGraphSelected(selected[0])
plt.plot(getAverageLengthOfChains(g, tmax=3000, interval= 100))
plt.ylim(0, 100)
plt.savefig(savePath)

plt.show()

savePath = f"avg-chain-length-{neighbourSelectionModeStr}-{start}-selected-visited.svg"
plt.plot(getAverageLengthOfChains(g, tmax=3000, interval= 100, useVisited=True))
plt.ylim(0, 100)
plt.savefig(savePath)

plt.show()
"""

for neighbourSelectionModeStr in ["F", "N"]:
    start = "ordered"
    filenames = [f"D:/vicsek-data2/adaptive_radius/trackinginfo/local/nosw/trackinginfo_local_1e_nosw_{start}_st={neighbourSelectionModeStr}__d=0.01_n=25_r=5_k=1_noise=1_drn=1000_5000-align_fixed_1.json"]

    neighbours, distances, localOrder, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformations(filenames)

    savePath = f"avg-chain-length-{neighbourSelectionModeStr}-1e-nosw-{start}-selected-maxDepth.svg"
    g = createDirectedStaticTemporalGraphSelected(selected[0])
    plt.plot(getAverageLengthOfChains(g, tmax=15000, interval= 100))
    plt.ylim(0, 100)
    plt.savefig(savePath)

    plt.show()