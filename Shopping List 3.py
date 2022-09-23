# Nick W
# Shopping List designed to assist FFXIV crafting

from unittest import skip
from colorama import Fore,Back,Style

class Material:

    def __init__(self, name, needed, inv, bank, type, HQ):
        self.name = name
        self.needed = needed
        self.inv = inv
        self.bank = bank
        self.type = type
        self.HQ = HQ
        self.forCraft = ""

    def update(self, name, needed, inv, bank, type, HQ, forCraft):
        self.name = name
        self.needed = needed
        self.inv = inv
        self.bank = bank
        self.type = type
        self.HQ = HQ
        self.forCraft = forCraft

    def updateName(self, name):
        self.name = name

    def updateNeeded(self, needed):
        self.needed = needed 
    
    def output(self):
        return self.name, self.needed, self.inv, self.bank, self.type, self.HQ, self.forCraft

class Craft:

    def __init__(self, job, quantity, materials):
        self.job = job
        self.quantity = quantity
        self.materials = materials
        
    

def initializeStructures():
    craftDict = {} # 3.0 dict
    materialDict = {} # 3.0 dict
    return craftDict, materialDict

# loads 2.0 format
def askToLoad():
    s=input("Load previous list?\n> ")
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
        s = input("Add to this list?\n> ")
        if s.lower() == "y":
            addTopCraft()
    else:
        craftDict.clear()
        materialDict.clear()
        addTopCraft()

def addTopCraft():
    print("Add top-level craft or 'done'")
    print("Format:")
    while True:
        s = input("Name.Crafter(.Quantity)\n> ")
        if s.lower() == "done":
            break
        else:
            parseCraft(s)
            addBankMats()
    materialSort()
    printAll()
    askToSave()

def parseCraft(s):
    l = s.split(".")
    if len(l) > 3:
        print("invalid input")
    elif len(l) < 2:
        print("invalid input")
    else:
        craftName = l[0]
        craftCrafter = l[1].upper()
        craftQuantity = l[2] if len(l) == 3 else 1
        craftLevel = "top"
        craftDict[craftName] = (craftCrafter,craftQuantity,craftLevel)
    
def addBankMats():
    print("Add crafting materials or 'done'")
    print("Format: (optional)")
    while True:
        s = input("Name.Quantity.Inv.Bank(.Type(.HQ))\n> ")
        if s.lower() == "done":
            break
        else:
            inputName, inputQuantity, inputInventory, inputBank, inputType, inputHQ = parseItem(s)
            materialDict[inputName] = Material(inputName, inputQuantity, inputInventory, inputBank, inputType, inputHQ)
            print(materialDict[inputName].needed)

                
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

def parseItem(s):
    l = s.split(".")
    if len(l) > 6 :
        print("invalid input")
    elif len(l) < 4 :
        print("invalid input")
    else:
        # argument has 4, 5, or 6 arguments
        inputName = l[0]
        inputQuantity = l[1]
        inputInventory = l[2]
        inputBank = l[3]
        inputType = l[4] if len(l) > 4 else None
        inputHQ = l[5] if len(l) > 5 else None
        return inputName, inputQuantity, inputInventory, inputBank, inputType, inputHQ

        # old assignment to dictionary
        """
        materialName = l[0]
        if materialName in materialDict:
            materialQuantity = int(l[1]) + int(materialDict[materialName][0])
            materialInDict = True
        else:
            materialQuantity = int(l[1])
        if materialInDict != False:
            materialInInventory = int(l[2])
            materialInBank = int(l[3])
        if len(l) > 4:
            materialType = l[4].lower()
            if len(l) > 5:
                materialHQ = l[5].upper()
            else:
                materialHQ = materialDict[materialName][5]
        else:
            materialType = ""
            materialHQ = ""
        materialDict[materialName] = (materialQuantity, materialInInventory, materialInBank, materialType, materialHQ)
        """

def addToDict(s, dict):
    if s in dict:
        skip


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
    
def materialSort():
    skip

def printAll():
    print("")
    print("")
    print("Remove from bank:")
    for key,value in materialDict.items():
        materialName = key
        materialQuantity = value.needed
        materialInInventory = value.inv
        materialInBank = value.bank
        materialType = value.type
        materialHQ = value.HQ
        color = Fore.RESET
        if materialQuantity > materialInInventory + materialInBank:
            color = Fore.RED
        print(f"{color}({materialType}) {materialQuantity} {materialName}: inv: {materialInInventory} bank: {materialInBank} {materialHQ}{Style.RESET_ALL}")
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
        

# old methods
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