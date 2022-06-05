import csv

# Check if passed description is missing from the batch file for its tracking number
def checkIfMissing(batchFilename, trackingNumber, ASSY_PART):
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile) # Create a new reader    
        for row in batchReader:
            # If you found it, return False since it is not missing
            if row[8] == trackingNumber and row[12] == ASSY_PART:
                return False
        # Couldn't find it, confirm it IS missing
        return True