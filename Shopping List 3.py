from colorama import Fore,Back,Style

topCrafts = []
medCrafts = []
needed = {}
crafts = {}
inv = {}
bank = {}

def addTopCraft():
    print("Add top-level crafts or 'done'")
    print("Format:")
    while True:
        s = input("Quantity.Name\n")
        if s.lower() == "done":
            break
        else:
            l = s.split(".")
            if len(l) == 2:
                if l[1] in topCrafts:
                    crafts[l[1]] += int(l[0])
                else:
                    topCrafts.append(l[1])
                    crafts[l[1]] = int(l[0])
                addBankMats()
            else:
                topCrafts.append(l)
                addToList(crafts,1,l)
    # outside the while loop
    printAll()
    askToSave()
    
def addBankMats():
    print("Add mats from bank or 'done'")
    print("Format: (optional)")
    while True:
        s = input("Quantity.Name.Inv.Bank\n")
        if s.lower() == "done":
            break
        else:
            l = s.split(".")
            if len(l) == 4:
                inv[l[1]] = int(l[2])
                bank[l[1]] = int(l[3])
                if l[1] in needed:
                    needed[l[1]] += int(l[0])
                else:
                    needed[l[1]] = int(l[0])
                    
            else:
                print("invalid input")
    # outside the while loop
    addMedCrafts()
    
    
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
                if l[1] in medCrafts:
                    crafts[l[1]] += int(l[0])
                else:
                    medCrafts.append(l[1])
                    crafts[l[1]] = int(l[0])
            else:
                print("invalid input")
    #outside the while loop
    print("Add top-level crafts or 'done'")
    print("Format:")
    
def printAll():
    print("")
    print("")
    print("Remove from bank:")
    for i in needed.keys():
        color=Fore.RESET
        if needed[i] > inv[i]+bank[i]:
            color=Fore.RED
        print(f"{color}{needed[i]} {i} (Inv:{inv[i]} Bank:{bank[i]}){Style.RESET_ALL}")
    print("")
    print("Craft in order:")
    for i in medCrafts:
        print(f"{crafts[i]} {i}")
    print("")
    for i in topCrafts:
        print(f"{crafts[i]} {i}")
 
def askToSave():
    s=input("Save this list?\n")
    if s.lower() == "y":
        with open("shoppinglist.txt","w") as file:
            file.write("bank\n")
            for i in needed.keys():
                file.write("{}.{}.{}.{}\n".format(needed[i],i,inv[i],bank[i]))
            file.write("medCrafts\n")
            for i in medCrafts:
                file.write("{}.{}\n".format(crafts[i],i))
            file.write("topCrafts\n")
            for i in topCrafts:
                file.write("{}.{}\n".format(crafts[i],i))

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
                elif line == "medCrafts\n":
                    isBank = False
                elif line == "topCrafts\n":
                    isTopCraft = True
                else:
                    line = line[:len(line)-1]
                    l = line.split(".")
                    item = l[1]
                    quant = int(l[0])
                    if isBank:
                        numInInv = int(l[2])
                        numInBank = int(l[3])
                        needed[item] = quant
                        inv[item] = numInInv
                        bank[item] = numInBank
                    elif isTopCraft:
                        topCrafts.append(item)
                        crafts[item] = quant
                    else:
                        medCrafts.append(item)
                        crafts[item] = quant
        printAll()
        s = input("Add to this list?\n")
        if s.lower() == "y":
            addTopCraft()
    else:
        addTopCraft()
        
def addToList(dest, num, ele):
    if ele in dest:
        dest[ele] += int(num)
    else:
        dest[ele] = int(num)

# program starts here
askToLoad()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
