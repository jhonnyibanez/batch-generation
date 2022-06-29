import csv
# Delete stiles, jamb covers, and reinforcementss
def deleteSGDGarbageValues(fileList):
    keepRows = list()
    deletedComponents = ["LEFT STILE", "RIGHT STILE", "JAMB SCREW CVR", "STILE REINFORCEMENT"]
    for row in fileList:
        if row[13] not in deletedComponents:
            keepRows.append(row)

    return keepRows

# Delete extra jambs for pocket doors
def deleteExtraSGDJambs(fileList, orderNum, lineNum, POCKET_ID):
    keepRows = list()

    # Define jambs to delete
    if POCKET_ID == "L":
        JAMB_DESC = ["LH JAMB"]
    elif POCKET_ID == "R":
        JAMB_DESC = ["RH JAMB"]
    elif POCKET_ID == "B":
        JAMB_DESC = ["LH JAMB", "RH JAMB"]
    
    # Delete corresponding extra jambs
    for row in fileList:
        if row[3] == orderNum and row[2] == lineNum:
            if row[13] not in JAMB_DESC:
                keepRows.append(row)
        else:
            keepRows.append(row)    
    return keepRows
