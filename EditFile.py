import colorama, csv
import CheckMissing, BatchInfo, AddProfile, DeleteProfile, Constants, ConfigurationDB

def returnLineNumber(line):
    if line.isdigit():
        return line
    else:
        return line[0:len(line)-1]

# Read original batch file into a list. Edit this list instead of openning file constantly
def readOGFile(filename):
    with open(filename, 'r') as infile:
        batchReader = csv.reader(infile)  
        OGFile = list(batchReader)
    return OGFile

# Overwrite original batch file with new data
def writeOGFile(filename, fileList):
    with open(filename, 'w', encoding='UTF8', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(fileList)

# GS Auditing Process
def addMissingSGDProfiles(filename, results, CONFIGURATIONS, DEPENDENCIES):
    orderHasScreens ={}
    visitedBefore = {}
    
    # Read original file into list, automatically delete garbage
    print("Reading file\nDeleting garbage values")
    OGFile = DeleteProfile.deleteSGDGarbageValues(readOGFile(filename))
    rowsAdded = []
    BATCH_DATA = [OGFile[0][17], OGFile[0][10]]

    # Initialize visited before dicts and misc batch data for every tracking number
    print("Initializing...")    
    for row in results:
        # 0: tracking, 1: order, 2: line, 3: batch, 4: slot, 5: AO (DOOR TYPE), 6: AJE (COLOR), 7: AR, 8: CONF, 9: Stile length, 10: Screen Rail Length, 11: TRCO, 12: DPSW, 13: HP, 14: astragal?
        orderLineID = row[1] + returnLineNumber(row[2])

        # Set state flags

        # FOR ANOUNCING START OF NEW LINE
        if orderLineID not in visitedBefore:
            visitedBefore[orderLineID] = False
        # Initialize flag for screens to false (this will run when it see the first tracking number in an an order)
        if orderLineID not in orderHasScreens:
            orderHasScreens[orderLineID] = False
        # Toggle flag to true if in that order number a screen tracking number shows up
        elif row[0][-2] == "R":
            orderHasScreens[orderLineID] = True
    print("Initialization complete.")

    print("Going through tracking numbers...")
    # Go through tracking numbers in SQL query results and...
    for row in results:
        trackingNum = row[0]
        orderLevel = trackingNum[-2:]
        orderLineID = row[1] + returnLineNumber(row[2])

        # Reset state for every new order/line
        if not visitedBefore[orderLineID]:
            visitedBefore[orderLineID] = True
            
            print(colorama.Fore.RED + "\n########## NOW AUDITING " + row[1] + " - " + returnLineNumber(row[2]) + " ##########")

            # Fix NULL values 
            if row[5] is None or row[5] == "NotNeeded":
                row[5] = input("AO was NULL, please enter the correct AO...: ").upper()
            if row[8] is None or row[8] == "NotNeeded":
                row[8] = input("CONF was NULL, please enter the correct CONF: ").upper()
            if row[13] is None or row[13] == "NotNeeded":
                row[13] = input("HP was NULL, please enter the correct HP: ").upper()

            if row[5] != "PASS" and row[8] != "PASS" and row[13] != "PASS":
                # Get dependencies for this line
                # ----->returns a configuration (AO Family) object with all of these values as properties and more. See ConfigurationDB.py for class def
                currentConfig = ConfigurationDB.pickConfiguration(CONFIGURATIONS, DEPENDENCIES, row, orderHasScreens[orderLineID])
                print(colorama.Fore.RED + "~~~             Configuration: " + currentConfig.description + "           ~~~")
                # Check for pocket doors, use to notify user and to delete extra jambs
                if currentConfig.CONF in Constants.pocketDoorConfigs:
                    POCKET = True
                    pocketQTY = 2 if (currentConfig.CONF in Constants.doublePockets) else 1 
                    print(colorama.Fore.YELLOW + "!ALERT: RANDOM POCKET DOOR ENCOUNTERED!")
                else:
                    # Reset to false for any non pocket doors
                    POCKET = False
        if row[5] != "PASS" and row[8] != "PASS" and row[13] != "PASS":

            # Check for horz. frame pack components (header)
            if orderLevel == "A1":
                sillMissing = CheckMissing.checkIfMissing(OGFile, trackingNum, "SILL")
                if not sillMissing:
                    # ...If header missing, add it
                    if CheckMissing.checkIfMissing(OGFile, trackingNum, "HEADER"):
                        print("Header missing. Adding...")
                        sillInfo = BatchInfo.getPartInfo(OGFile, orderLineID, "HEADER")
                        rowsAdded += AddProfile.addHeader(row, BATCH_DATA, sillInfo)
            if not sillMissing:
                # Check for vert. frame pack components (jamb covers)
                if orderLevel == "A2":
                    # ...add jamb covers (avoid double pockets, they don't need them)
                    if row[8] not in Constants.doublePockets:
                        print("Adding jamb covers for " + row[1] + " - " +  returnLineNumber(row[2]))
                        jambLength = BatchInfo.getPartInfo(OGFile, orderLineID, "JAMB CVR")
                        rowsAdded +=   AddProfile.addJambCovers(row, BATCH_DATA, currentConfig, jambLength)
                    
                    # If pocket add any missing hook/hook covers
                    if POCKET:
                        # Delete extra jambs if present (change initial row count to reflect the new value)
                        if row[8] in Constants.leftPockets:
                            OGFile = DeleteProfile.deleteExtraSGDJambs(OGFile, row[1], returnLineNumber(row[2]), "L")
                            
                        elif row[8] in Constants.rightPockets:
                            OGFile = DeleteProfile.deleteExtraSGDJambs(OGFile, row[1], returnLineNumber(row[2]), "R")
                            
                        elif row[8] in Constants.doublePockets:
                            OGFile = DeleteProfile.deleteExtraSGDJambs(OGFile, row[1], returnLineNumber(row[2]), "B")
                            # pretty sure there are no extra jambs for double pocket doors since they don't make it to the BOM in the first place but just in case 
                            # (i.e this line won't delete anything)

                        # ...If pocket hook covers missing, add them
                        if CheckMissing.checkIfMissing(OGFile, trackingNum, "POCKET HOOK CVR"):
                            print("Pocket hook covers were missing. Adding...")
                            pcktLength = BatchInfo.getPartInfo(OGFile, orderLineID)
                            rowsAdded += AddProfile.addPocketHookCovers(row, BATCH_DATA, pcktLength, 2*pocketQTY)

                        # ...If pocket hooks missing, add them
                        if CheckMissing.checkIfMissing(OGFile, trackingNum, "POCKET HOOK"):
                            print("Pocket hook(s) was(were) missing. Adding...")
                            pcktLength = BatchInfo.getPartInfo(OGFile, orderLineID)
                            rowsAdded += AddProfile.addPocketHooks(row, BATCH_DATA, pcktLength, pocketQTY)

                # ...Add correct stiles
                elif orderLevel[0] == "S":
                    print("Adding " + orderLevel + " stiles for " + row[1] + " - " +  returnLineNumber(row[2]))
                    # Check if entire sash was missing, if so add the top/bottom rails too
                    sashRailsMissing = CheckMissing.checkIfMissing(OGFile, trackingNum, "TOP RAIL")
                    # sashRailsMissing = CheckMissing.checkIfMissing(OGFile, trackingNum, "BOTTOM RAIL") 
                    # # NOT SURE IF WE SHOULD CHECK FOR ONLY TOP OR BOTTOM, currently only way is for both to be missing

                    # Inside WE ADD RAILS AND REINFORCEMENTS!!!
                    stileLength, rowsAddedTemp =  AddProfile.addStiles(row, BATCH_DATA, currentConfig, sashRailsMissing)
                    rowsAdded += rowsAddedTemp

                # Check for screens
                elif orderLevel[0] == "R":
                    print("Damn bro we got screens... my b")
                    # ...If screens missing, add them
                    if CheckMissing.checkIfMissing(OGFile, trackingNum, "SCREEN STILES"):
                        print("Screens were missing. Adding screens for " + orderLevel + " level")
                        rowsAdded += AddProfile.addScreens(row, BATCH_DATA, stileLength)
        
    initialRowCount = len(OGFile)
    OGFile += rowsAdded

    writeOGFile(filename, OGFile)

    return [initialRowCount, len(rowsAdded)]

# PB Auditing Process
def addMissingPBProfiles(filename, results):
    # Read original file into list, automatically delete garbage
    print("Reading file")
    OGFile = readOGFile(filename)
    
    # keep track of what was added
    rowsAdded = []
    
    batchData = {}
    visitedBefore = {}

    # Initialize visited before dicts and misc batch data for every tracking number
    print("Initializing...")    
    for row in results:
        # 0: tracking, 1: order, 2: line, 3: batch, 4: slot, 5: AO, 6: AJE, 7: AR, 8: CONF, 9: Stile length, 10: Screen Rail Length, 11: TRCO
        orderLineID = row[1] + returnLineNumber(row[2])

        # Generate batch data for this line
        if orderLineID not in batchData:
            batchData[orderLineID] = BatchInfo.getBatchInfo(filename, orderLineID)

        # Set state flags
        if orderLineID not in visitedBefore:
            visitedBefore[orderLineID] = False
    print("Initialization complete.")
    
    print("Going through tracking numbers...")
    # Go through tracking numbers in SQL query results and...
    for row in results:
        trackingNum = row[0]
        orderLevel = trackingNum[-2:]
        orderLineID = row[1] + returnLineNumber(row[2])

        # Update state for every new order/line
        if not visitedBefore[orderLineID]:
            visitedBefore[orderLineID] = True
            print("\n")
            print(colorama.Fore.RED + "\n########## NOW AUDITING " + row[1] + " - " + returnLineNumber(row[2]) + " ##########")
            
        # Add sweep adapters
        if orderLevel == "A1":
            # Check if jamb covers are missing
            if CheckMissing.checkIfMissing(OGFile, trackingNum, "JAMB SCREW CVR"):
                print("Jamb covers missing. Adding...")
                rowsAdded += AddProfile.addJambCoversPB(row, batchData[orderLineID])

        # ...Add correct stiles
        elif orderLevel[0] == "S":
            print("Checking " + orderLevel + " rails for " + row[1] + " - " +  returnLineNumber(row[2]))

            # Fix NULL values 
            if row[9] is None or row[9] == "NotNeeded" or row[9] == -1:
                row[9] = input("Top rail dimension didn't come through, please enter TPRD...: ").upper()
            if row[8] is None or row[8] == "NotNeeded" or row[8] == -1:
                row[8] = input("Bottom rail dimension didn't come through, please enter TPRD...: ").upper()

            # Check if top/bottom rails were missing
            topRailMissing = CheckMissing.checkIfMissing(OGFile, trackingNum, "TOP RAIL")
            bottomRailMissing = CheckMissing.checkIfMissing(OGFile, trackingNum, "BOTTOM RAIL")

            if topRailMissing:
                rowsAdded += AddProfile.addPBRail(row, batchData[orderLineID], "TOP RAIL")
            if bottomRailMissing:
                rowsAdded += AddProfile.addPBRail(row, batchData[orderLineID], "BOTTOM RAIL")

            # Check if sweep adapter is missing
            if CheckMissing.checkIfMissing(OGFile, trackingNum, "SWEEP ADAPTER"):
                print("Sweep adapters missing. Adding...")
                rowsAdded += AddProfile.addSweepAdapters(row, batchData[orderLineID])
    
    initialRowCount = len(OGFile)
    OGFile += rowsAdded

    writeOGFile(filename, OGFile)

    return [initialRowCount, 0 if len(rowsAdded) == 1 else len(rowsAdded)]
