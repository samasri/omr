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
		self.primaryKey = 'FunctionID'
		self.columns = ['FunctionID', 'BaseClassID', 'OverridingClassID']
		self.FunctionID = 'INT'
		self.BaseClassID = 'INT'
		self.OverridingClassID = 'INT'

class PolymorphismTable:
	def __init__(self):
		self.tableName = 'Polymorphism'
		self.primaryKey = 'RecordID'
		self.columns = ['RecordID', 'ChildClassID', 'ParentClassID']
		self.RecordID = 'INT'
		self.ChildClassID = 'INT'
		self.ParentClassID = 'INT'

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

def getOMRLongestPath():
	path = os.path.dirname(os.path.realpath(__file__)) + sys.argv[0]
	pathToOMR = path[:path.index('/omr/tools/compiler/') + 5] #get path for omr directory
	maxPathLength = -1
	for root, subdirs, files in os.walk(pathToOMR):
		maxFileLength = -1
		for currentFile in files:
			if maxFileLength < len(str(currentFile)): maxFileLength = len(str(currentFile))
		
		pathLength = len(str(root)) + maxFileLength
		if maxPathLength < pathLength: maxPathLength = pathLength
	return maxPathLength

def insertTo(table, vector):
	result = ''
	result += 'INSERT INTO ' + table + ' VALUES('
	for value in vector: 
		result += "'" + str(value) + "',"
	result = result[:len(result)-2]
	result += ')'
	return result


path = sys.argv[0]
nameIndex = path.index('getDatabaseSQL.py')
path = path[:nameIndex]

allFunctions = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allFunctions2 = csv.reader(open(path + 'allFunctions','r'), delimiter=";") #Can iterate only once on one variable, need to iterate through this file twice
allClasses = csv.reader(open(path + 'allClasses','r'), delimiter=";")
overloads = csv.reader(open(path + '../visualization/Overloads/overloads','r'), delimiter=";")
overrides = csv.reader(open(path + '../visualization/Overrides/overrides','r'), delimiter=";")
hierarchies = csv.reader(open(path + '../visualization/Hierarchy/hierarchy','r'), delimiter=";")


maxFunctionNameLength = -1
maxSignatureLength = -1
maxNamespaceLength = -1
maxClassNameLength = -1
for row in allFunctions:
	if maxFunctionNameLength < len(row[0]): maxFunctionNameLength = len(row[0])
	if maxSignatureLength < len(row[1]): maxSignatureLength = len(row[1])
	if maxNamespaceLength < len(row[3]) : maxNamespaceLength = len(row[3])
	if maxClassNameLength < len(row[4]) : maxClassNameLength = len(row[4])

# Create tables
functions = functionTable(maxFunctionNameLength, maxSignatureLength)
files = FileTable(getOMRLongestPath())
overloadsTable = OverloadTable()
overridesTable = OverrideTable()
polymorphism = PolymorphismTable()
classes = ClassTable(maxNamespaceLength, maxClassNameLength)

# Fill tables
classToIDMap = {}
functionToIDMap = {}
# Fill Class Table
print createTable(classes)
id = 1
for row in allClasses:
	#['ID', 'Namespace', 'ClassName', 'IsExtensible']
	isExtensible = row[2]
	namespace = row[0]
	className = row[1]
	qualifiedName = namespace + '::' + className if namespace != '' else className;
	classToIDMap[qualifiedName] =  id #Fill classToIDMap from allClasses CSV File
	print insertTo('Class', [id, namespace, className, isExtensible])
	id += 1

# Fill Functions table
print createTable(functions)
id = 0
for row in allFunctions2:
	#['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
	if id == 0:
		id += 1
		continue
	
	qualifiedName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	classID = classToIDMap[qualifiedName]
	functionToIDMap[row[1]] = id
	print insertTo('Function', [id, row[0], row[1], classID, row[6], row[5], -1])
	id += 1

# Fill Overload table
print createTable(overloadsTable)
id = 0
for row in overloads:
	#self.columns = ['FunctionID', 'IsFirstOccurrence']
	if id == 0: 
		id += 1
		continue
	signature = row[1]
	functionID = functionToIDMap[signature]
	print insertTo('Overload', [functionID, row[2]])
	
# Fill Override table
print createTable(overridesTable)
id = 0
for row in overrides:
	#['FunctionID', 'BaseClassID', 'OverridingClassID']
	if id == 0: 
		id += 1
		continue
	
	signature = row[2]
	functionID = functionToIDMap[signature]
	
	#Reconstruct qualfied names of classes & get IDs
	qualifiedBaseName = row[0] + '::' + row[1] if row[0] != '' else row[1]
	qualifiedOverridingName = row[3] + '::' + row[4] if row[3] != '' else row[4]
	baseClassID = classToIDMap[qualifiedBaseName]
	overridingClassID = classToIDMap[qualifiedOverridingName]
	
	print insertTo('Override', [functionID, baseClassID, overridingClassID])
	
# Fill Polymorphism table
print createTable(polymorphism)
id = 0
for row in hierarchies:
	# ['RecordID', 'ChildClassID', 'ParentClassID']
	if id == 0:
		id += 1
		continue
	hierarchy = row[1]
	previousClassID = ''
	for clas in hierarchy.split(' --> '):
		if 'TR_' in clas and '::' not in clas: clas = clas.replace('TR_', 'TR::')
		if 'TRPersistentMemoryAllocator' == clas: clas = 'TR::PersistentMemoryAllocator'
		if previousClassID == '':
			previousClassID = classToIDMap[clas]
			continue
		currentClassID = classToIDMap[clas]
		print insertTo('Polymorphism', [id, previousClassID, currentClassID])
		previousClassID = currentClassID
	id += 1

# Fill Files table
print createTable(files)
