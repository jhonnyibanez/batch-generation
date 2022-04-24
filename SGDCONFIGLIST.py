import csv
import re

sgdStiles = {}
configObject = {}
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

# class SGDConfigurations:
#     def __init__(self, AOfamily):
#         self.family = AOfamily
        
class AOfamily:
    def __init__(self, family, configuration, handing, track, meeting, sashes):
        self.family = family
        self.configuration = configuration
        self.handing = handing
        self.track = track
        self.meeting = meeting
        self.sashes = sashes

# class Sashes:
#     def __init__(self, sashes):
#         self.sashes = sashes


# Create dict of sashes for current configuration
def generateSashes(row):
    # Initialize sash object and number
    sashes = {}
    sashNum = 1

    # Go through each sash position
    for i in range(5, 14):
        # Check if sash exists in that configuration
        if row[i]:

            currentSash = "S" + str(sashNum)
            sashes[currentSash] = None

            # Define current sashes stiles
            sashStiles = {
                "leftStile": row[i].split("/")[0][0:3],
                "rightStile": row[i].split("/")[1][0:3],
            }

            # Index current sash in sashes object, add stilles
            sashes[currentSash] = sashStiles

            # Increment sash number for next loop
            sashNum += 1

    return sashes
   

configListFilename = "SGD Stiles by Configuration - Python List.csv"


# AO = ["KM", "KMHI", "KM12"]
AOFamilies = []
linesList = []

# Create database of configurations
with open(configListFilename) as infile:
    reader = csv.reader(infile) # Create a new reader    

    for row in reader:
        # Configuration and family
        configuration = row[1]
        family = row[0]
        
        # Check for dependencies
        handing = row[2] if row[2] else "NONE"
        track = row[3] if row[3] else "NONE"
        meeting = row[4] if row[4] else "NONE"
        
        # Generate sashes
        sashes = generateSashes(row)
        # Make a list of all configuration instances
        AOFamilies.append(AOfamily(family, configuration, handing, track, meeting, sashes))

# print(AOFamilies)