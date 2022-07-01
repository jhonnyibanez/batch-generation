import pyodbc, os, time, colorama
import Constants, ConfigurationDB, EditFile
server = 'SERVER'
database = 'DATABASE-NAME'
username = 'ENTER-USERNAME-HERE'
password = 'ENTER-PASSWORD-HERE'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Reset colors automatically
colorama.init(autoreset = True)

# Script entry
def beginScript():
    # Define producting location and batch number
    while True:
        prodLoc = input("What producing location? [Enter 'CM', 'SF', 'WIN', 'SGD', 'FD', 'PB', or 'GD']: ").upper()
        if prodLoc in Constants.producingLoc:
            break
        
    # Edit batch files
    rowsAddedArray = autoEditBatchFile(prodLoc)

    # Sum up all rows added for output
    totalRowsAdded = sum(rowsAddedArray)
    return totalRowsAdded

# SELECT query
def queryBatch(batchNumber, prodLoc):
    print ('Querying batch number ' + batchNumber)
    tsql = """SELECT """ + str(Constants.tableCols[prodLoc]) + """ FROM """ + str(Constants.SQLTables[prodLoc]) + """
    WHERE (producingLocationID = """ + str(Constants.producingLocID[prodLoc]) + """) AND (batchNumber = """ + batchNumber + """)  ORDER BY unit.trackingNumber;"""
    with cursor.execute(tsql):
        return cursor.fetchall()
        # print(cursor.fetchall())

# Edit batch files specified by user
def autoEditBatchFile(prodLoc):
    totalRowsAdded = []
    initRowCounts = []

    # Decide to audit one batch or all :)
    while True:
        decision = input("Do you want to run all batches in folder or specific quantity? [Please enter specific quantity or 'ALL']: ").upper()
        if decision.isnumeric() or decision == 'ALL':
            break
    
    # Define batch filenames and query results
    print ('Connected to SQL')
    print('Hacking the mainframe...')
    [filenames, queries, totalQueryTime] = defineBatches(decision, prodLoc)
    print(colorama.Fore.LIGHTCYAN_EX + colorama.Back.WHITE + "###########################################################################")
    print(colorama.Fore.LIGHTCYAN_EX + colorama.Back.WHITE + "                    Total time to execute queries: " + str(round(totalQueryTime,1)))
    print(colorama.Fore.LIGHTCYAN_EX + colorama.Back.WHITE + "###########################################################################")

    # Define configuration list and dependecy list from 'database'
    if prodLoc == "SGD":
        CONFIGURATIONS = ConfigurationDB.createConfigurationDB()
        DEPENDENCIES = ConfigurationDB.defineDependencyDB()

    # Run for as many batches requested or in folder
    for batch in range(0,len(filenames)):
        print("")
        print(colorama.Fore.BLUE + colorama.Back.WHITE + "###########################################################################")
        print(colorama.Fore.BLUE + colorama.Back.WHITE + "                    NOW AUDTIING BATCH FILE: " + os.path.basename(filenames[batch]))
        print(colorama.Fore.BLUE + colorama.Back.WHITE + "###########################################################################")
        print("")
        
        # Record Start Time
        auditStartTime = time.time()

        # Audit batch
        if prodLoc == "SGD":
            [initialRowCount, rowsAdded] = EditFile.addMissingSGDProfiles(filenames[batch], queries[batch], CONFIGURATIONS, DEPENDENCIES)
        elif prodLoc == "PB":
            [initialRowCount, rowsAdded] = EditFile.addMissingPBProfiles(filenames[batch], queries[batch])
        # Might not need initial row counts?
        initRowCounts.append(initialRowCount)
        totalRowsAdded.append(rowsAdded)
        
        # Calculate time to audit
        auditExecutionTime = (time.time() - auditStartTime)

        print("")
        print(colorama.Fore.WHITE + colorama.Back.GREEN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(colorama.Fore.WHITE + colorama.Back.GREEN + "                     Rows present when started: " + str(initialRowCount) )
        print(colorama.Fore.WHITE + colorama.Back.GREEN + "                              Rows added: " + str(rowsAdded))
        print(colorama.Fore.WHITE + colorama.Back.GREEN + '                    Execution time in seconds: ' + str(round(auditExecutionTime,1)))
        print(colorama.Fore.WHITE + colorama.Back.GREEN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("")

    return totalRowsAdded

# Generate list of batch file names and query results for batch(es) user requests
def defineBatches(decision, prodLoc):
    # Define PENDING TO CHECK folder, directory constants, and initialize file and query lists
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    FOLDER_DIR_END = 45
    FILE_PREFIX = Constants.filePrefix[prodLoc]
    filenames = []
    queries = []


    # All batches
    if decision == 'ALL':
        # Start time
        queryStartTime = time.time()
        for file in os.listdir(THIS_FOLDER[0:FOLDER_DIR_END]):
            if file.startswith(FILE_PREFIX):
                # Grab only the "batch number" portion of the file name 
                batchNumber = file.split('_')[1].split('.')[0]
                
                # Check that this is not a batch we set aside by editing the name
                if batchNumber.isnumeric():
                    # Generate batch filename list
                    batchFile = FILE_PREFIX + batchNumber + ".csv"
                    batchFilename = os.path.join(THIS_FOLDER[0:FOLDER_DIR_END], batchFile)
                    filenames.append(batchFilename)
                    
                    # Query batch, generate query results list
                    query = queryBatch(batchNumber, prodLoc)
                    queries.append(query)
    # Only one batch
    else:
        batchNumberList = []
        for i in range(int(decision)):
            # Generate batch filename
            while True:
                batchNumber = input("Input batch number " + str(i+1) + " : ")
                if batchNumber.isnumeric():
                    batchNumberList.append(batchNumber)
                    break

            # Start time
            batchFile = FILE_PREFIX + batchNumber + ".csv"
            batchFilename = os.path.join(THIS_FOLDER[0:45], batchFile)
            filenames.append(batchFilename)

        queryStartTime = time.time()
        for batchNum in batchNumberList:
            # Query batch
            query = queryBatch(batchNum, prodLoc)
            queries.append(query)
    
    # End time
    queryExecutionTime = (time.time() - queryStartTime)

    return [filenames, queries, queryExecutionTime]