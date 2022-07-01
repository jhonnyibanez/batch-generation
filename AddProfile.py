from cmath import nan
import csv, GenerateStiles, Constants

def returnLineNumber(line):
    if line.isdigit():
        return line
    else:
        return line[0:len(line)-1]

# 0tracking, 1order, 2line, 3batch, 4slot, 5AO, 6AJE, 7AR, 8CONF, 9Stile length, 10Screen Rail Length
def addHeader(row, batchData, sillInfo):
    # Header part number
    headerProfile = Constants.headerProf[sillInfo[0]]
    headerPartNum = headerProfile + Constants.colors[row[6]] + "296"

    # Write header row to batch file
    headerTemplate = [sillInfo[1], "1", returnLineNumber(row[2]), row[1], row[3], row[4], headerPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "HEADER", "HEADER", "", "", "", batchData[0], headerProfile, "316920"]
    
    return [headerTemplate]

#   addJambCovers(filename, row, batchData[orderLineID], currentConfig, jambLength, rowsAdded)
def addJambCovers(row, batchData, currentConfig, jambLength):

    # Jamb cover part number
    JCPartNo = "703A" + Constants.colors[row[6]] + "197"

    # Add jamb cover to 
    jambCoverTemplate = [jambLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], JCPartNo,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "JAMB SCREW CVR", "JAMB SCREW CVR", "", "", "", batchData[0], "703", "316920"]
    JBQTY = int(currentConfig.coverQty)
    rowsAdded = [jambCoverTemplate]*JBQTY
    return rowsAdded
            
# Add pocket hook covers SGD
def addPocketHookCovers(row, batchData, pocketLength, pocketQTY):
    # Jamb cover part number
    PHCPartNum = "510" + Constants.colors[row[6]] + "197"

    # Add jamb cover to 
    pocketHookCoverTemplate = [pocketLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], PHCPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "POCKET HOOK CVR", "POCKET HOOK CVR", "", "", "", batchData[0], "510", "316920"]
    rowsAdded = [pocketHookCoverTemplate]*pocketQTY
    return rowsAdded

# Add pocket hooks SGD
def addPocketHooks(row, batchData, pocketLength, pocketQTY):

    # Jamb cover part number
    PHPartNum = "726" + Constants.colors[row[6]] + "197"

    # Add jamb cover to 
    pocketHookTemplate = [pocketLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], PHPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "POCKET HOOK", "POCKET HOOK", "", "", "", batchData[0], "726", "316920"]
    rowsAdded = [pocketHookTemplate]*pocketQTY
    
    return rowsAdded

# Add stiles SGD   
def addStiles(row, batchData, currentConfig, sashRailsMissing):
    # rowsAdded = []
    # Generate stiles for current sash (current sash defined by tracking number: row[0])
    stilesInfo = GenerateStiles.getSashInfo(row, Constants.colors[row[6]], currentConfig)
    leftRowTemplate = [str(row[9]), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[0],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "LEFT STILE", "LEFT STILE", "", "", "", batchData[0], stilesInfo[2], "316920"]
    rightRowTemplate = [str(row[9]), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[1],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "RIGHT STILE", "RIGHT STILE", "", "", "", batchData[0], stilesInfo[3], "316920"]
    rowsAdded = [leftRowTemplate]
    rowsAdded.append(rightRowTemplate)

    # Add reinforcements if they exist
    if stilesInfo[4] is not None:
        # Left stile reinforcement
        print("Adding reinforcement for left stile...")
        leftReinforecmentTemplate = [str(float(row[9])-4.75), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[4],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "STILE REINFORCEMENT", "STILE REINFORCEMENT", "", "", "", batchData[0], stilesInfo[5], "316920"]
        rowsAdded.append(leftReinforecmentTemplate)

    if stilesInfo[6] is not None:
        # Right stile reinforcement
        print("Adding reinforcement for right stile...")
        rightReinforecmentTemplate = [str(float(row[9])-4.75), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[6],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "STILE REINFORCEMENT", "STILE REINFORCEMENT", "", "", "", batchData[0], stilesInfo[7], "316920"]
        rowsAdded.append(rightReinforecmentTemplate)

    # Check if entire sash was missing. If so, add rails as well
    if sashRailsMissing:
        print("Looks like the whole sash was missin, lemme pop them rails in for ya...")
        railLength = str(float(row[12])-0.188)
        TOP_PART_NUM = "709" + Constants.colors[row[6]] + "197"
        BOTTOM_PART_NUM = "710" + Constants.colors[row[6]] + "197"
        topRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], TOP_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "TOP RAIL", "TOP RAIL", "", "", "", batchData[0], "709", "316920"]
        bottomRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], BOTTOM_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "BOTTOM RAIL", "BOTTOM RAIL", "", "", "", batchData[0], "710", "316920"]
        rowsAdded.append(topRailTemplate)
        rowsAdded.append(bottomRailTemplate)


    return [str(row[9]), rowsAdded]

# Add screens SGD
def addScreens(row, batchData, stileLength):
    rowsAdded = []
    # Screen part numbers
    scrRailPartNum = "712" + Constants.colors[row[6]] + "197"
    scrStilePartNum = "713" + Constants.colors[row[6]] + "197"
    scrAstragalPartNum = "714" + Constants.colors[row[6]] + "197"
    
    # Screen rows
    screenRailTemplate = [row[10], "2", returnLineNumber(row[2]), row[1], row[3], row[4], scrRailPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SCREEN RAILS", "SCREEN RAILS", "", "", "", batchData[0], "712", "316920"]
    screenStileTemplate = [stileLength, "2", returnLineNumber(row[2]), row[1], row[3], row[4], scrStilePartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SCREEN STILES", "SCREEN STILES", "", "", "", batchData[0], "713", "316920"]
    screenAstragalTemplate = [stileLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], scrAstragalPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "ASTRAGAL", "ASTRAGAL", "", "", "", batchData[0], "714", "316920"]
    
    # Add the rails and stiles. Only add astragal if user requests it
    rowsAdded.append(screenRailTemplate)
    rowsAdded.append(screenStileTemplate)
    if row[14] == "T":
        rowsAdded.append(screenAstragalTemplate)
    elif row[14] == "F":
        pass
    else:
        print("THIS WAS NOT ACTUALLY THE ASTRAGAL T/F FAMILY")
    return rowsAdded



############### PIVOT AND BIFOLD METHODS ###############
# Add sweep adapters PB
def addSweepAdapters(row, batchData):
    rowsAdded = []
    railLength = str(round(row[9],3))
    SA_PROF = "809"
    SA_PART_NUM = SA_PROF + "M197"
    sweepAdapterTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], SA_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SWEEP ADAPTER", "SWEEP ADAPTER", "", "", "", batchData[0], SA_PROF, "343920"]
    rowsAdded.append(sweepAdapterTemplate)
    rowsAdded.append(sweepAdapterTemplate)
    return rowsAdded

# Add jamb covers PB
def addJambCoversPB(row, batchData):
    rowsAdded = []
    jambLength = str(round(row[10],3))
    PROF = "808"
    PART_NUM = PROF + Constants.colors[row[6]] + "300"
    jambCoverTemplate = [jambLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "JAMB SCREW CVR", "JAMB SCREW CVR", "", "", "", batchData[0], PROF, "343920"]
    rowsAdded.append(jambCoverTemplate)
    rowsAdded.append(jambCoverTemplate)
    return rowsAdded

# Add rails PB
def addPBRail(row, batchData, PART_DESC):
    railLength = str(round(row[9],3))

    # Change print message depending on what was missing
    if PART_DESC == "TOP RAIL":
        RAIL_PROF = Constants.PBRails[str(int(row[7]))]
        print("Top rail was missing")

    elif PART_DESC == "BOTTOM RAIL":
        RAIL_PROF = Constants.PBRails[str(int(row[8]))]
        print("Bottom rail was missing")
    RAIL_PART_NUM = RAIL_PROF + Constants.colors[row[6]] + "197"
    topRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], RAIL_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", PART_DESC, PART_DESC, "", "", "", batchData[0], RAIL_PROF, "343920"]


    rowsAdded = [topRailTemplate]

    return rowsAdded