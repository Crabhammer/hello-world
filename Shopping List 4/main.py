import SL3core as sl

# program starts here
oldtopCrafts, oldmedCrafts, oldneeded, oldcrafts, oldinv, oldbank = sl.initializeOldVariables()
craftDict, materialDict = sl.initializeStructures()
# sl.askToLoad()
sl.materialLookup("Stiperstone")