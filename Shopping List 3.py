# Nick W
# Shopping List designed to assist FFXIV crafting

from unittest import skip
from colorama import Fore,Back,Style

def initializeStructures():
    craftDict = {} # 3.0 dict
    materialDict = {} # 3.0 dict
    return craftDict, materialDict

def parseCraft(s, argMin, argMax):
    l = s.split(".")
    if len(l) > argMax:
        print("invalid input")
    elif len(l) < argMin:
        print("invalid input")
    else:
        craftName = l[0]
        craftCrafter = l[1].upper()
        craftQuantity = l[2] if len(l) == 3 else 1
        craftLevel = "top"
        craftDict[craftName] = (craftCrafter,craftQuantity,craftLevel)
    
def addBankMats():
    print("Add mats from bank or 'done'")
    print("Format: (optional)")
    while True:
        s = input("Name.Quantity.Inv.Bank(.Type(.HQ))\n")
        if s.lower() == "done":
            break
        else:
            parseItem(s, 6, 4)
                
            # old way
            """
            if len(l) == 4:
                oldinv[l[1]] = int(l[2])
                oldbank[l[1]] = int(l[3])
                if l[1] in oldneeded:
                    oldneeded[l[1]] += int(l[0])
                else:
                    oldneeded[l[1]] = int(l[0])
            else:
                print("invalid input")
            """
    # outside the while loop
    addMedCrafts()

def parseItem(s, argMax, argMin):
    l = s.split(".")
    if len(l) > argMax :
        print("invalid input")
    elif len(l) < argMin :
        print("invalid input")
    else:
                # argument has 4, 5, or 6 arguments
        materialName = l[0]
        if materialName in materialDict:
            materialQuantity = int(l[1]) + int(materialDict[materialName][0])
        else:
            materialQuantity = int(l[1])
        if l[2] != " ":
            materialInInventory = int(l[2])
        if l[3] != " ":
            materialInBank = int(l[3])
        if len(l) > 4:
            materialType = l[4].lower()
            if len(l) > 5:
                materialHQ = l[5].lower()
            else:
                materialHQ = ""
        else:
            materialType = ""
            materialHQ = ""
        materialDict[materialName] = (materialQuantity, materialInInventory, materialInBank, materialType, materialHQ)
    
def addMedCrafts():
    print("Add intermediary crafts or 'done'")
    print("Add right to left, top to bottom")
    print("Format:")
    while True:
        s = input("Quantity.Name\n")
        if s.lower() == "done":
            break
        else:
            l = s.split(".")
            if len(l) == 2:
                if l[1] in oldmedCrafts:
                    oldcrafts[l[1]] += int(l[0])
                else:
                    oldmedCrafts.append(l[1])
                    oldcrafts[l[1]] = int(l[0])
            else:
                print("invalid input")
    #outside the while loop
    print("Add top-level crafts or 'done'")
    print("Format:")
    
def printAll():
    print("")
    print("")
    print("Remove from bank:")
    for key,value in materialDict.items():
        materialName = key
        materialQuantity = int(value[0])
        materialInInventory = int(value[1])
        materialInBank = int(value[2])
        materialType = value[3]
        materialHQ = value[4]
        print(f"({materialType}) {materialQuantity} {materialName}: inv: {materialInInventory} bank: {materialInBank} {materialHQ}")
    """
    for i in oldneeded.keys():
        color=Fore.RESET
        if oldneeded[i] > oldinv[i]+oldbank[i]:
            color=Fore.RED
        print(f"{color}{oldneeded[i]} {i} (Inv:{oldinv[i]} Bank:{oldbank[i]}){Style.RESET_ALL}")
    """
    print("")
    print("Craft in order:")
    if len(oldmedCrafts) == 0:
        print("(no intermediate crafts)")
    else:
        for i in oldmedCrafts:
            print(f"{oldcrafts[i]} {i}")
    print("")
    # for i in oldtopCrafts:
    #    print(f"{crafts[i]} {i}")
    for key,value in craftDict.items():
        craftName = key
        craftCrafter = value[0].upper()
        craftQuantity = value[1]
        craftLevel = value[2]
        if craftLevel == "top":
            print(f"{craftCrafter}: {craftQuantity} {craftName}")


    """
    for i in range(len(craftList)):
        craftName = craftList[i][0]
        craftCrafter = craftList[i][1]
        craftQuantity = int(craftList[i][2])
        craftLevel = craftList[i][3]
        if craftLevel.lower() == "top": 
            print(f"{craftCrafter}: {craftQuantity} {craftName}")

    """
 
def askToSave():
    s=input("Save this list?\n")
    if s.lower() == "y":
        with open("shoppinglist.txt","w") as file:
            file.write("bank\n")
            for i in oldneeded.keys():
                file.write("{}.{}.{}.{}\n".format(oldneeded[i],i,oldinv[i],oldbank[i]))
            file.write("oldmedCrafts\n")
            for i in oldmedCrafts:
                file.write("{}.{}\n".format(oldcrafts[i],i))
            file.write("oldtopCrafts\n")
            for i in oldtopCrafts:
                file.write("{}.{}\n".format(oldcrafts[i],i))

def askToLoad():
    s=input("Load previous list?\n")
    if s.lower() == "y":
        with open("shoppinglist.txt","r") as file:
            lines = file.readlines()
            isBank = True
            isTopCraft = False
            for line in lines:
                if line == "bank\n":
                    continue
                elif line == "oldmedCrafts\n":
                    isBank = False
                elif line == "oldtopCrafts\n":
                    isTopCraft = True
                else:
                    line = line[:len(line)-1]
                    l = line.split(".")
                    item = l[1]
                    quant = int(l[0])
                    if isBank:
                        numInInv = int(l[2])
                        numInBank = int(l[3])
                        oldneeded[item] = quant
                        oldinv[item] = numInInv
                        oldbank[item] = numInBank
                    elif isTopCraft:
                        oldtopCrafts.append(item)
                        oldcrafts[item] = quant
                    else:
                        oldmedCrafts.append(item)
                        oldcrafts[item] = quant
        printAll()
        s = input("Add to this list?\n")
        if s.lower() == "y":
            addTopCraft()
    else:
        addTopCraft()
        
# old methods
def addTopCraft():
    print("Add top-level craft or 'done'")
    print("Format:")
    while True:
        s = input("Name.Crafter(.Quantity)\n> ")
        if s.lower() == "done":
            break
        else:
            parseCraft(s, 2, 3)
            addBankMats()
    printAll()
    askToSave()

def initializeOldVariables():
    oldtopCrafts = [] # 2.0 list
    oldmedCrafts = [] # 2.0 list
    oldneeded = {} # 2.0 dict
    oldcrafts = {} # 2.0 dict
    oldinv = {} # 2.0 dict
    oldbank = {} # 2.0 dict
    return oldtopCrafts,oldmedCrafts,oldneeded,oldcrafts,oldinv,oldbank

def addCraftToList(dest, level, num, ele):
    if ele in level:
        dest[ele] += int(num)
    else:
        level.append(ele)
        dest[ele] = int(num)

# program starts here
oldtopCrafts, oldmedCrafts, oldneeded, oldcrafts, oldinv, oldbank = initializeOldVariables()
craftDict, materialDict = initializeStructures()
askToLoad()