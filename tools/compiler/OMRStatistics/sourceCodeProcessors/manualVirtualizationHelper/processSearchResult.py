import sys
import collections

def getHeaders(mainPath, namespace):
	files = collections.OrderedDict() # To iterate the paths in order later
	files[mainPath + 'compiler/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	files[mainPath + 'compiler/x/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	files[mainPath + 'compiler/x/amd64/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	files[mainPath + 'compiler/x/i386/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	files[mainPath + 'compiler/p/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	files[mainPath + 'compiler/z/codegen/' + namespace + 'CodeGenerator.hpp'] = []
	
	for (name,lines) in files.iteritems():
		file = open(name)
		for r in file: 
			files[name].append(r)
		file.close()
	return files

def getFunctionsList(file):
	list = []
	for r in file:
		if not r: continue
		list.append(r.strip())
	return list

def addVirtual(line):
	newLine = ''
	addedVirtual = 0
	for c in line:
		if c == ' ': newLine += c #skip initial padding in line
		if not addedVirtual and c != ' ':
			newLine += "virtual "
			addedVirtual = 1
		if c != ' ': newLine += c
	return newLine	

def editFile(function, headers):
	isEditted = 0
	isSkip = 3
	for (filename,lines) in headers.iteritems(): 
		for (index,line) in enumerate(headers[filename]):
			if isSkip < 2: #skip 2 files when condition appears
				isSkip += 1
				continue
			if function in headers[filename][index]:
				headers[filename][index] = addVirtual(headers[filename][index])
				if 'compiler/codegen/' in filename: return 1
				if 'compiler/x/codegen/' in filename: isSkip = 0 # Skip the next 2 files from now
	return 0

def applyHPPEdits(headers):
	for (filename, lines) in headers.iteritems():
		write = open(filename, 'w')
		toWrite = ""
		for line in lines: 
			toWrite += line
		write.write(toWrite)
		write.close()

def printIgnoredFunctions(ignoredFunctions, ignoredFile):
	for f in ignoredFunctions: ignoredFile.write(f + "\n")

def changeHPPs(mainPath, functionsFile, namespace, ignoredFile):
	headers = getHeaders(mainPath, namespace.upper()) # Returns a mapping between each filename and list with its lines
	functions = getFunctionsList(functionsFile)
	ignoredFunctions = [] # Keep track of ignored functions
	for function in functions:
		if not editFile(function, headers): ignoredFunctions.append(function)
	applyHPPEdits(headers)
	printIgnoredFunctions(ignoredFunctions, ignoredFile)

class FileChange:
	def __init__(self, func, line):
		self.func = func
		self.line = line

def processResultsToMap(file):
	fileChanges = {}
	count = 0
	func = ''
	for r in file:
		r = r.strip()
		if count == 0: 
			func = r.replace('self()->','')
			func = func[:-1]
			count += 1
			continue
		if count > 0:
			if r == '--------------------':
				count = 0
				continue
			else: 
				r = r.split(':')
				file = r[0]
				line = r[1]
				if file not in fileChanges: fileChanges[file] = []
				fileChanges[file].append(FileChange(func,line))
				count += 1
	return fileChanges

def applyCPPEdits(fileChanges):
	for fileName in fileChanges:
		changes = fileChanges[fileName]
		read = open(fileName)
		fileStr = "";
		for line in read: fileStr += line
		for change in changes:
			changeWithoutSelf = change.line.replace("self()->" + change.func,change.func)
			if change.line in fileStr: fileStr = fileStr.replace(change.line,changeWithoutSelf)
			else: print 'Not found: ' + change.line
		read.close()
		write = open(fileName, "w")
		write.write(fileStr)
		write.close()

def changeCPPs(file):
	fileChanges = processResultsToMap(file)
	applyCPPEdits(fileChanges)

omrResults = open('results.omr')
openJ9Results = open('results.openj9')
functionsFile = open('list-raw')
ignoredFile = open('ignored','w')

changeCPPs(omrResults)
changeCPPs(openJ9Results)
changeHPPs(sys.argv[1],functionsFile, 'omr', ignoredFile)
changeHPPs(sys.argv[2],functionsFile, 'j9', ignoredFile)