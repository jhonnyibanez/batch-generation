# 0tracking, 1order, 2line, 3batch, 4slot, 5AO, 6AJE, 7AR, 8CONF, 9Stile length, 10Screen Rail Length
def getSashInfo(row, color, config):
    # Pick current sashes stiles (row[0] is the tracking number)
    sashKey = row[0][-2:]

    # Left stile
    leftStile = config.sashes[sashKey]["leftStile"]
    leftPartNum = leftStile + color + "197"
    
    # Right stile
    rightStile = config.sashes[sashKey]["rightStile"]
    rightPartNum = rightStile + color + "197"

    return [str(leftPartNum), str(rightPartNum), str(leftStile), str(rightStile)] 

# Need to figure out a way to add reinforcements

# def getReinforcements(row, stile, DSPW, DSPH):
#     sashKey = row[0][-2:]
#     if stile == "708":
#         # 901A for any interlock 708
#     elif stile == "706":
#         # 901A for any meeting stile with panel size > 60 x 108
#     elif stile == "718":
#         # Astragal Reinforcement (1/2” X 2-1/2” Aluminum Bar) is required in SIW718 HD Lock Stile profile when used at a Center Meet/Astragal and the Panel height is greater than 120”.
#     elif stile == "738":
#         # 901A for any interlock when DPSW > 60 and DSPH > 82 OR DSPW > 42 and DPSW > 94
    

#     elif stile == "755":
#         # 901E NO MATTER WHAT

