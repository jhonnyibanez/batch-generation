from SGDCONFIGLIST import AOFamilies
import csv
import re

colors = {
    "A": "ANO",
    "B": "BZ IMP",
    "BLKY": "BLK KYNAR",
    "BZKY": "BZ KYNAR",
    "CH": "CHERRY",
    "CI": "CINNAMON",
    "CP": "CUSTOM",
    "H": "HAZELNUT",
    "M": "MILL",
    "OA": "OAK",
    "W": "WH IMP",
    "WHKY": "WH KYNAR",
    "WN": "WALNUT"
}
acceptedFamily = ["KM", "KMHI", "KM12"]
acceptedHand = ["LH", "RH", "NONE"]
acceptedTrack = ["3/5 TRACK", "4 TRACK", "NONE"]
acceptedMeet = ["OLD", "NEW", "NONE"]
orderLineList = []
batchLines = []
batchNo = input("Batch number in file name [SGDMET_#####: ONLY THE #S]: ")
batchFilename = "SGDMET_" + batchNo + ".csv"

class batchLine:
    def __init__(self, lineNo, orderNo, trackPrefix, trackSubNo, dispatchID):
        self.lineNo = lineNo
        self.orderNo = orderNo
        self.trackPrefix = trackPrefix
        self.trackSubNo = trackSubNo
        self.dispatchID = dispatchID


# Add stiles to batch file
def addStilesToFile(sashes, color, length, orderNo, lineNo):
    with open("SGDMET_0TEST.csv", 'a', encoding='UTF8', newline='') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile)

        # write a row to the csv file
        for batch in batchLines:
            if batch.orderNo == orderNo and batch.lineNo == lineNo:
                trackingPrefix = batch.trackPrefix
                sashTrackSubNo = batch.trackSubNo+2
                dispatchID = batch.dispatchID
        
        sashQty = len(sashes)
        for i in range(sashQty):
            sashKey = "S" + str(i+1)
            trackingNum = trackingPrefix + str(sashTrackSubNo+i) + "A2" + sashKey
            # Left stile
            leftStile = sashes[sashKey]["leftStile"]
            leftPartNum = leftStile + color + "197"
            
            # Right stile
            rightStile = sashes[sashKey]["rightStile"]
            rightPartNum = rightStile + color + "197"

            colorCode = colors[color]

            leftRowTemplate = [length, "1", lineNo, orderNo, batchNo, "SLOT",leftPartNum,"",trackingNum,colorCode, "DATE HERE", "", "LEFT STILE", "LEFT STILE", "", "", "", dispatchID, leftStile, "316920"]
            rightRowTemplate = [length, "1", lineNo, orderNo, batchNo, "SLOT",rightPartNum,"",trackingNum,colorCode, "DATE HERE", "", "RIGHT STILE", "RIGHT STILE", "", "", "", dispatchID, rightStile, "316920"]
            writer.writerow(leftRowTemplate)
            writer.writerow(rightRowTemplate)

# Find configuration specified by user in list
# def pickConfig(family, conf, hand, track, meet):
def pickConfig(family, conf, depends, details, orderNo, lineNo):
    for i in AOFamilies:
        if i.family == family and i.configuration == conf:
            # Handing dependencies
            if depends[0] == i.handing and depends[1] == i.track and depends[2] == i.meeting:
                addStilesToFile(i.sashes, details[0], details[1], orderNo, lineNo)


# Read batch file to generate row template variables
with open(batchFilename) as infile:
    batchReader = csv.reader(infile) # Create a new reader    

    for row in batchReader:
        lineNo = row[2]
        orderNo = row[3]
        orderLineID =  orderNo + lineNo
        if orderLineID not in orderLineList:
            # Add to dict of orders and lines
            orderLineList.append(orderLineID)
            # Generate tracking number
            splitTrackingNo = re.findall(r'(\w+?)(\d+)', row[8])
            trackNoPrefix = splitTrackingNo[0][0]
            trackNoSubNo = int(splitTrackingNo[0][1])
            dispatchID = row[17]

            batchLines.append(batchLine(lineNo, orderNo, trackNoPrefix, trackNoSubNo, dispatchID))

        

for j in range(len(orderLineList)):
    # print(userLines+1)
    # Current order line string
    ordertxt = orderLineList[j][0:8]
    linetxt = orderLineList[j][8:len(orderLineList[j])]

    print("Please enter information for line " + ordertxt + "-" + linetxt + "\n")
    
    # Family & Configuration
    while True:
        userAO = input("AO: [Please enter 'KM', 'KMHI', or 'KM12']: ").upper()
        if userAO in acceptedFamily:
            break
    userCONF = input("CONF: ").upper()

    # Dependencies
    while True:
        userHanding = input("Handing: [Please enter 'LH', 'RH', or 'NONE']: ").upper()
        if userHanding in acceptedHand:
            break

    while True:
        userTrack = input("Track: [Please enter '3/5 TRACK', '4 TRACK', or 'NONE']: ").upper()
        if userTrack in acceptedTrack:
            break
    while True:
        userMeeting = input("Meeting: [Please enter 'OLD', 'NEW', or 'NONE']: ").upper()
        if userMeeting in acceptedMeet:
            break

    dependencies = [userHanding, userTrack, userMeeting]
    # Part details
    while True:
        userColor = input("Color: [Please enter color as it appears in part # (A, B, BLKY, M, W, etc..)]: ").upper()
        if userColor in colors:
            break
    userStileLength = input("Stile length: [Please enter one value]: ")
    partDetails = [userColor, userStileLength]
    
    pickConfig(userAO, userCONF, dependencies, partDetails, ordertxt, linetxt)

# [length, ////////////// user
#  "QTY", /////////////// default 1?????????
# "LINE #" ////////////// lineNo
#  "ORDER #", /////////// orderNo
#  "BATCH #", /////////// batchNo
#  "SLOT/BIN #",??????
#  leftPartNum,"",///////
# "TRACKING #", ///////// Have the prefix, just need to add "S{#}" when adding to file
# colorCode, 
# "DATE HERE", "", ??????????
# "LEFT STILE", "LEFT STILE", "", "", "", 
# "DISPATCH ID", leftStile, "316920"] /////////////dispatchID, profile #, 316920