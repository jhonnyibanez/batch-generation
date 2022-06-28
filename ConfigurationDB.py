import csv, Constants

# 8: jamb cover qty, 9-28 stiles
class AOfamily():
    # Create dict of sashes for current configuration
    def generateSashes(self, configRow, stileTypeRow):
        # Initialize sash object and number
        sashes = {}
        sashNum = 1
        SASH_DATA_BEGIN = 9
        SASH_DATA_END = 28

        # Go through each sash position
        for i in range(SASH_DATA_BEGIN, SASH_DATA_END, 2):
            # Check if current sash exists in that configuration database (csv)
            if configRow[i] and configRow[i+1]:
                # Define current sashes stiles and add stiles to dict
                currentSash = "S" + str(sashNum)
                sashes[currentSash] = {
                    "leftStile": {
                        "prof": configRow[i],
                        "ID" : stileTypeRow[i]
                        },
                    "rightStile": {
                        "prof": configRow[i+1],
                        "ID" : stileTypeRow[i+1]
                        },
                }

                # Increment sash number for next two loops
                sashNum += 1

        return sashes
    
    # Check for dependencies
    def __init__(self, configRow, stileTypeRow):
        # Dependencies
        self.family = configRow[0]
        self.HP = configRow[1]
        self.CONF = configRow[2]
        self.handing = configRow[4] if configRow[4] else False
        self.track = configRow[5] if configRow[5] else False
        self.meeting = configRow[6] if configRow[6] else False
        self.screens = True if configRow[7] else False
        
        # Sashes, jamb cover quantities, and configuration description
        self.description = configRow[3]
        self.coverQty = configRow[8]
        self.sashes = self.generateSashes(configRow, stileTypeRow)

class Dependencies():
    def __init__(self,row):
        # Dependencies
        self.AO = row[0]
        self.HP = row[1]
        self.CONF = row[2]
        self.TRCO = row[3]

        self.AR = True if row[4] else False
        self.MEET = True if row[5] else False
        
# Create database of configurations
def createConfigurationDB():
    configListFilename = "SGD UCFG Configurations.csv"
    stileTypeFilename = "StileTypeIDs.csv"
    AOFamilies = []

    with open(configListFilename, encoding='utf-8-sig') as configFile, open(stileTypeFilename, encoding='utf-8-sig') as stileTypeFile:
        configReader = list(csv.reader(configFile)) # Create a new reader    
        stileTypeReader = list(csv.reader(stileTypeFile)) # Create a new reader    
        
    # Generate each configuration and append to list
    for i in range(len(configReader)):
        AOFamilies.append(AOfamily(configReader[i], stileTypeReader[i]))
    
    return AOFamilies

# Define dependencies for configuration families
def defineDependencyDB():
    dependencyFilename = "CONFDependencies.csv"
    CONFdependencies = []

    with open(dependencyFilename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile) # Create a new reader    
        
        # Generate each configuration and append to list
        for row in reader:
            CONFdependencies.append(Dependencies(row))
    
    return CONFdependencies

# Match order's configuration to one in the database
def pickConfiguration(families, dependencies, row, hasScreens):
    # Find out what the current configuration depends on
    for entry in dependencies:
        if entry.AO == row[5] and entry.CONF == row[8] and entry.HP == row[13] and entry.TRCO == str(row[11]):
            dependsOn = entry
            if dependsOn.AR:
                dependsOn.AR = row[7]
            if dependsOn.MEET:
                while True:
                    dependsOn.MEET = input("Meeting: [Please enter 'OLD' or 'NEW']: ").upper()
                    if dependsOn.MEET in Constants.acceptedMeet:
                        break
                break

    # Find configuration details in database
    for config in families:
        # MUST MATCH: AO, CONF, HP, TRCO, AR, meeting stiles, presence of screens
        if (config.family == dependsOn.AO and config.CONF == dependsOn.CONF and config.HP == dependsOn.HP and config.track == dependsOn.TRCO 
            and config.handing == dependsOn.AR and config.meeting == dependsOn.MEET and config.screens == hasScreens):
            
            # Found the current configurations, return it 
            return config