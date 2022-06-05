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
def getSillInfo(batchFilename, orderlineID):
    ASSY_PART = "SILL"
    with open(batchFilename) as infile:
        batchReader = csv.reader(infile)  
        for row in batchReader:
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

# # define user input for config
# def dependencyInput(row):
#     # acceptedAKKA = ["KM", "KMHI"]
#     acceptedMeet = ["OLD", "NEW"]

#     # Define the AO family and CONF
#     if row[5] == "AKKA":
#         if row[13] == "HPHD":
#             AO = "KMHI"
#         elif row[13] == "STAN":
#             AO = "KM"
#         else:
#             print("FUCK, that wasn't the right column to differentiate between KM and KMHI")
#     elif row[5] == "AKKC":
#         AO = "KM12"
#     else:
#         print("BOI THE WRONG AO FAMILY CAME IN? DID WE GET THE RIGHT COLUMN FROM THE SQL SERVER?")
#     CONF = row[8]


#     # Check for handing dependency
#     for AOCONF in _SGDCONFIGLIST.AOFamilies:
#         if AOCONF.family == AO and AOCONF.configuration == CONF:
#             if AOCONF.handing != "NONE":
#                 if row[7] == "ARAA":
#                     userHanding = "LH"
#                 elif row[7] == "ARAB":
#                     userHanding = "RH"
#                 elif row[7] is None :
#                     userHanding = input("COULDN'T FIND IT CAUSE ORDER MESSED UP? ENTER AR FAMILY PLS (NONE IS ACCEPTABLE): ")
#             else:
#                 userHanding = "NONE"

#         # Check for track qty. dependency
#             if AOCONF.track != "NONE":
#                 row[11] = str(row[11]).split(".")[0]
#                 if row[11][0] == "3" or row[11] == "5":
#                     userTrack = "3/5"
#                 elif row[11] == "4":
#                     userTrack = "4"
#                 elif row[11] is None:
#                     # print("BRO DID YOU GET THE RIGHT TRACK NUMBER COLUMN FROM SQL")
#                     userTrack = input("COULDN'T FIND IT CAUSE ORDER MESSED UP? ENTER TRCO FAMILY PLS (NONE IS ACCEPTABLE): ")
#             else:
#                 userTrack = "NONE"

#         # Check for meeting stile dependency
#             if AOCONF.meeting != "NONE":
#                 while True:
#                     userMeeting = input("Meeting: [Please enter 'OLD' or 'NEW']: ").upper()
#                     if userMeeting in acceptedMeet:
#                         break
#             else:
#                 userMeeting = "NONE"
            
#             break
    
#     # Return dependencies
#     return [AO, CONF, userHanding, userTrack, userMeeting]

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