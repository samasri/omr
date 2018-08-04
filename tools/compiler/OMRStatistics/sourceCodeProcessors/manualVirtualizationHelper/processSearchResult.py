import sys
import collections

def getHeaders(mainPath, namespace):
	files = collections.OrderedDict() # To iterate the paths in order later
	global TARGET_CLASS
	genericHeaderName = namespace + TARGET_CLASS + '.hpp'
	files[mainPath + 'compiler/codegen/' + genericHeaderName] = []
	files[mainPath + 'compiler/x/codegen/' + genericHeaderName] = []
	files[mainPath + 'compiler/x/amd64/codegen/' + genericHeaderName] = []
	files[mainPath + 'compiler/x/i386/codegen/' + genericHeaderName] = []
	files[mainPath + 'compiler/p/codegen/' + genericHeaderName] = []
	files[mainPath + 'compiler/z/codegen/' + genericHeaderName] = []
	
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
			#else: print 'Not found: ' + change.line
		read.close()
		write = open(fileName, "w")
		write.write(fileStr)
		write.close()

def changeCPPs(file):
	fileChanges = processResultsToMap(file)
	applyCPPEdits(fileChanges)
	
def getListFromFile(file):
	list = set()
	for row in file:
		row = row.strip()
		if not row: continue
		list.add(row[:row.index('(') + 1])
	return list

def getNamespaceFromHeader(headerPath):
	if 'compiler/codegen/' in headerPath: return 'OMR'
	if 'compiler/x/codegen/' in headerPath: return 'OMR::X86'
	if 'compiler/x/amd64/codegen/' in headerPath: return 'OMR::X86::AMD64'
	if 'compiler/x/i386/codegen/' in headerPath: return 'OMR::X86::I386'
	if 'compiler/p/codegen/' in headerPath: return 'OMR::Power'
	if 'compiler/z/codegen/' in headerPath: return 'OMR::Z'

def getNamespaceFromClassName(name):
	#Enum(OMR, X86, Power, Z, AMD64, I386)
	name = name.upper()
	name = name.split('::')
	returnNb = 0
	className = name[len(name) - 2]
	global TARGET_CLASS
	if className != TARGET_CLASS: return -1
	for p in r:
		if p == 'OMR': returnNb = 1
		if p == 'X86': returnNb = 2
		if p == 'Power': returnNb = 3
		if p == 'Z': returnNb = 4
		if p == 'AMD64': returnNb = 5
		if p == 'I386': returnNb = 6
	return returnNb

def append(sigs1, sigs2):
	for sig in sigs2:
		if sig in sigs1: print 'Error: entry already exists'
		sigs1[sig] = {}
		for namespace in sigs2[sig]:
			if namespace in sigs1[sig]: print 'Error: entry already exists'
			#sigs1[sig1] = 
			sigs2[sig][namespace]

def checkHeaders(headers, sigList):
	sigs = {} # Dict: sigs --> namespace --> isDefined
	ignoredFunctions = [] # Keep track of ignored functions
	for sig in sigList:
		found = 0
		for header in headers:
			header = open(header)
			continued = 0 # keep track of function definitions that take multiple lines
			for line in header:
				if not line: continue
				if continued:
					if '{' in line: 
						sigs[sig][namespace] = 1
						continued = 0
					elif ';' in line: 
						sigs[sig][namespace] = 0
						continued = 0
				line = line.strip()
				if sig in line:
					namespace = getNamespaceFromHeader(header.name)
					if '{' in line:
						found = 1
						if sig not in sigs: sigs[sig] = {}
						elif namespace in sigs: print 'Function is overloaded: ' + sig
						sigs[sig][namespace] = 1
					elif ';' in line:
						found = 1
						if sig not in sigs: sigs[sig] = {}
						elif namespace in sigs: print 'Function is overloaded: ' + sig
						sigs[sig][namespace] = 0
					else:
						found = 1
						conitnued = 1
						if sig not in sigs: sigs[sig] = {}
						elif namespace in sigs: print 'Function is overloaded: ' + sig
			if continued == 1: 'Error: file is finished but function definition is not: ' + sig
			header.close()
		if not found: ignoredFunctions.append(sig)
	
	return sigs, ignoredFunctions

# def checkSources(sigs, grepResults):
	# for r in grepResults:
		# r = split by ': '
		# sig = get signature from r #r[:r.index(')') + 1]
		# namespace = getNamespaceFromClassName(r[1])
		# if sig in sigs and namespace in sigs[sig]:
			# if sigs[sig][namespace] == 1: print 'signature defined twice, in header file and in cpp: ' + sig
			# if sigs[sig][namespace] == 0: sigs[sig][namespace] = 1
		# else: print 'error: target signature not defined in headers: ' + sig
			
def checkDefinitions(paths, functionsFile, results):
	omrHeaders = getHeaders(paths[0], 'OMR')
	openj9Headers = getHeaders(paths[1], 'J9')
	sigList = getListFromFile(functionsFile)
	sigs, ignoredFunctions = checkHeaders(omrHeaders, sigList)
	for f in ignoredFunctions: print f
	openJ9Sigs, ignoredFunctions = checkHeaders(openj9Headers, ignoredFunctions)
	append(sigs, openJ9Sigs)
	for sig in sigs:
		print sig + ':'
		for namespace in sigs[sig]:
			print '\t' + namespace + ': ' + str(sigs[sig][namespace])
	# checkSources(sigs, results[0])
	# checkSources(sigs, results[1])
	return ignoredFunctions

omrResults = open('callResults.omr')
openj9Results = open('callResults.openj9')
functionsFile = open('list-raw')
ignoredFile = open('ignored','w')
omrGrepResults = open('defResults.omr','w')
openj9GrepResults = open('defResults.openj9','w')
TARGET_CLASS = sys.argv[3]

# changeCPPs(omrResults)
# changeCPPs(openj9Results)
# changeHPPs(sys.argv[1],functionsFile, 'omr', ignoredFile)
# changeHPPs(sys.argv[2],functionsFile, 'j9', ignoredFile)
ignoredFunctions = checkDefinitions([sys.argv[1], sys.argv[2]], functionsFile, [omrGrepResults, openj9Results])