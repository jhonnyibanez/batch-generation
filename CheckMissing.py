import csv

# Check if passed description is missing from the batch file for its tracking number
def checkIfMissing(fileList, trackingNumber, ASSY_PART):
    for row in fileList:
        # If you found it, return False since it is not missing
        if row[8] == trackingNumber and row[12] == ASSY_PART:
            return False
    # Couldn't find it, confirm it IS missing
    return True