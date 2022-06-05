# OBSOLETE
import csv
keepRows = list()
filename = "\\raptor\OPT_FILES\SIW_MAIN\PENDING TO CHECK\SGDMET_17184.CSV"
with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
    batchReader = csv.reader(csvfile)  
    for row in batchReader:
            keepRows.append(row)

for row in keepRows:
    print(row)