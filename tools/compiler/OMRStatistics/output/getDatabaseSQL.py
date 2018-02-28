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
	for value in vector: result += str(value) + ', '
	result = result[:len(result)-2]
	result += ')'
	return result


path = sys.argv[0]
nameIndex = path.index('getDatabaseSQL.py')
path = path[:nameIndex]

allFunctions = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
allClasses = csv.reader(open(path + 'allClasses','r'), delimiter=";")


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
overloads = OverloadTable()
overrides = OverrideTable()
polymorphism = PolymorphismTable()
classes = ClassTable(maxNamespaceLength, maxClassNameLength)

# Print create table queries
#print createTable(functions)
#print createTable(files)
#print createTable(overloads)
#print createTable(overrides)
#print createTable(polymorphism)
#print createTable(classes)

# Fill tables
classToIDMap = {}
id = 1
for row in allClasses:
	#['ID', 'Namespace', 'ClassName', 'IsExtensible']
	isExtensible = row[0]
	classes = row[1].split(' --> ')
	for fullClassName in classes:
		lastColonIndex = fullClassName.rfind('::')
		if lastColonIndex == -1: lastColonIndex = 0
		namespace = fullClassName[:lastColonIndex]
		className = fullClassName[lastColonIndex:]
		classToIDMap[namespace + '::' + className] =  id
		#print insertTo('Class', [id, namespace, className, isExtensible])
	id += 1

allFunctions = csv.reader(open(path + 'allFunctions','r'), delimiter=";")
id = 1
for row in allFunctions:
	#['ID', 'FunctionName', 'Signature', 'ClassID', 'IsVirtual', 'IsImplicit', 'FileID']
	if id == 1:
		id += 1
		continue
	classID = classToIDMap[row[3] + '::' + row[4]]
	print classID
	input = [id, row[0], row[1], 'ClassID', row[6], row[5], -1]
	id += 1