# 0tracking, 1order, 2line, 3batch, 4slot, 5AO, 6AJE, 7AR, 8CONF, 9Stile length, 10Screen Rail Length
def getSashInfo(row, color, config):
    # Pick current sashes stiles (row[0] is the tracking number)
    sashKey = row[0][-2:]

    # Left stile
    leftStile = config.sashes[sashKey]["leftStile"]["prof"]
    leftPartNum = leftStile + color + "197"
    
    # Right stile
    rightStile = config.sashes[sashKey]["rightStile"]["prof"]
    rightPartNum = rightStile + color + "197"

    # Check for reinforcements
    leftReinfPartNum, leftReinfProf = getReinforcements(leftStile, config, config.sashes[sashKey]["leftStile"]["ID"], row[9], float(row[12]))
    rightReinfPartNum, rightReinfProf = getReinforcements(rightStile, config, config.sashes[sashKey]["rightStile"]["ID"], row[9], float(row[12]))
    return [str(leftPartNum), str(rightPartNum), str(leftStile), str(rightStile), leftReinfPartNum, leftReinfProf, rightReinfPartNum, rightReinfProf] 

# Need to figure out a way to add reinforcements

def getReinforcements(stile, config, configID, DSPH, DSPW):
    AO = config.family
    HP = config.HP
    # DSPH should already be numerical but just in case
    DSPW = float(DSPW)
    DSPH = float(DSPH)

    if stile == "708" and configID == "INLK":
        # 901A for any interlock 708
        prof = "901A"
    elif stile == "706" and configID == "CNMT" and not (AO == "AKKA" and HP == "STAN") and (DSPW >= 60 or DSPH >= 108):
        prof = "901A"
    elif stile == "718" and configID == "CNMT" and DSPH >= 120:
        # Astragal Reinforcement (1/2” X 2-1/2” Aluminum Bar) is required in SIW718 HD Lock Stile profile when used at a Center Meet/Astragal and the Panel height is greater than 120”.
        prof = "901A"
    elif stile == "738" and configID == "INLK" and (DSPW >= 60 or DSPH >= 94 or (DSPW >= 42 and DSPH >= 82)):
        prof = "901A"
    elif stile == "755":
        # 901E NO MATTER WHAT (new meeting stiles sold separately)
        prof = "901E"
    else:
        prof = None

    # 
    if prof:
        partNum = prof + "M197"
    else:
        partNum = None

    return [partNum, prof]

