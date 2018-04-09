import csv
import sys
import os

# ------------------------------------------Define Tables------------------------------------------
class functionTable:
	def __init__(self, functionNameLength, signatureLength):
		self.tableName = 'Function'
		self.primaryKey = 'ID'
		self.columns = ['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
		self.ID = 'INT';
		self.FunctionName = 'VARCHAR(' + str(functionNameLength) + ')'
		self.Signature = 'VARCHAR(' + str(signatureLength) + ')'
		self.ClassID = 'INT'
		self.IsVirtual = 'INT'
		self.IsImplicit = 'INT'
		self.FileID = 'INT'

class FileTable:
	def __init__(self, maxLocationLength):
		self.tableName = 'File'
		self.primaryKey = 'ID'
		self.columns = ['ID', 'Location']
		self.ID = 'INT'
		self.Location = 'VARCHAR(' + str(maxLocationLength) + ')'

class OverloadTable:
	def __init__(self):
		self.tableName = 'Overload'
		self.primaryKey = 'FunctionID'
		self.columns = ['FunctionID', 'IsFirstOccurrence']
		self.FunctionID = 'INT'
		self.IsFirstOccurrence = 'INT'

class OverrideTable:
	def __init__(self):
		self.tableName = 'Override'
		self.primaryKey = 'FunctionID, BaseClassID, OverridingClassID'
		self.columns = ['FunctionID', 'BaseClassID', 'OverridingClassID']
		self.FunctionID = 'INT'
		self.BaseClassID = 'INT'
		self.OverridingClassID = 'INT'

class PolymorphismTable:
	def __init__(self):
		self.tableName = 'Polymorphism'
		self.primaryKey = 'HierarchyID, ChildClassID, ParentClassID'
		self.columns = ['HierarchyID', 'ChildClassID', 'ParentClassID']
		self.HierarchyID = 'INT'
		self.ChildClassID = 'INT'
		self.ParentClassID = 'INT'

class HierarchiesBase:
	def __init__(self):
		self.tableName = 'HierarchiesBase'
		self.primaryKey = 'HierarchyID'
		self.columns = ['HierarchyID', 'BaseClassID']
		self.HierarchyID = 'INT'
		self.BaseClassID = 'INT'

class ClassTable:
	def __init__(self, maxNamespaceLength, maxClassNameLength):
		self.tableName = 'Class'
		self.primaryKey = 'ID'
		self.columns = ['ID', 'Namespace', 'ClassName', 'IsExtensible']
		self.ID = 'INT'
		self.Namespace = 'VARCHAR(' + str(maxNamespaceLength) + ')'
		self.ClassName = 'VARCHAR(' + str(maxClassNameLength) + ')'
		self.IsExtensible = 'INT'
	
# -------------------------------------End of Defining Tables--------------------------------------

def createTable(table):
	result = ''
	tableColumns = table.__dict__
	result += 'CREATE TABLE ' + table.tableName + ' (\n'
	for column in table.columns:
		result += '\t' + column + ' ' + tableColumns[column] + ',\n'
	result += '\tPRIMARY KEY(' + table.primaryKey + ')\n'
	result +=  ');'
	return result

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
	result += ');'
	return result

def getSignature(qualifiedName):
	parenIndex = qualifiedName.find('(')
	inputTrimmed = qualifiedName[:parenIndex]
	lastColonIndex = inputTrimmed.rfind('::')
	signature = qualifiedName[lastColonIndex + 2:]
	return signature

debug = 0
# Get path from OMRStatistics directory to the python script
path = sys.argv[0]
nameIndex = path.index('getDatabaseSQL.py')
path = path[:nameIndex]
# Get the absolute path to the OMR directory
pathToOMR = os.path.dirname(os.path.realpath(__file__)) + sys.argv[0]
pathToOMR = pathToOMR[:pathToOMR.index('/omr/tools/compiler/') + 5] #get path for omr directory

allFunctions = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allClasses = csv.reader(open(path + 'allClasses','r'), delimiter=";")
overloads = csv.reader(open(path + '../visualization/Overloads/overloads','r'), delimiter=";")
overrides = csv.reader(open(path + '../visualization/Overrides/overrides','r'), delimiter=";")
hierarchies = csv.reader(open(path + '../visualization/Hierarchy/hierarchy','r'), delimiter=";")
functionLocations = csv.reader(open(path + 'functionLocation','r'), delimiter=";")
#Can iterate only once on one variable, need to iterate through these file twice
allFunctions2 = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allClasses2 = csv.reader(open(path + 'allClasses','r'), delimiter=";")


maxFunctionNameLength = -1
maxSignatureLength = -1
for row in allFunctions:
	if maxFunctionNameLength < len(row[0]): maxFunctionNameLength = len(row[0])
	if maxSignatureLength < len(row[1]): maxSignatureLength = len(row[1])

maxNamespaceLength = -1
maxClassNameLength = -1
for row in allClasses2:
	if maxNamespaceLength < len(row[0]) : maxNamespaceLength = len(row[0])
	if maxClassNameLength < len(row[1]) : maxClassNameLength = len(row[1])
	
# Create Database
if not debug: print 'CREATE DATABASE IF NOT EXISTS omrstatisticsdb;'
# Create tables
functions = functionTable(maxFunctionNameLength, maxSignatureLength)
files = FileTable(getOMRLongestPath(pathToOMR))
overloadsTable = OverloadTable()
overridesTable = OverrideTable()
polymorphism = PolymorphismTable()
hierarchiesBase = HierarchiesBase()
classes = ClassTable(maxNamespaceLength, maxClassNameLength)

# Drop tables if they already existed
if not debug:
	print 'DROP TABLE IF EXISTS Function;'
	print 'DROP TABLE IF EXISTS File;'
	print 'DROP TABLE IF EXISTS Class;'
	print 'DROP TABLE IF EXISTS Override;'
	print 'DROP TABLE IF EXISTS Polymorphism;'

# Fill tables
classToIDMap = {}
functionToIDMap = {}
fileToIDMap = {}
functionToFileIDMap = {}
ignoredFunctionSignatures = []

# Fill Files table
id = 0
if not debug: print createTable(files)
for root, subdirs, files in os.walk(pathToOMR):
	for currentFile in files:
		id += 1
		filePath = root + '/' + currentFile
		filePath = filePath.replace('//', '/')
		filePath = filePath[len(pathToOMR) - 4:] # Get relative path
		if not debug: print insertTo('File', [id, filePath])
		fileToIDMap[filePath] = id

		
# Fill Class Table
if not debug: print createTable(classes)
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
	if not debug: print insertTo('Class', [id, namespace, className, isExtensible])

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
if not debug: print createTable(functions)
id = 0
for row in allFunctions2:
	#['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
	if id == 0:
		id += 1
		continue
	
	classQualifiedName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	functionQualifiedName = classQualifiedName + '::' + row[1]
	
	if row[1] in ignoredFunctionSignatures: continue #Ignore signatures declared in a non-OMR file
	fileID = functionToFileIDMap[functionQualifiedName]
	
	classID = classToIDMap[classQualifiedName]
	functionToIDMap[row[1]] = id
	if not debug: print insertTo('Function', [id, row[0], row[1], classID, row[6], row[5], fileID])
	id += 1

# Fill Override table
if not debug: print createTable(overridesTable)
id = 0
for row in overrides:
	#['FunctionID', 'BaseClassID', 'OverridingClassID']
	if id == 0: 
		id += 1
		continue
	
	signature = row[2]
	try: functionID = functionToIDMap[signature]
	except KeyError: # This case is when functions are located outside OMR directory, they will not have an entry in the functionToIDMap
		continue
	
	#Reconstruct qualified names of classes & get IDs
	qualifiedBaseName = row[0] + '::' + row[1] if row[0] != '' else row[1]
	qualifiedOverridingName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	baseClassID = classToIDMap[qualifiedBaseName]
	overridingClassID = classToIDMap[qualifiedOverridingName]
	
	if not debug: print insertTo('Override', [functionID, baseClassID, overridingClassID])
	
# Fill Polymorphism and HierarchiesBase tables
if not debug: print createTable(polymorphism)
if not debug: print createTable(hierarchiesBase)
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
			if not debug: print insertTo('HierarchiesBase', [hierarchyID, previousClassID])
			
			continue
		currentClassID = classToIDMap[clas]
		
		# Duplicate entries will generate in cases of 2 hierarchies that have different bases but merge at some point (so they would have the same top), we remove them here
		key = str(hierarchyID) + ':' + str(previousClassID) + ':' + str(currentClassID)
		if key not in duplicateEntries:
			duplicateEntries.add(key)
			if not debug: print insertTo('Polymorphism', [hierarchyID, previousClassID, currentClassID])
		else: # Based on my testing, no case passed here
			pass
		
		previousClassID = currentClassID
		previousClas = clas
	hierarchyID += 1