from cmath import nan
import csv, GenerateStiles, Constants

def returnLineNumber(line):
    if line.isdigit():
        return line
    else:
        return line[0:len(line)-1]

# 0tracking, 1order, 2line, 3batch, 4slot, 5AO, 6AJE, 7AR, 8CONF, 9Stile length, 10Screen Rail Length
def addHeader(filename, row, batchData, sillInfo, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header part number
        headerProfile = Constants.headerProf[sillInfo[0]]
        headerPartNum = headerProfile + Constants.colors[row[6]] + "296"
 
        # Write header row to batch file
        headerTemplate = [sillInfo[1], "1", returnLineNumber(row[2]), row[1], row[3], row[4], headerPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "HEADER", "HEADER", "", "", "", batchData[0], headerProfile, "316920"]
        writer.writerow(headerTemplate)
        rowsAdded += 1 
    return rowsAdded

#   addJambCovers(filename, row, batchData[orderLineID], currentConfig, jambLength, rowsAdded)
def addJambCovers(filename, row, batchData, currentConfig, jambLength, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Jamb cover part number
        JCPartNo = "703A" + Constants.colors[row[6]] + "197"

        # Add jamb cover to 
        jambCoverTemplate = [jambLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], JCPartNo,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "JAMB SCREW CVR", "JAMB SCREW CVR", "", "", "", batchData[0], "703", "316920"]
        JBQTY = int(currentConfig.coverQty)
        for i in range(JBQTY):
            writer.writerow(jambCoverTemplate)
            rowsAdded += 1 
    return rowsAdded
            
# Add pocket hook covers SGD
def addPocketHookCovers(filename, row, batchData, pocketLength, pocketQTY, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Jamb cover part number
        JCPartNo = "510" + Constants.colors[row[6]] + "197"

        # Add jamb cover to 
        pocketHookCoverTemplate = [pocketLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], JCPartNo,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "POCKET HOOK CVR", "POCKET HOOK CVR", "", "", "", batchData[0], "510", "316920"]
        for i in range(pocketQTY):
            writer.writerow(pocketHookCoverTemplate)
            rowsAdded += 1 
    return rowsAdded

# Add pocket hooks SGD
def addPocketHooks(filename, row, batchData, pocketLength, pocketQTY, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Jamb cover part number
        JCPartNo = "726" + Constants.colors[row[6]] + "197"

        # Add jamb cover to 
        pocketHookTemplate = [pocketLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], JCPartNo,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "POCKET HOOK", "POCKET HOOK", "", "", "", batchData[0], "726", "316920"]
        for i in range(pocketQTY):
            writer.writerow(pocketHookTemplate)
            rowsAdded += 1 
    return rowsAdded

# Add stiles SGD   
def addStiles(filename, row, batchData, currentConfig, sashRailsMissing, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Generate stiles for current sash (current sash defined by tracking number: row[0])
        stilesInfo = GenerateStiles.getSashInfo(row, Constants.colors[row[6]], currentConfig)
        leftRowTemplate = [str(row[9]), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[0],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "LEFT STILE", "LEFT STILE", "", "", "", batchData[0], stilesInfo[2], "316920"]
        rightRowTemplate = [str(row[9]), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[1],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "RIGHT STILE", "RIGHT STILE", "", "", "", batchData[0], stilesInfo[3], "316920"]
        writer.writerow(leftRowTemplate)
        writer.writerow(rightRowTemplate)
        rowsAdded += 2

        # Add reinforcements if they exist
        if stilesInfo[4] is not None:
            # Left stile reinforcement
            print("Adding reinforcement for left stile...")
            leftReinforecmentTemplate = [str(float(row[9])-4.75), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[4],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "STILE REINFORCEMENT", "STILE REINFORCEMENT", "", "", "", batchData[0], stilesInfo[5], "316920"]
            writer.writerow(leftReinforecmentTemplate)
            rowsAdded += 1

        if stilesInfo[6] is not None:
            # Right stile reinforcement
            print("Adding reinforcement for right stile...")
            rightReinforecmentTemplate = [str(float(row[9])-4.75), "1", returnLineNumber(row[2]), row[1], row[3], row[4], stilesInfo[6],"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "STILE REINFORCEMENT", "STILE REINFORCEMENT", "", "", "", batchData[0], stilesInfo[7], "316920"]
            writer.writerow(rightReinforecmentTemplate)
            rowsAdded += 1

        # Check if entire sash was missing. If so, add rails as well
        if sashRailsMissing:
            print("Looks like the whole sash was missin, lemme pop them rails in for ya...")
            railLength = str(float(row[12])-0.188)
            TOP_PART_NUM = "709" + Constants.colors[row[6]] + "197"
            BOTTOM_PART_NUM = "710" + Constants.colors[row[6]] + "197"
            topRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], TOP_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "TOP RAIL", "TOP RAIL", "", "", "", batchData[0], "709", "316920"]
            bottomRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], BOTTOM_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "BOTTOM RAIL", "BOTTOM RAIL", "", "", "", batchData[0], "710", "316920"]
            writer.writerow(topRailTemplate)
            writer.writerow(bottomRailTemplate)
            rowsAdded += 2


        return [str(row[9]), rowsAdded]

# Add screens SGD
def addScreens(filename, row, batchData, stileLength, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Screen part numbers
        scrRailPartNum = "712" + Constants.colors[row[6]] + "197"
        scrStilePartNum = "713" + Constants.colors[row[6]] + "197"
        scrAstragalPartNum = "714" + Constants.colors[row[6]] + "197"
        
        # Screen rows
        screenRailTemplate = [row[10], "2", returnLineNumber(row[2]), row[1], row[3], row[4], scrRailPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SCREEN RAILS", "SCREEN RAILS", "", "", "", batchData[0], "712", "316920"]
        screenStileTemplate = [stileLength, "2", returnLineNumber(row[2]), row[1], row[3], row[4], scrStilePartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SCREEN STILES", "SCREEN STILES", "", "", "", batchData[0], "713", "316920"]
        screenAstragalTemplate = [stileLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], scrAstragalPartNum,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "ASTRAGAL", "ASTRAGAL", "", "", "", batchData[0], "714", "316920"]
        
        # Add the rails and stiles. Only add astragal if user requests it
        writer.writerow(screenRailTemplate)
        writer.writerow(screenStileTemplate)
        rowsAdded += 2
        if row[14] == "T":
            writer.writerow(screenAstragalTemplate)
            rowsAdded += 1
        elif row[14] == "F":
            # DO NOTHING
            print()
        else:
            print("THIS WAS NOT ACTUALLY THE ASTRAGAL T/F FAMILY")
    return rowsAdded

# Add sweep adapters PB
def addSweepAdapters(filename, row, batchData, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        railLength = str(row[9])
        SA_PROF = "809"
        SA_PART_NUM = SA_PROF + "M197"
        sweepAdapterTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], SA_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "SWEEP ADAPTER", "SWEEP ADAPTER", "", "", "", batchData[0], SA_PROF, "343920"]
        writer.writerow(sweepAdapterTemplate)
        writer.writerow(sweepAdapterTemplate)
        rowsAdded += 2
    return rowsAdded

# Add jamb covers PB
def addJambCoversPB(filename, row, batchData, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        jambLength = str(row[10])
        PROF = "808"
        PART_NUM = PROF + Constants.colors[row[6]] + "300"
        jambCoverTemplate = [jambLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "JAMB SCREW CVR", "JAMB SCREW CVR", "", "", "", batchData[0], PROF, "343920"]
        writer.writerow(jambCoverTemplate)
        writer.writerow(jambCoverTemplate)
        rowsAdded += 2
    return rowsAdded

# Add rails PB
def addPBRails(filename, row, batchData, topRailMissing, bottomRailMissing, rowsAdded):
    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        railLength = str(row[9])
        TOP_PROF = Constants.PBRails[str(int(row[7]))]
        BOT_PROF = Constants.PBRails[str(int(row[8]))]
        TOP_PART_NUM = TOP_PROF + Constants.colors[row[6]] + "197"
        BOTTOM_PART_NUM = BOT_PROF + Constants.colors[row[6]] + "197"
        topRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], TOP_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "TOP RAIL", "TOP RAIL", "", "", "", batchData[0], TOP_PROF, "343920"]
        bottomRailTemplate = [railLength, "1", returnLineNumber(row[2]), row[1], row[3], row[4], BOTTOM_PART_NUM,"",row[0], Constants.colorCodes[row[6]], batchData[1], "", "BOTTOM RAIL", "BOTTOM RAIL", "", "", "", batchData[0], BOT_PROF, "343920"]
        if topRailMissing and bottomRailMissing:
            print("Rails were missing")
            writer.writerow(topRailTemplate)
            writer.writerow(bottomRailTemplate)
            rowsAdded += 2
        else:
            if topRailMissing:
                print("Top rail was missing")
                writer.writerow(topRailTemplate)
                rowsAdded += 1
            if bottomRailMissing:
                print("Bottom rail was missing")
                writer.writerow(bottomRailTemplate)
                rowsAdded += 1
    return rowsAdded