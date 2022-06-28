######## QUERY CONSTANTS ########
producingLoc = {
    "CM" : 262920,
    "SF" : 269920,
    "WIN" : 294920,
    "SGD" : 316920,
    "FD" : 319920,
    "PB" : 343920,
    "GD" : 346920,
}

producingLocID = {
    "CM" : 262920,
    "SF" : 269920,
    "WIN" : 37,
    "SGD" : 30,
    "FD" : 39,
    "PB" : 31,
    "GD" : 346920,
}

filePrefix = {
    "CM" : "CMMET_",
    "SF" : "SFMET_",
    "WIN" : "WINMET_",
    "SGD" : "SGDMET_",
    "FD" : "FDMET_",
    "PB" : "PIVBIMET_",
    "GD" : "GDMET_",
}


######## BOILER PLATE ########
### trackingNumber = tracking #
### charCol2 = order #
### charCol3 = line #
### charCol5 = batch #
### charCol6 = slot #
### charCol13 - color - AJE Family
### charCol17 = AO FAMILY # so is charCol8 for SGD for some reason...
######## BOILER PLATE ########

# DEFINING FAMILY -- type: String

# LENGTHS AND DIMENSIONS -- type: Decimal
# numCol141 = BTRD bottom rail dimension 
# numCol142 = TPRD top rail dimension
# numCol203 = SRLT TOP rail length
# numCol206 = STLB BOTTOM rail length

# Can use numCol108 for head/sill length
# But I won't >:)

#------- NOT IN USE -------#
# numCol182 =  GBLH
# numCol172 = DSPH = stile length
# numCol20(4/5) = stile length
### numCol173 = DSPW = rail length + stile dims?

#  COLUMNS TAKEN FROM TABLE FOR GIVEN PRODUCING LOCATION
#                   0           1         2          3         4         5         6          7          8          9         10         11          12         13        14
tableCols = {
    "CM" : "*",
    "SF" : "*",
    "WIN" : "*",
    "SGD" : """unit.trackingNumber, 
                unit.orderNumber,
                unit.orderLineNumber,
                unit.batchNumber,
                unit.slot,
                ao.familyCode,
                aji.familyCode as interiorColor,
                ar.familyCode as handing,
                conf.familyCode as configuration,
                ld.sashPanelHeight,
                ld.screenFrameHorzLength,
                FLOOR(ld.trackCount),
                ld.sashPanelWidth,
                CASE WHEN conf.familyCode = 'COP5' THEN 'STAN'
                    WHEN conf.familyCode = 'COP3' THEN 'STAN'
                    WHEN ao.familyCode = 'AKKC' THEN 'STAN'
                    ELSE hp.familyCode end as performanceOption,
                scas.familyCode as screenAstragal""",
    "FD" : "*",
    "PB" : """unit.trackingNumber,
                unit.orderNumber,
                unit.orderLineNumber,
                unit.batchNumber,
                unit.slot,
                ao.familyCode,
                aji.familyCode,
                ld.btmRailDim,
                ld.topRailDim,
                ld.sashBottomRailLength,
                ld.frameLeftJambLength,
		        ld.sashPanelWidth""",
    "GD" : "*",
}

# old PB columns, I'm pretty sure they are all there. Still need sweep adapter length tho...
# NEED TO CHECK ORDER OF IT THO
# "PB" : "trackingNumber, charCol2, charCol3, charCol5, charCol6, charCol17, charCol13, numCol142, numCol141, numCol203",

    # "SGD" : """unit.trackingNumber, 
    #             unit.orderNumber,
    #             unit.orderLineNumber,
    #             unit.batchNumber,
    #             unit.slot,
    #             ao.familyCode,
    #             aji.familyCode as interiorColor,
    #             ar.familyCode as handing,
    #             conf.familyCode as configuration,
    #             ld.sashPanelHeight,
    #             ld.screenFrameHorzLength,
    #             FLOOR(ld.trackCount),
    #             ld.sashPanelWidth,
    #             CASE WHEN hp.shortDesc = 'STANDARD' THEN 'STAN' 
    #                 WHEN  hp.shortDesc = 'HEAVY DUTY' THEN 'HPHD' 
    #                 END AS performanceOption,
    #             scas.familyCode as screenAstragal""",







SQLTables = {
    "CM" : "*",
    "SF" : "*",
    "WIN" : "*",
    "SGD" : """BatchFileUnitSIW AS unit WITH (NOLOCK)
                JOIN SIWLabelData AS ld WITH (NOLOCK)
                ON ld.icimID = unit.icimID
                LEFT OUTER JOIN icimAJI AS aji WITH (NOLOCK)
                ON aji.id = unit.interiorColor
                LEFT OUTER JOIN icimAR AS ar WITH (NOLOCK)
                ON ar.id = unit.handing
                LEFT OUTER JOIN icimCONF AS conf WITH (NOLOCK)
                ON conf.id = ld.[configuration]
                LEFT OUTER JOIN icimSCAS AS scas WITH (NOLOCK)
                ON scas.id = ld.screenAstragal
                LEFT OUTER JOIN icimHP AS hp WITH (NOLOCK)
                ON hp.id = ld.performanceOption
                LEFT OUTER JOIN icimAO AS ao WITH (NOLOCK)
                ON ao.id = unit.unitTypeDoors""",
    "FD" : "*",
    "PB" : """BatchFileUnitSIW AS unit WITH (NOLOCK)
                JOIN SIWLabelData AS ld WITH (NOLOCK)
                ON ld.icimID = unit.icimID
                LEFT OUTER JOIN icimAJI AS aji WITH (NOLOCK)
                ON aji.id = unit.interiorColor
                LEFT OUTER JOIN icimAO AS ao WITH (NOLOCK)
                ON ao.id = unit.unitTypeDoors""",
    "GD" : "*",
}


###### SGD CONSTANTS ######
# charCol16 = AR - handing
# charCol62 = CONF - configuration
# numCol187 = DSPH - stile length
# numCol106 = ??? - Screen rail length
# numCol103 = TRCO - Track count
# numCol186 = DSPW - used to calculate rail length
# charCol72 = HP - STAN/HPHD
# charCol69 = SCAS - T/F Screen Astragal
acceptedAKKA = ["KM", "KMHI"]
acceptedMeet = ["OLD", "NEW"]

pocketDoorConfigs = [
    "CONZ", "COP1", "COP2", "COP3", "COP4", "COP5",
    "COP6", "COP7", "COP8", "COP9", "COPA", "COPB"
]
leftPockets = ["CONZ", "COP2", "COP4", "COP6"]
rightPockets =["COP1", "COP3", "COP5", "COP7"]
doublePockets = ["COP8","COP9","COPA","COPB"]
headerProf = {
    "720": "719",
    "732": "702",
    "734": "727",
    "735": "723",
}
reinforcedStiles = ["706","708","718","738","755"]

###### PV/BF CONSTANTS ######
PBRails = {
    "4" : "805",
    "8" : "814",
}


###### COMMON ORDER CONSTANTS ######
colors = {
    "AJSC" : "A",
    "AJSB" : "B",
    "AJSI" : "BLKY",
    "AJSK" : "BZKY",
    "AJSF" : "CH",
    "AJSG" : "CI",
    "AJSM" : "CP",
    "AJSF" : "H",
    "AJSL" : "M",
    "AJSE" : "OA",
    "AJSA" : "W",
    "AJSJ" : "WHKY",
    "AJSH" : "WN",
}

colorCodes = {
        "AJSC": "CL ANO IMP",
        "AJSB": "BZ IMP",
        "AJSI": "BK KYNAR I",
        "AJSK": "BZ KYNAR I",
        "AJSF": "HNY CHRY I",
        "AJSG": "CIN IMP",
        "AJSM": "CC IMP",
        "AJSF": "HZLNT IMP",
        "AJSL": "MILL",
        "AJSE": "OAK IMP",
        "AJSA": "WH IMP",
        "AJSJ": "WH KYNAR I",
        "AJSH": "WALNUT IMP"
    }
