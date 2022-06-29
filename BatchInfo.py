import csv
# import _SGDCONFIGLIST

# Return dispatch ID, date
def getBatchInfo(batchFilename, orderlineID):
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile)  
        for row in batchReader:
            if (row[3] + row[2]) == orderlineID:
                return [row[17], row[10]]

# Return sill profile and length
def getPartInfo(fileList, orderlineID, partSearched=None):
    # Search values depending on inputs
    HEADER_SEARCH = "SILL"
    ASSY_PART = ["LH JAMB", "RH JAMB", "POCKET HOOK CVR", "POCKET HOOK"]

    # If looking for header info
    if partSearched == "HEADER":
        for row in fileList:
            if (row[3] + row[2]) == orderlineID and row[12] == HEADER_SEARCH:
                return [row[18], row[0]]
        sillLength = input("!*!*!*!*!*!*!*!*!*!*!*!*!I couldn't find a sill length T-T Please enter sill length: ")
        sillProfile = input("!*!*!*!*!*!*!*!*!*!*!*!*!I couldn't find a sill profile T-T Please enter sill profile: ")
        return [sillProfile, sillLength]
    # If looking for jamb cover or pocket hook (cvr) info (RETURN VALUE IS SLIGHTLY DIFFERENT)
    else:
        for row in fileList:
            if (row[3] + row[2]) == orderlineID and row[12] in ASSY_PART:
                if partSearched == "JAMB CVR":
                    return str(float(row[0]) - 0.187)
                elif partSearched is None:
                    return str(row[0]) 
    
        jambLength = input("!*!*!*!*!*!*!*!*!*!*!*!*!I couldn't find a jamb length T-T Please enter jamb length: ")
        if partSearched == "JAMB CVR":
            return str(float(jambLength) - 0.187)
        else:
            return jambLength

            



# Return sill profile and length
def getSillInfo(fileList, orderlineID):
    ASSY_PART = "SILL"
    for row in fileList:
        if (row[3] + row[2]) == orderlineID and row[12] == ASSY_PART:
            return [row[18], row[0]]
    
# Return jamb length for jamb cvr length
def getJambLength(batchFilename, orderlineID):
    ASSY_PART = ["LH JAMB", "RH JAMB", "POCKET HOOK CVR", "POCKET HOOK"]
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile)  
        for row in batchReader:
            if (row[3] + row[2]) == orderlineID and row[12] in ASSY_PART:
                return str(float(row[0]) - 0.187)
        jambLength = input("!*!*!*!*!*!*!*!*!*!*!*!*!I couldn't find a jamb length T-T Please enter jamb cvr length: ")
        return jambLength
    
# Return jamb length for jamb cvr length
def getPocketLength(batchFilename, orderlineID):
    ASSY_PART = ["LH JAMB", "RH JAMB", "POCKET HOOK CVR", "POCKET HOOK"]
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile)  
        for row in batchReader:
            if (row[3] + row[2]) == orderlineID and row[12] in ASSY_PART:
                return str(row[0])
        jambLength = input("!*!*!*!*!*!*!*!*!*!*!*!*!I couldn't find a jamb length T-T Please enter jamb cvr length: ")
        return jambLength

# define user input for config
def dependencyNEW(row, currentConfig):
    acceptedMeet = ["OLD", "NEW"]

    # Define the AO family and CONF
    AO = row[5]
    CONF = row[8]
    HP = row[13]
    TRCO = row[11]


    # Check for handing dependency
    if currentConfig.family == AO and currentConfig.configuration == CONF and currentConfig.HP == HP and currentConfig.track == TRCO:
        if currentConfig.handing != "NONE":
            if row[7] == "ARAA":
                userHanding = "LH"
            elif row[7] == "ARAB":
                userHanding = "RH"
            elif row[7] is None :
                userHanding = input("COULDN'T FIND IT CAUSE ORDER MESSED UP? ENTER AR FAMILY PLS (NONE IS ACCEPTABLE): ")
        else:
            userHanding = "NONE"

    # Check for meeting stile dependency
        if currentConfig.meeting != "NONE":
            while True:
                userMeeting = input("Meeting: [Please enter 'OLD' or 'NEW']: ").upper()
                if userMeeting in acceptedMeet:
                    break
        else:
            userMeeting = "NONE"
    else:
        print("PICKED THE WRONG CONFIGURATION. SHIEEEEEEEEEEEEEEEEEET")
            
    
    # Return dependencies
    return [AO, CONF, userHanding, userTrack, userMeeting]


def getOriginalRowCount(batchFilename):
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile)
        return len(list(batchReader))