import queryServer, time

startTime = time.time()
totalRowsAdded = queryServer.beginScript()
executionTime = (time.time() - startTime)
print("***************************************************************")
print("     Total rows added using script across batches: " + str(totalRowsAdded))
print('                Execution time in seconds: ' + str(round(executionTime,1)))
print("***************************************************************")