
import ServiceGeneral
import ServiceSavedModel
import ServiceNetwork

iStart = 1
iStop = 3
baseFilename = f"test_tracking_info"
filenames = ServiceGeneral.createListOfFilenamesForI(baseFilename=baseFilename, minI=iStart, maxI=iStop, fileTypeString="json")
neighbours, distances, localOrders, orientationDifferences, selected = ServiceSavedModel.loadConnectionTrackingInformations(filenames)

print(neighbours)
print(ServiceNetwork.getMinAvgMaxNumberOfNeighboursFromTrackingInfoMultipleRuns(neighbours))

