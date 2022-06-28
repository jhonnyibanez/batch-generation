import csv

def deleteSGDStiles(batchFilename):
    keepRows = list()
    stiles = ["LEFT STILE", "RIGHT STILE"]
    with open(batchFilename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if len(row) > 0 and row[13] not in stiles:
                keepRows.append(row)

    with open(batchFilename, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(keepRows)
    
def deleteSGDJambCovers(batchFilename):
    keepRows = list()
    JAMB_CVR_DESC = "JAMB SCREW CVR"
    with open(batchFilename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if len(row) > 0 and row[13] != JAMB_CVR_DESC:
                keepRows.append(row)

    with open(batchFilename, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(keepRows)

def deleteSGDReinforcements(batchFilename):
    keepRows = list()
    REINFORCEMENT_DESC = "STILE REINFORCEMENT"
    with open(batchFilename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if len(row) > 0 and row[13] != REINFORCEMENT_DESC:
                keepRows.append(row)

    with open(batchFilename, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(keepRows)


def deleteExtraSGDJambs(batchFilename, orderNum, lineNum, initialRowCount, POCKET_ID):
    keepRows = list()

    # Define jambs to delete
    if POCKET_ID == "L":
        JAMB_DESC = ["LH JAMB"]
    elif POCKET_ID == "R":
        JAMB_DESC = ["RH JAMB"]
    elif POCKET_ID == "B":
        JAMB_DESC = ["LH JAMB", "RH JAMB"]

    with open(batchFilename, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if len(row) > 0:
                if  row[3] == orderNum and row[2] == lineNum:
                    # Pretty sure I can combine this if statement with the one above but idc
                    if row[13] not in JAMB_DESC:
                        keepRows.append(row)
                    else:
                        initialRowCount -= 1
                else:
                    keepRows.append(row)

    with open(batchFilename, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(keepRows)
    
    return initialRowCount
