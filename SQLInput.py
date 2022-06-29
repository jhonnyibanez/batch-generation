# OBSOLETE
import csv, os
keepRows = list()
filename = "\\raptor\OPT_FILES\SIW_MAIN\PENDING TO CHECK\SGDMET_5164.CSV"
# Read original batch file into a list. Edit this list instead of openning file constantly
################# DONT DELETE
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
batchFile = "SGDMET_5164.CSV"
batchFilename = os.path.join(THIS_FOLDER[0:45], batchFile)
################# DONT DELETE



def readOGFile(filename):
    with open(filename, 'r') as infile:
        batchReader = csv.reader(infile)  
        OGFile = list(batchReader)
    return OGFile

saveresults = readOGFile(batchFilename)

tempList = [saveresults[0]]*10
print("test")