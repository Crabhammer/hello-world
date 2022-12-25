# Nick W
# Shopping List designed to assist FFXIV crafting

from unittest import skip
from colorama import Fore,Back,Style

class Material:

    def __init__(self, needed, name, inv, bank, type, HQ):
        self.name = str(name)
        self.needed = int(needed)
        self.inv = int(inv)
        self.bank = int(bank)
        self.type = type
        self.HQ = HQ
        self.forCraft = ""

    def updateName(self, name):
        self.name = name

    def updateNeeded(self, needed):
        self.needed = needed 

    def make(self, tup):
        self.needed = int(tup[0])
        self.name = str(tup[1])
        self.inv = int(tup[2])
        self.bank = int(tup[3])
        self.type = tup[4]
        self.HQ = tup[5]
        return self
    
    def output(self):
        return self.name, self.needed, self.inv, self.bank, self.type, self.HQ, self.forCraft

class Craft:

    def __init__(self, name, job, needed, materials, level, inv=0, invHQ=0):
        self.name = str(name)
        self.job = str(job)
        self.needed = int(needed)
        self.materials = materials
        self.level = int(level)
        self.inv = int(inv)
        self.invHQ = int(invHQ)
        
def initializeStructures():
    craftDict = {} # 3.0 dict
    materialDict = {} # 3.0 dict
    return craftDict, materialDict

# loads 2.0 format
def askToLoad():
    craftDict = {}
    materialDict = {}
    s=input("Load previous list?\n> ")
    if s.lower() == "y":
        with open("shoppinglist.txt","r") as file:
            lines = file.readlines()
            isBank = True
            isCraft = False
            for line in lines:
                if line == "bank\n":
                    continue
                elif line == "midCrafts\n":
                    isBank = False
                    isCraft = True
                else:
                    line = line[:len(line)-1]
                    l = line.split(".")
                    name = str(l[1])
                    needed = int(l[0])
                    if isBank:
                        inv = int(l[2])
                        bank = int(l[3])
                        type = str(l[4])
                        materialDict[name] = Material(needed,name,inv,bank,type,"")
                    elif isCraft:
                        job = str(l[2])
                        inv = int(l[3])
                        invHQ = int(l[4])
                        craftDict[name] = Craft(name,job,needed,None,0,inv,invHQ)

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
        s = input("Needed.Name.Crafter\n> ")
        if s.lower() == "done":
            break
        else:
            parseCraft(s,0)
            addBankMats()
    materialSort()
    printAll()
    askToSave()

def parseCraft(s, level=0):
    l = s.split(".") # Needed.Name.Crafter (top) ||  Quantity.Name.Crafter (med)
    # if type(l[0]) != type(0):
    #     l.insert(0,1)
    if len(l) > 5:
        print("invalid input")
    elif len(l) < 2:
        print("invalid input")
    else:
        craftNeeded = int(l[0])
        craftName = str(l[1])
        craftJob = str(l[2]).upper()
        craftLevel = int(level)
        if len(l) > 3:
            craftLess = int(l[3])
            if len(l) > 4:
                craftLessHQ = int(l[4])
            else:
                craftLessHQ = 0
        else:
            craftLess = 0
            craftLessHQ = 0

        if craftName in craftDict:
            craftNeeded = craftNeeded + int(craftDict[craftName].needed)
        craftDict[craftName] = Craft(craftName,craftJob,craftNeeded,None,craftLevel,craftLess,craftLessHQ)
    
def addBankMats():
    print("Add crafting materials or 'done'")
    print("Format: (optional)")
    while True:
        s = input("Quantity.Name.Inv.Bank(.Type(.HQ))\n> ")
        if s.lower() == "done":
            break
        else:
            needed, name, inv, bank, type, HQ = parseItem(s)
            #needed, name, inv, bank, type, HQ = parseItem(s)
            #if name in materialDict:
            #    print(f"material {name} in materialDict")
            #    print(f"materialNeeded= {needed}")
            #    print(f"materialDict[{name}].needed= {materialDict[name].needed}")
            #
            #    needed = int(needed) + int(materialDict[name].needed)
            #
            #    print(f"needed= {needed}")
            materialDict[name] = Material(needed, name, inv, bank, type, HQ)
                
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
    addMidCrafts()

def parseItem(s):
    l = s.split(".")
    if len(l) > 6 :
        print("invalid input")
    elif len(l) < 4 :
        print("invalid input")
    else:
        # argument has 4, 5, or 6 arguments
        inputNeeded = int(l[0])
        inputName = str(l[1])
        inputInventory = int(l[2])
        inputBank = int(l[3])
        inputType = str(l[4]) if len(l) > 4 else None
        inputHQ = str(l[5]) if len(l) > 5 else None

        if inputName in materialDict:
            print(f"material {inputName} in materialDict")
            print(f"materialNeeded= {inputNeeded}")
            print(f"materialDict[{inputName}].needed= {materialDict[inputName].needed}")
        
            inputNeeded = inputNeeded + materialDict[inputName].needed

            print(f"inputNeeded= {inputNeeded}")

        return inputNeeded, inputName, inputInventory, inputBank, inputType, inputHQ

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

def addMidCrafts():
    print("Add intermediary crafts or 'done'")
    print("Add top to bottom, right to left")
    print("Format:")
    while True:
        s = input("Quantity.Name.Crafter\n")
        if s.lower() == "done":
            break
        else:
            parseCraft(s, 1)

            # old dict method
            """
            l = s.split(".")             
                if len(l) == 2:
                if l[1] in oldmedCrafts:
                    oldcrafts[l[1]] += int(l[0])
                else:
                    oldmedCrafts.append(l[1])
                    oldcrafts[l[1]] = int(l[0])
            else:
                print("invalid input") 
            """
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
        materialName = str(key)
        materialNeeded = int(value.needed)
        materialInInventory = int(value.inv)
        materialInBank = int(value.bank)
        materialType = value.type
        if value.HQ == None:
            materialHQ = ""
        else:
            materialHQ = value.HQ
        color = Fore.RESET
        if materialNeeded > materialInInventory + materialInBank:
            color = Fore.RED
        print(f"{color}({materialType}) {materialNeeded} {materialName}: inv: {materialInInventory} bank: {materialInBank} {materialHQ} ){Style.RESET_ALL}")
    """
    for i in oldneeded.keys():
        color=Fore.RESET
        if oldneeded[i] > oldinv[i]+oldbank[i]:
            color=Fore.RED
        print(f"{color}{oldneeded[i]} {i} (Inv:{oldinv[i]} Bank:{oldbank[i]}){Style.RESET_ALL}")
    """
    print("")
    print("Craft in order:")
    """     
        if len(oldmedCrafts) == 0:
        print("(no intermediate crafts)")
    else:
        for i in oldmedCrafts:
            print(f"{oldcrafts[i]} {i}")
    print("")
    for i in oldtopCrafts:
        print(f"{crafts[i]} {i}")
    """
    craftPrint(1)
    print("")
    craftPrint(0)
    """
    for i in range(len(craftList)):
        craftName = craftList[i][0]
        craftCrafter = craftList[i][1]
        craftQuantity = int(craftList[i][2])
        craftLevel = craftList[i][3]
        if craftLevel.lower() == "top": 
            print(f"{craftCrafter}: {craftQuantity} {craftName}")

    """

def craftPrint(level):
    for key,value in craftDict.items():
        craftName = str(key)
        craftJob = str(value.job)
        craftNeeded = int(value.needed)
        craftLevel = int(value.level)
        craftLess = int(value.inv)
        craftLessHQ = int(value.invHQ)
        if craftLevel == level:
            print(f"{craftJob}: {craftNeeded} {craftName} - (inv: {craftLess}, HQ: {craftLessHQ}")
 
def askToSave():
    s=input("Save this list?\n")
    if s.lower() == "y":
        with open("shoppinglist.txt","w") as file:
            file.write("bank\n")
            for key,value in materialDict.items():
                file.write(f"{value.needed}.{key}.{value.inv}.{value.bank}.{value.type}\n")
            file.write("midCrafts\n")
            for i in range(1,-1,-1):
                for key,value in craftDict.items():
                    if value.level == i:
                        #file.write("{}.{}.{}.{}\n".format(value.needed, key, value.job, value.level))
                        file.write(f"{value.needed}.{key}.{value.job}.{value.level}.{value.inv}.{value.invHQ}\n")
        

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

