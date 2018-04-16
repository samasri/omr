# This python script creates SQL files containing queries that create the database. The script does not support more than one argument. 
# Passing no arguments for the script creates the SQL files in the same directory as the python file. 
# Passing 'd' to the script will run it in debug mode (no output generated). 
# Passing anything else to the script will be considered as the path to the directory for the output to be placed in
import csv
import sys
import os
import warnings
import random

# ------------------------------------------Define Tables------------------------------------------
class FunctionTable:
	def __init__(self, functionNameLength, signatureLength):
		self.tableName = 'Function'
		self.columns = ['FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
		self.primaryKey = 'Signature, ClassID'
		self.foreignKeys = {}
		self.foreignKeys['ClassID'] = [ClassTable(-1,-1), 'ID']
		self.foreignKeys['FileID'] = [FileTable(-1), 'ID']
		# Columns
		self.FunctionName = 'VARCHAR(' + str(functionNameLength) + ')'
		self.Signature = 'VARCHAR(' + str(signatureLength) + ')'
		self.ClassID = 'INT'
		self.IsVirtual = 'INT'
		self.IsImplicit = 'INT'
		self.FileID = 'INT'

class FileTable:
	def __init__(self, maxLocationLength):
		self.tableName = 'File'
		self.columns = ['ID', 'Location']
		self.primaryKey = 'ID'
		# Columns
		self.ID = 'INT'
		self.Location = 'VARCHAR(' + str(maxLocationLength) + ')'

class OverrideTable:
	def __init__(self, maxSigLen):
		self.tableName = 'Override'
		self.columns = ['FirstClassID', 'FunctionSig', 'BaseClassID', 'OverridingClassID']
		self.primaryKey = 'FirstClassID, FunctionSig, BaseClassID, OverridingClassID'
		self.foreignKeys = {}
		self.foreignKeys['FirstClassID, FunctionSig'] = [FunctionTable(-1,-1), 'ClassID, Signature']
		self.foreignKeys['BaseClassID'] = [FunctionTable(-1,-1), 'ClassID']
		self.foreignKeys['OverridingClassID'] = [ClassTable(-1,-1), 'ID']
		# Columns
		self.FirstClassID = 'INT'
		self.FunctionSig = 'VARCHAR(' + str(maxSigLen) + ')'
		self.BaseClassID = 'INT'
		self.OverridingClassID = 'INT'

class PolymorphismTable:
	def __init__(self):
		self.tableName = 'Polymorphism'
		self.columns = ['HierarchyID', 'ChildClassID', 'ParentClassID']
		self.primaryKey = 'HierarchyID, ChildClassID, ParentClassID'
		self.foreignKeys = {}
		self.foreignKeys['HierarchyID'] = [HierarchiesBase(), 'HierarchyID']
		self.foreignKeys['ChildClassID'] = [ClassTable(-1,-1), 'ID']
		self.foreignKeys['ParentClassID'] = [ClassTable(-1,-1), 'ID']
		# Columns
		self.HierarchyID = 'INT'
		self.ChildClassID = 'INT'
		self.ParentClassID = 'INT'

class HierarchiesBase:
	def __init__(self):
		self.tableName = 'HierarchiesBase'
		self.foreignKeys = {}
		self.foreignKeys['BaseClassID'] = [ClassTable(-1,-1), 'ID']
		self.primaryKey = 'HierarchyID'
		self.columns = ['HierarchyID', 'BaseClassID']
		self.HierarchyID = 'INT'
		self.BaseClassID = 'INT'

class ClassTable:
	def __init__(self, maxNamespaceLength, maxClassNameLength):
		self.tableName = 'Class'
		self.columns = ['ID', 'Namespace', 'ClassName', 'IsExtensible']
		self.primaryKey = 'ID'
		self.unique = 'Namespace, ClassName'
		# Columns
		self.ID = 'INT'
		self.Namespace = 'VARCHAR(' + str(maxNamespaceLength) + ')'
		self.ClassName = 'VARCHAR(' + str(maxClassNameLength) + ')'
		self.IsExtensible = 'INT'
	
# -------------------------------------End of Defining Tables--------------------------------------

# ------------------------------------------Configurations-----------------------------------------

# Get path from OMRStatistics directory to the python script
path = sys.argv[0]
nameIndex = path.index('getDatabaseSQL.py')
path = path[:nameIndex]
fileWritePath = path + sys.argv[1] + '/' if len(sys.argv) == 2 and sys.argv[1] != 'd' else path + './'

print fileWritePath

# Get the absolute path to the OMR directory
pathToOMR = os.path.dirname(os.path.realpath(__file__)) + sys.argv[0]
pathToOMR = pathToOMR[:pathToOMR.index('/omr/tools/compiler/') + 5] #get path for omr directory

# Setting debug
if len(sys.argv) == 2 and sys.argv[1] == 'd': debug = 1
else: debug = 0

# --------------------------------------End of Configurations--------------------------------------

# ---------------------------------------Defining Functions----------------------------------------
def createTable(table):
	# Create file
	file = open(fileWritePath + table.tableName + '.sql', 'w')
	
	# Get MySQL instruction
	result = ''
	tableColumns = table.__dict__
	result += 'CREATE TABLE ' + table.tableName + ' (\n'
	for column in table.columns:
		result += '\t' + column + ' ' + tableColumns[column] + ',\n'
	# Adding Primary key
	result += '\tPRIMARY KEY(' + table.primaryKey + '),\n'
	# Adding Foreign keys
	if 'foreignKeys' in tableColumns:
		for fk in table.foreignKeys: 
			result += '\tFOREIGN KEY(' + fk + ') '
			fkTable = table.foreignKeys[fk][0]
			result += 'REFERENCES ' + fkTable.tableName + '(' + table.foreignKeys[fk][1]+'),\n'
	# Adding UNIQUE constraints
	if 'unique' in tableColumns:
		result += '\tUNIQUE (' + (table.unique) + '),\n'
	# Final Edits
	result = result[:-2] + '\n);\n' # Remove last coma
	result += 'ALTER TABLE ' + table.tableName + ' CONVERT TO CHARACTER SET latin1 COLLATE latin1_general_cs;\n' # Make case-sensitive
	
	# Write instruction on file and return file
	file.write(result)
	return file

def getOMRLongestPath(pathToOMR):
	maxPathLength = -1
	for root, subdirs, files in os.walk(pathToOMR):
		maxFileLength = -1
		for currentFile in files:
			if maxFileLength < len(str(currentFile)): maxFileLength = len(str(currentFile))
		pathLength = len(str(root)) + maxFileLength + 1
		if maxPathLength < pathLength: maxPathLength = pathLength
	return maxPathLength

def insertTo(table, vector):
	result = ''
	result += 'INSERT INTO ' + table + ' VALUES('
	for value in vector: 
		result += "'" + str(value) + "',"
	result = result[:len(result)-1]
	result += ');\n'
	return result

def getSignature(qualifiedName):
	parenIndex = qualifiedName.find('(')
	inputTrimmed = qualifiedName[:parenIndex]
	lastColonIndex = inputTrimmed.rfind('::')
	signature = qualifiedName[lastColonIndex + 2:]
	return signature
# -----------------------------------End of Defining Functions-------------------------------------

allFunctions = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allClasses = csv.reader(open(path + 'allClasses','r'), delimiter=";")
overrides = csv.reader(open(path + '../visualization/Overrides/overrides','r'), delimiter=";")
hierarchies = csv.reader(open(path + '../visualization/Hierarchy/hierarchy','r'), delimiter=";")
functionLocations = csv.reader(open(path + 'functionLocation','r'), delimiter=";")
#Can iterate only once on one variable, need to iterate through these file twice
allFunctions2 = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allClasses2 = csv.reader(open(path + 'allClasses','r'), delimiter=";")


maxFunctionNameLength = -1
maxSignatureLength = -1
for row in allFunctions:
	if 'Arch:' in row[0]: continue
	if maxFunctionNameLength < len(row[0]): maxFunctionNameLength = len(row[0])
	if maxSignatureLength < len(row[1]): maxSignatureLength = len(row[1])

maxNamespaceLength = -1
maxClassNameLength = -1
for row in allClasses2:
	if maxNamespaceLength < len(row[0]) : maxNamespaceLength = len(row[0])
	if maxClassNameLength < len(row[1]) : maxClassNameLength = len(row[1])
	
# Create and use database
if not debug: 
	initFile = open(fileWritePath + 'init.sql', 'w')
	initFile.write('CREATE DATABASE IF NOT EXISTS omrstatisticsdb;')
	initFile.write('USE omrstatisticsdb;')
# Create tables
functions = FunctionTable(maxFunctionNameLength, maxSignatureLength)
files = FileTable(getOMRLongestPath(pathToOMR))
overridesTable = OverrideTable(maxSignatureLength)
polymorphism = PolymorphismTable()
hierarchiesBase = HierarchiesBase()
classes = ClassTable(maxNamespaceLength, maxClassNameLength)

# Drop tables if they already existed
if not debug:
	initFile.write('DROP TABLE IF EXISTS Polymorphism;')
	initFile.write('DROP TABLE IF EXISTS HierarchiesBase;')
	initFile.write('DROP TABLE IF EXISTS Override;')
	initFile.write('DROP TABLE IF EXISTS Function;')
	initFile.write('DROP TABLE IF EXISTS File;')
	initFile.write('DROP TABLE IF EXISTS Class;')

# Global data structures
classToIDMap = {}
fileToIDMap = {}
functionToFileIDMap = {}
ignoredFunctionSignatures = []

# Fill Files table
id = 0
if not debug: FileFile = createTable(files)
for root, subdirs, files in os.walk(pathToOMR):
	for currentFile in files:
		id += 1
		filePath = root + '/' + currentFile
		filePath = filePath.replace('//', '/')
		filePath = filePath[len(pathToOMR) - 4:] # Get relative path
		if not debug: FileFile.write(insertTo('File', [id, filePath]))
		fileToIDMap[filePath] = id

		
# Fill Class Table
if not debug: ClassFile = createTable(classes)
id = 0
for row in allClasses:
	#['ID', 'Namespace', 'ClassName', 'IsExtensible']
	if id == 0:
		id += 1
		continue
	id += 1
	isExtensible = row[2]
	namespace = row[0]
	className = row[1]
	qualifiedName = namespace + '::' + className if namespace != '' else className;
	classToIDMap[qualifiedName] =  id #Fill classToIDMap from allClasses CSV File
	if not debug: ClassFile.write(insertTo('Class', [id, namespace, className, isExtensible]))

# Link functions to their file ID
id = 0
for row in functionLocations:
	functionQualifiedName = row[0]
	functionLocation = row[1]
	
	#Ignore cases where declaration is outside the OMR directory
	if functionLocation[:9] != "../../../":
		signature = getSignature(functionQualifiedName)
		ignoredFunctionSignatures.append(signature)
		continue
	#Get relative source location path
	functionLocation = functionLocation.replace("../../../../", pathToOMR);
	functionLocation = functionLocation.replace("//", "/");
	functionLocation = functionLocation[len(pathToOMR)-4:]
	
	colonIndex = functionLocation.find(':')
	functionLocation = functionLocation[:colonIndex]
	fileID = fileToIDMap[functionLocation]
	functionToFileIDMap[functionQualifiedName] = fileID

# Fill Functions table
if not debug: FunctionFile = createTable(functions)
id = 0
f2r = {} # Function --> row
dupKeys = set() # Functions in visitedFunctions that have more than one value
for row in allFunctions2:
	if 'Arch:' in row[0]: continue
	#['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
	if id == 0:
		id += 1
		continue
	classQualifiedName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	functionQualifiedName = classQualifiedName + '::' + row[1]
	
	# Record duplicates and dont add them to the database
	if functionQualifiedName not in f2r:
		f2r[functionQualifiedName] = []
	else:
		dupKeys.add(functionQualifiedName)
		id += 1
		continue
	
	f2r[functionQualifiedName].append(row)
	
	if row[1] in ignoredFunctionSignatures: continue #Ignore signatures declared in a non-OMR file
	fileID = functionToFileIDMap[functionQualifiedName]
	
	classID = classToIDMap[classQualifiedName]
	
	if not debug:
		FunctionFile.write(insertTo('Function', [row[0], row[1], classID, row[6], row[5], fileID]))
	id += 1

# Report to the user about the ignored functions
warning = "In allFunctions output, the following lines were ignored due to having previous contradicting records:\n"
printWarning = 0
for k in dupKeys:
	iSig = f2r[k][0]
	for sig in f2r[k]:
		if sig[6] != iSig[6]:
			warning += str(sig) + "\n"
			printWarning = 1
if printWarning: warnings.warn(warning)

# Fill Override table
if not debug: OverrideFile = createTable(overridesTable)
id = 0
firstClassMap = {}
firstClassID = -1
for row in overrides:
	# ['FirstClassID', 'FunctionSignature', 'FunctionClassID', 'BaseClassID', 'OverridingClassID']
	if id == 0: 
		id += 1
		continue
	id += 1
	
	# Reconstruct qualified names of classes & get IDs
	qualifiedBaseName = row[0] + '::' + row[1] if row[0] != '' else row[1]
	qualifiedOverridingName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	baseClassID = classToIDMap[qualifiedBaseName]
	overridingClassID = classToIDMap[qualifiedOverridingName]
	
	sig = row[2]
	
	# If first line, store info in variables and move on
	if id == 1:
		continue
	
	# Ignore functions outside omr
	funcQualifiedName = qualifiedBaseName + '::' + sig
	if sig in ignoredFunctionSignatures: continue	
	
	# Get the correct FirstClassID and signature
	baseClassQualSig = str(baseClassID) + "::" + sig
	overridingClassQualSig = str(overridingClassID) + "::" + sig
	if baseClassQualSig in firstClassMap:
		firstClassMap[overridingClassQualSig] = firstClassMap[baseClassQualSig]
	else:
		firstClassMap[overridingClassQualSig] = baseClassID
	
	firstClassID = firstClassMap[overridingClassQualSig]
	
	if not debug: OverrideFile.write(insertTo('Override', [firstClassID, sig, baseClassID, overridingClassID]))

# Fill Polymorphism and HierarchiesBase tables
if not debug: HierarchiesBaseFile = createTable(hierarchiesBase)
if not debug: PolymorphismFile = createTable(polymorphism)
hierarchyID = 0
duplicateEntries = set()
for row in hierarchies:
	# ['HierarchyID', 'ChildClassID', 'ParentClassID']
	if hierarchyID == 0:
		hierarchyID += 1
		continue
	hierarchy = row[1]
	previousClassID = ''
	for clas in hierarchy.split(' --> '):
		if previousClassID == '': # This is the first class in this hierarchy
			previousClassID = classToIDMap[clas]
			# Record the base class of this hierarchy in the HierarchiesBase table
			baseClass = clas
			if not debug: HierarchiesBaseFile.write(insertTo('HierarchiesBase', [hierarchyID, previousClassID]))
			
			continue
		currentClassID = classToIDMap[clas]
		
		# Duplicate entries will generate in cases of 2 hierarchies that have different bases but merge at some point (so they would have the same top), we remove them here
		key = str(hierarchyID) + ':' + str(previousClassID) + ':' + str(currentClassID)
		if key not in duplicateEntries:
			duplicateEntries.add(key)
			if not debug: PolymorphismFile.write(insertTo('Polymorphism', [hierarchyID, previousClassID, currentClassID]))
		else: # Based on my testing, no case passed here
			pass
		
		previousClassID = currentClassID
		previousClas = clas
	hierarchyID += 1