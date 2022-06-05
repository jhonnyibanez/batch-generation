import csv, Constants

# 8: jamb cover qty, 9-28 stiles
class AOfamily():
    # Create dict of sashes for current configuration
    def generateSashes(self, row):
        # Initialize sash object and number
        sashes = {}
        sashNum = 1
        SASH_DATA_BEGIN = 9
        SASH_DATA_END = 28

        # Go through each sash position
        for i in range(SASH_DATA_BEGIN, SASH_DATA_END, 2):
            # Check if current sash exists in that configuration database (csv)
            if row[i] and row[i+1]:
                # Define current sashes stiles and add stiles to dict
                currentSash = "S" + str(sashNum)
                sashes[currentSash] = {
                    "leftStile": row[i],
                    "rightStile": row[i+1],
                }

                # Increment sash number for next two loops
                sashNum += 1

        return sashes
    
    # Check for dependencies
    def __init__(self, row):
        # Dependencies
        self.family = row[0]
        self.HP = row[1]
        self.CONF = row[2]
        self.handing = row[4] if row[4] else False
        self.track = row[5] if row[5] else False
        self.meeting = row[6] if row[6] else False
        self.screens = True if row[7] else False
        
        # Sashes, jamb cover quantities, and configuration description
        self.description = row[3]
        self.coverQty = row[8]
        self.sashes = self.generateSashes(row)

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
    AOFamilies = []

    with open(configListFilename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile) # Create a new reader    
        
        # Generate each configuration and append to list
        for row in reader:
            AOFamilies.append(AOfamily(row))
    
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