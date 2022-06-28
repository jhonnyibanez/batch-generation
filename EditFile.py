from cmath import nan

import colorama
import CheckMissing, BatchInfo, AddProfile, DeleteProfile, Constants, ConfigurationDB

def returnLineNumber(line):
    if line.isdigit():
        return line
    else:
        return line[0:len(line)-1]

# GS Auditing Process
def addMissingSGDProfiles(filename, results, CONFIGURATIONS, DEPENDENCIES):
    batchData = {}
    orderHasScreens ={}
    visitedBefore = {}
    
    # Initialize visited before dicts and misc batch data for every tracking number
    print("Initializing...")    
    for row in results:
        # 0: tracking, 1: order, 2: line, 3: batch, 4: slot, 5: AO, 6A: JE, 7: AR, 8: CONF, 9: Stile length, 10: Screen Rail Length, 11: TRCO
        orderLineID = row[1] + returnLineNumber(row[2])

        # Generate batch data for this line
        if orderLineID not in batchData:
            batchData[orderLineID] = BatchInfo.getBatchInfo(filename, orderLineID)

        # Set state flags
        if orderLineID not in visitedBefore:
            visitedBefore[orderLineID] = False
        if orderLineID not in orderHasScreens:
            orderHasScreens[orderLineID] = False
        elif row[0][-2] == "R":
            orderHasScreens[orderLineID] = True

    # Delete garbage
    print("Initialization complete.\nDeleting stiles...")
    DeleteProfile.deleteSGDStiles(filename)
    print("Deleting jamb covers...")
    DeleteProfile.deleteSGDJambCovers(filename)
    print("Deleting existing reinforcements...")
    DeleteProfile.deleteSGDReinforcements(filename)
    
    # Record what was useful // keep track of what was added
    initialRowCount = BatchInfo.getOriginalRowCount(filename)
    rowsAdded = 0

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

            # Get dependencies for this line
            #THIS USED TO RETURN THIS:    # return [AO, CONF, userHanding, userTrack, userMeeting]
            # Now returns a configuration object with all of these values as properties and more. See ConfigurationDB.py for class def
            currentConfig = ConfigurationDB.pickConfiguration(CONFIGURATIONS, DEPENDENCIES, row, orderHasScreens[orderLineID])
            print(colorama.Fore.RED + "~~~             Configuration: " + currentConfig.description + "           ~~~")
            if currentConfig.CONF in Constants.pocketDoorConfigs:
                POCKET = True
                pocketQTY = 2 if (currentConfig.CONF in Constants.doublePockets) else 1 
                print(colorama.Fore.YELLOW + "!ALERT: RANDOM POCKET DOOR ENCOUNTERED!")
            else:
                # Reset to false for any non pocket doors
                POCKET = False

        # Check for horz. frame pack components (header)
        if orderLevel == "A1":
            # ...If header missing, add it
            if CheckMissing.checkIfMissing(filename, trackingNum, "HEADER"):
                print("Header missing. Adding...")
                sillInfo = BatchInfo.getSillInfo(filename, orderLineID)
                rowsAdded = AddProfile.addHeader(filename, row, batchData[orderLineID], sillInfo, rowsAdded)

        # Check for vert. frame pack components (jamb covers)
        elif orderLevel == "A2":
            # ...If jamb covers missing, add them (avoid double pockets, they don't need them)
            if row[8] not in Constants.doublePockets:
                print("Adding jamb covers for " + row[1] + " - " +  returnLineNumber(row[2]))
                jambLength = BatchInfo.getJambLength(filename, orderLineID)
                rowsAdded =   AddProfile.addJambCovers(filename, row, batchData[orderLineID], currentConfig, jambLength, rowsAdded)
            
            # If pocket add any missing hook/hook covers
            if POCKET:
                # Delete extra jambs if present (change initial row count to reflect the new value)
                if row[8] in Constants.leftPockets:
                    initialRowCount = DeleteProfile.deleteExtraSGDJambs(filename, row[1], returnLineNumber(row[2]), initialRowCount, "L")
                     
                elif row[8] in Constants.rightPockets:
                    initialRowCount = DeleteProfile.deleteExtraSGDJambs(filename, row[1], returnLineNumber(row[2]), initialRowCount, "R")
                     
                elif row[8] in Constants.doublePockets:
                    initialRowCount = DeleteProfile.deleteExtraSGDJambs(filename, row[1], returnLineNumber(row[2]), initialRowCount, "B")
                    # pretty sure there are no extra jambs for double pocket doors since they don't make it to the BOM in the first place but just in case

                # ...If pocket hook covers missing, add them
                if CheckMissing.checkIfMissing(filename, trackingNum, "POCKET HOOK CVR"):
                    print("Pocket hook covers were missing. Adding...")
                    pcktLength = BatchInfo.getPocketLength(filename, orderLineID)
                    rowsAdded = AddProfile.addPocketHookCovers(filename, row, batchData[orderLineID], pcktLength, 2*pocketQTY, rowsAdded)

                # ...If pocket hooks missing, add them
                if CheckMissing.checkIfMissing(filename, trackingNum, "POCKET HOOK"):
                    print("Pocket hook(s) was(were) missing. Adding...")
                    pcktLength = BatchInfo.getPocketLength(filename, orderLineID)
                    rowsAdded = AddProfile.addPocketHooks(filename, row, batchData[orderLineID], pcktLength, pocketQTY, rowsAdded)

        # ...Add correct stiles
        elif orderLevel[0] == "S":
            print("Adding " + orderLevel + " stiles for " + row[1] + " - " +  returnLineNumber(row[2]))
            # Check if entire sash was missing, if so add the top/bottom rails too
            sashRailsMissing = CheckMissing.checkIfMissing(filename, trackingNum, "TOP RAIL")
            # sashRailsMissing = CheckMissing.checkIfMissing(filename, trackingNum, "BOTTOM RAIL") 
            # # NOT SURE IF WE SHOULD CHECK FOR ONLY TOP OR BOTTOM, currently only way is for both to be missing

            [stileLength, rowsAdded] =   AddProfile.addStiles(filename, row, batchData[orderLineID], currentConfig, sashRailsMissing, rowsAdded)

        # Check for screens
        elif orderLevel[0] == "R":
            print("Damn bro we got screens... my b")
            # ...If screens missing, add them
            if CheckMissing.checkIfMissing(filename, trackingNum, "SCREEN RAILS"):
                print("Screens were missing. Adding screens for " + orderLevel + " level")
                rowsAdded = AddProfile.addScreens(filename, row, batchData[orderLineID], stileLength, rowsAdded)
    
    return [initialRowCount, rowsAdded]

# PB Auditing Process
def addMissingPBProfiles(filename, results):
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
    
    # Record what was useful // keep track of what was added
    initialRowCount = BatchInfo.getOriginalRowCount(filename)
    rowsAdded = 0
    
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
            
        if orderLevel[0] == "S":
            # Fix NULL values 
            if row[9] is None or row[9] == "NotNeeded" or row[9] == -1:
                row[9] = input("Top rail dimension didn't come through, please enter TPRD...: ").upper()
            if row[8] is None or row[8] == "NotNeeded" or row[8] == -1:
                row[8] = input("Bottom rail dimension didn't come through, please enter TPRD...: ").upper()

        # Add sweep adapters
        if orderLevel == "A1":
            print("Checking if jamb covers are missing...")
            if CheckMissing.checkIfMissing(filename, trackingNum, "JAMB SCREW CVR"):
                print("Jamb covers missing. Adding...")
                rowsAdded = AddProfile.addJambCoversPB(filename, row, batchData[orderLineID], rowsAdded)

        # ...Add correct stiles
        elif orderLevel[0] == "S":
            print("Adding " + orderLevel + " rails for " + row[1] + " - " +  returnLineNumber(row[2]))
            # Check if entire sash was missing, if so add the top/bottom rails too
            topRailMissing = CheckMissing.checkIfMissing(filename, trackingNum, "TOP RAIL")
            bottomRailMissing = CheckMissing.checkIfMissing(filename, trackingNum, "BOTTOM RAIL")
            rowsAdded = AddProfile.addPBRails(filename, row, batchData[orderLineID], topRailMissing, bottomRailMissing, rowsAdded)
            # stileLength = AddProfile.addStiles(filename, row, batchData[orderLineID], dependencies, sashRailsMissing, hasScreens, rowsAdded)

            print("Checking if sweep adapters missing...")
            if CheckMissing.checkIfMissing(filename, trackingNum, "SWEEP ADAPTER"):
                print("Sweep adapters missing. Adding...")
                rowsAdded = AddProfile.addSweepAdapters(filename, row, batchData[orderLineID], rowsAdded)
    return [initialRowCount, rowsAdded]
