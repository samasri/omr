# This python script creates SQL files containing queries that create the database.
# PROJECT_PATH and TARGET_PROJECT variables should be configured
import csv
import sys
import os
import warnings
import random

# Configured per project
PROJECTS_PATH = ['/home/sam/omr/', '/home/sam/3openj9/openj9-openjdk-jdk9/build/'] #Path to build directory
TARGET_PROJECT = 0 # The project that this python file is targetting
# In case the database already have entries
FILE_ID_OFFSET = 0
CLASS_ID_OFFSET = 0
FUNCTION_ID_OFFSET = 0
HIERARCHY_ID_OFFSET = 0
# ------------------------------------------Define Tables------------------------------------------
class FunctionTable:
	def __init__(self, functionNameLength, signatureLength):
		self.tableName = 'Function'
		self.columns = ['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
		self.primaryKey = 'ID'
		self.foreignKeys = {}
		self.foreignKeys['ClassID'] = [ClassTable(-1,-1), 'ID']
		self.foreignKeys['FileID'] = [FileTable(-1), 'ID']
		self.unique = 'Signature, ClassID'
		# Columns
		self.ID = 'INT'
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

class PolymorphismTable:
	def __init__(self):
		self.tableName = 'Polymorphism'
		self.columns = ['HierarchyID', 'ChildClassID', 'ParentClassID']
		self.primaryKey = 'HierarchyID, ChildClassID, ParentClassID'
		self.foreignKeys = {}
		self.foreignKeys['HierarchyID'] = [Hierarchy(), 'ID']
		self.foreignKeys['ChildClassID'] = [ClassTable(-1,-1), 'ID']
		self.foreignKeys['ParentClassID'] = [ClassTable(-1,-1), 'ID']
		# Columns
		self.HierarchyID = 'INT'
		self.ChildClassID = 'INT'
		self.ParentClassID = 'INT'

class Hierarchy:
	def __init__(self):
		self.tableName = 'Hierarchy'
		self.foreignKeys = {}
		self.foreignKeys['BaseClassID'] = [ClassTable(-1,-1), 'ID']
		self.primaryKey = 'ID'
		self.columns = ['ID', 'BaseClassID']
		self.ID = 'INT'
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

class FunctionCall:
	def __init__(self, maxLocationLength):
		self.tableName = 'FunctionCall'
		self.columns = ['CallerFunctionID', 'CalledFunctionID', 'CallSite']
		self.primaryKey = 'CallerFunctionID, CalledFunctionID, CallSite'
		self.foreignKeys = {}
		self.foreignKeys['CallerFunctionID'] = [FunctionTable(-1,-1), 'ID']
		self.foreignKeys['CalledFunctionID'] = [FunctionTable(-1,-1), 'ID']
		# Columns
		self.CallerFunctionID = 'INT'
		self.CalledFunctionID = 'INT'
		self.CallSite = 'VARCHAR(' + str(maxLocationLength) + ')'
# -------------------------------------End of Defining Tables--------------------------------------

# ------------------------------------------Configurations-----------------------------------------

# Configure Paths
pathToProject = PROJECTS_PATH[TARGET_PROJECT]
pathToFile = os.path.dirname(os.path.realpath(__file__))
OMRStatisticsDir = os.path.abspath(os.path.join(pathToFile, os.pardir))
outputPath = OMRStatisticsDir + '/output/'
fileWritePath = OMRStatisticsDir + '/database/'

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

	# Write queries on file and return file
	global allSQLQueries
	allSQLQueries.write(result)
	file.write(result)
	return file

def getOMRLongestPathIn(directory):
	maxPathLength = -1
	for root, subdirs, files in os.walk(directory):
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

	global allSQLQueries
	allSQLQueries.write(result)
	return result

def getSignature(qualifiedName):
	# Handle special case when the class is in an anonymous namespace
	if '(anonymous namespace)' == qualifiedName[:21]: 
		qualifiedName = qualifiedName[23:]
	parenIndex = qualifiedName.find('(')
	inputTrimmed = qualifiedName[:parenIndex]
	lastColonIndex = inputTrimmed.rfind('::')
	signature = qualifiedName[lastColonIndex + 2:]
	return signature

def getRelativePath(path):
	path = path.replace("//", "/");
	if TARGET_PROJECT == 0: return path[len(pathToProject) - 4:] # since "omr/" is of lenght = 4
	elif TARGET_PROJECT == 1:
		relPath = path[len(pathToProject) - 7:]
		relPath = relPath.replace('/build/linux-x86_64-normal-server-release/', 'openj9/')
		return relPath
# -----------------------------------End of Defining Functions-------------------------------------

# Global data structures
classToIDMap = {}
fileToIDMap = {}
functionToFileIDMap = {}
functionQualNametoID = {}
ignoredFunctionSignatures = []
if not debug: allSQLQueries = open(fileWritePath + 'all.sql', 'w') # Write all queries in one file

# Import CSV files for reading and processing
allFunctions = csv.reader(open(outputPath + 'allFunctions','r'), delimiter=";")
allClasses = csv.reader(open(outputPath + 'allClasses','r'), delimiter=";")
hierarchies = csv.reader(open(outputPath + '../visualization/Hierarchy/hierarchy','r'), delimiter=";")
functionLocations = csv.reader(open(outputPath + 'functionLocation','r'), delimiter=";")
functionCalls = csv.reader(open(outputPath + 'functionCalls','r'), delimiter=";")
#Can iterate only once on one variable, need to iterate through these file twice
allFunctions2 = csv.reader(open(outputPath + 'allFunctions','r'), delimiter=";")
functionCalls2 = csv.reader(open(outputPath + 'functionCalls','r'), delimiter=";")
allClasses2 = csv.reader(open(outputPath + 'allClasses','r'), delimiter=";")

# Find max fields length to create database
maxFunctionNameLength = -1
maxSignatureLength = -1 # For Function table
for row in allFunctions2:
	if 'Arch:' in row[0]: continue
	if maxFunctionNameLength < len(row[0]): maxFunctionNameLength = len(row[0])
	if maxSignatureLength < len(row[1]): maxSignatureLength = len(row[1])

maxNamespaceLength = -1
maxClassNameLength = -1
for row in allClasses2:
	if maxNamespaceLength < len(row[0]) : maxNamespaceLength = len(row[0])
	if maxClassNameLength < len(row[1]) : maxClassNameLength = len(row[1])

maxLocationLength = -1 # For FunctionCall table, this shouldn't be different however we have a bug in the plugin
for row in functionCalls2:
	if maxLocationLength < len(row[6]): maxLocationLength = len(row[6])

# Create database and drop any existing tables
if not debug:
	initFile = open(fileWritePath + 'init.sql', 'w')
	createDBQuery = 'CREATE DATABASE IF NOT EXISTS omrstatisticsdb;\n'
	createDBQuery += 'USE omrstatisticsdb;\n'
	initFile.write(createDBQuery)
	allSQLQueries.write(createDBQuery)
	dropQueries = 'DROP TABLE IF EXISTS FunctionCall;\n'
	dropQueries += 'DROP TABLE IF EXISTS Polymorphism;\n'
	dropQueries += 'DROP TABLE IF EXISTS Hierarchy;\n'
	dropQueries += 'DROP TABLE IF EXISTS Function;\n'
	dropQueries += 'DROP TABLE IF EXISTS File;\n'
	dropQueries += 'DROP TABLE IF EXISTS Class;\n'
	initFile.write(dropQueries)
	allSQLQueries.write(dropQueries)

# Create tables
functions = FunctionTable(maxFunctionNameLength, maxSignatureLength)
files = FileTable(getOMRLongestPathIn(pathToProject))
polymorphism = PolymorphismTable()
hierarchiesTable = Hierarchy()
classes = ClassTable(maxNamespaceLength, maxClassNameLength)
functionCallsTable = FunctionCall(maxLocationLength)

# Fill Files table
id = FILE_ID_OFFSET
if not debug: FileFile = createTable(files)
for root, subdirs, files in os.walk(pathToProject):
	for currentFile in files:
		id += 1
		filePath = root + '/' + currentFile
		filePath = getRelativePath(filePath)
				
		if not debug: FileFile.write(insertTo('File', [id, filePath]))
		fileToIDMap[filePath] = id


# Fill Class Table
if not debug: ClassFile = createTable(classes)
id = CLASS_ID_OFFSET
for row in allClasses:
	#['ID', 'Namespace', 'ClassName', 'IsExtensible']
	if id == CLASS_ID_OFFSET:
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
	path = PROJECTS_PATH[TARGET_PROJECT]
	if functionLocation[:len(path)] != path:
		signature = getSignature(functionQualifiedName)
		ignoredFunctionSignatures.append(signature)
		continue
	
	functionLocation = getRelativePath(functionLocation)
	
	colonIndex = functionLocation.find(':')
	functionLocation = functionLocation[:colonIndex]
	fileID = fileToIDMap[functionLocation]
	functionToFileIDMap[functionQualifiedName] = fileID

# Fill Functions table
if not debug: FunctionFile = createTable(functions)
id = FUNCTION_ID_OFFSET
f2r = {} # Function --> row
dupKeys = set() # Functions in visitedFunctions that have more than one value
for row in allFunctions:
	#Function table: ['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
	if 'Arch:' in row[0]: continue
	if id == FUNCTION_ID_OFFSET:
		id += 1
		continue
	classQualifiedName = row[2] + '::' + row[3] if row[2] != '' else row[3]
	functionQualifiedName = classQualifiedName + '::' + row[1]
	
	# Record duplicates and dont add them to the database
	if functionQualifiedName not in f2r:
		f2r[functionQualifiedName] = []
	else:
		dupKeys.add(functionQualifiedName)
		id += 1
		continue

	f2r[functionQualifiedName].append(row)

	# Ignore signatures declared in a non-OMR file
	if row[1] in ignoredFunctionSignatures: continue
	
	fileID = functionToFileIDMap[functionQualifiedName]
	classID = classToIDMap[classQualifiedName]
	
	#print row[0] + ';' + row[1]
	functionQualNametoID[str(classID) + '::' + row[1]] = id
	
	if not debug:
		FunctionFile.write(insertTo('Function', [id, row[0], row[1], classID, row[5], row[4], fileID]))
	id += 1

# Report to the user about the ignored functions
warning = "In allFunctions output, the following lines were ignored due to having previous contradicting records:\n"
printWarning = 0
for k in dupKeys:
	iSig = f2r[k][0]
	for sig in f2r[k]:
		if sig[5] != iSig[5]:
			warning += str(sig) + "\n"
			printWarning = 1
if printWarning: warnings.warn(warning)

# Fill Polymorphism and Hierarchy tables
if not debug: HierarchiesFile = createTable(hierarchiesTable)
if not debug: PolymorphismFile = createTable(polymorphism)
hierarchyID = HIERARCHY_ID_OFFSET
duplicateEntries = set()
for row in hierarchies:
	# ['HierarchyID', 'ChildClassID', 'ParentClassID']
	if hierarchyID == HIERARCHY_ID_OFFSET:
		hierarchyID += 1
		continue
	hierarchy = row[1]
	previousClassID = ''
	for clas in hierarchy.split(' --> '):
		if previousClassID == '': # This is the first class in this hierarchy
			previousClassID = classToIDMap[clas]
			# Record the base class of this hierarchy in the Hierarchy table
			baseClass = clas
			if not debug: HierarchiesFile.write(insertTo('Hierarchy', [hierarchyID, previousClassID]))

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

def insertTo2(table, vector):
	result = ''
	result += 'INSERT INTO ' + table + ' VALUES('
	for value in vector:
		result += "'" + str(value) + "',"
	result = result[:len(result)-1]
	result += ');' +  + '\n'

	global allSQLQueries
	allSQLQueries.write(result)
	return result

id = 0
inconsistentIgnoredFunctions = set()
dupSet = set()
if not debug: FunctionCallFile = createTable(functionCallsTable)
for row in functionCalls:
	if id == 0:
		id += 1
		continue
	
	callerNamespace = row[0]
	callerClassName = row[1]
	callerFuncSig = row[2]
	if callerFuncSig in ignoredFunctionSignatures: continue
	
	calledFuncSignature = row[3]
	receiverNamespace = row[4]
	receiverClassName = row[5]
	callSite = row[6]
	
	callSite = getRelativePath(callSite)
	
	callerQualName = callerNamespace + '::' + callerClassName if callerNamespace != '' else callerClassName
	receiverQualName = receiverNamespace + '::' + receiverClassName if receiverNamespace != '' else receiverClassName
	
	callerID = classToIDMap[callerQualName]
	callerID = functionQualNametoID[str(callerID) + '::' + callerFuncSig]
	try: receiverID = classToIDMap[receiverQualName]
	except:
		#inconsistentIgnoredFunctions.add(receiverQualName) #Issue 
		continue
	try: receiverID = functionQualNametoID[str(receiverID) + '::' + calledFuncSignature]
	except:
		#inconsistentIgnoredFunctions.add(receiverQualName + '::' + calledFuncSignature) #Issue
		continue
	
	if not debug: FunctionCallFile.write(insertTo('FunctionCall', [callerID, receiverID, callSite]))