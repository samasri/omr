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
		try:
			file = open(name)
		except IOError: 
			files.pop(name, None)
			continue
		for r in file: 
			files[name].append(r)
		file.close()
	return files

def getFunctionsList(filePath):
	file = open(filePath)
	list = set()
	for row in file:
		row = row.strip()
		if not row: continue
		list.add(row[:row.index('(')])
	file.close()
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

def getNamespaceFromHeader(headerPath):
	if 'runtime/compiler/codegen/' in headerPath: return 'J9'
	elif 'runtime/compiler/x/codegen/' in headerPath: return 'J9::X86'
	elif 'runtime/compiler/x/amd64/codegen/' in headerPath: return 'J9::X86::AMD64'
	elif 'runtime/compiler/x/i386/codegen/' in headerPath: return 'J9::X86::I386'
	elif 'runtime/compiler/p/codegen/' in headerPath: return 'J9::Power'
	elif 'runtime/compiler/z/codegen/' in headerPath: return 'J9::Z'
	elif 'compiler/codegen/' in headerPath: return 'OMR'
	elif 'compiler/x/codegen/' in headerPath: return 'OMR::X86'
	elif 'compiler/x/amd64/codegen/' in headerPath: return 'OMR::X86::AMD64'
	elif 'compiler/x/i386/codegen/' in headerPath: return 'OMR::X86::I386'
	elif 'compiler/p/codegen/' in headerPath: return 'OMR::Power'
	elif 'compiler/z/codegen/' in headerPath: return 'OMR::Z'

def editFile(function, headers, overloaded):
	global PRINT_OVERLOADS
	exitAfterFileEnds = 0
	virtualized = 0
	isSkip = 3
	for (filename,lines) in headers.iteritems(): 
		editTimes = 0
		if isSkip < 2: # Skip 2 files when condition appears
			isSkip += 1
			continue
		for (index,line) in enumerate(headers[filename]):
			if function + '(' in headers[filename][index]:
				# If function is editted more than once in a file, then its overloaded
				editTimes += 1
				namespace = getNamespaceFromHeader(filename)
				if editTimes > 1:
					overloaded.add(function)
					if PRINT_OVERLOADS: 
						print 'Function is overloaded: ' + namespace + '::' + TARGET_CLASS + '::' + function
					return 0 # Function is overloaded, manual check is required
				
				# Virtualize function
				virtualized = 1
				headers[filename][index] = addVirtual(headers[filename][index])
				
				# If function is found in OMR or J9, exit directly after
				if 'compiler/codegen/' in filename or 'runtime/compiler/codegen/' in filename:
					exitAfterFileEnds = 1 
				# If function is found in an X86 namespace, skip the next 2 files (AMD64 and I386)
				if 'compiler/x/codegen/' in filename: isSkip = 0
		if exitAfterFileEnds: return 1
	if virtualized: return 1
	else: return 0

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

def changeHPPs(mainPath, functionsFilePath, ignoredFile):
	# Get mapping between each filename with a list of its lines
	headersOMR = getHeaders(mainPath[0], 'OMR')
	headersJ9 = getHeaders(mainPath[1], 'J9')
	
	functions = getFunctionsList(functionsFilePath)
	
	# Stage virtualization changes in the headers maps 
	ignored1 = set() # Keep track of ignored functions in OMR
	ignored2 = set() # Keep track of ignored functions in OpenJ9
	overloaded = set()
	for f in functions:
		if not editFile(f, headersOMR, overloaded): ignored1.add(f)
	for f in ignored1:
		if not editFile(f, headersJ9, overloaded): ignored2.add(f)
	ignoredFunctions = ignored2.union(overloaded)
	
	# Apply changes to files
	applyHPPEdits(headersOMR)
	applyHPPEdits(headersJ9)
	
	printIgnoredFunctions(ignoredFunctions, ignoredFile)

class FileChange:
	def __init__(self, func, line):
		self.func = func
		self.line = line

def processCallResultsToMap(file):
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
				r = r.split(':', 1)
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
	fileChanges = processCallResultsToMap(file)
	applyCPPEdits(fileChanges)

def append(sigs1, sigs2):
	global PRINT_1
	for sig in sigs2:
		if sig not in sigs1: sigs1[sig] = {}
		for namespace in sigs2[sig]:
			if namespace in sigs1[sig]:
				if PRINT_1:
					print 'Found case: ' + namespace + '::' + TARGET_CLASS + '::' + sig
					print sigs1[sig][namespace]
					print sigs2[sig][namespace]
				continue # Do not change already existing results
			sigs1[sig][namespace] = sigs2[sig][namespace]

def handleEndOfDef(line, sigs, sig, namespace, isDef, ignoredFunctions):
	global PRINT_OVERLOADS
	if sig not in sigs: sigs[sig] = {}
	elif namespace in sigs[sig]: 
		if PRINT_OVERLOADS: 
			print 'Function is overloaded: ' + namespace + '::' + TARGET_CLASS + '::' + sig
		ignoredFunctions.add(sig)
	sigs[sig][namespace] = isDef


def checkHeaders(headers, sigList):
	sigs = {} # Dict: sigs --> namespace --> isDefined
	ignoredFunctions = set() # Keep track of ignored functions
	for sig in sigList:
		found = 0
		for header in headers:
			header = open(header)
			continued = 0 # keep track of function definitions that take multiple lines
			for line in header:
				line = line.strip()
				if '//' in line: line = line[:line.index('//')] # Remove inline comments
				if not line: continue
				if continued or sig + '(' in line:
					namespace = getNamespaceFromHeader(header.name)
					if '{' in line:
						found = 1
						continued = 0
						handleEndOfDef(line, sigs, sig, namespace, 1, ignoredFunctions)
					elif ';' in line:
						found = 1
						continued = 0
						handleEndOfDef(line, sigs, sig, namespace, 0, ignoredFunctions)
					else:
						continued = 1
			if continued == 1: 'Error: file is finished but function definition is not: ' + sig
			header.close()
		if not found: ignoredFunctions.add(sig)
	return sigs, ignoredFunctions

def processQualSig(qualSig):
	qualO = qualSig
	qualSig = qualSig.split(' ')
	qualSigTarget = ''
	for part in qualSig:
		if 'OMR::' in part or 'J9::' in part:
			qualSigTarget = part[:part.index('(')]
			break
	qualSig = qualSigTarget.split('::')
	functionName = ''
	className = ''
	namespace = ''
	for (i, value) in enumerate(qualSig):
		if i == len(qualSig) - 2: className = qualSig[i] # ClassName is before the last part
		elif i == len(qualSig) - 1: functionName = qualSig[i] # Function is the last part
		else: namespace += qualSig[i] + '::' # Everything else is the namespace
	namespace = namespace[:-2] # Remove last :: appended to the namespace variable
	if namespace and '*' == namespace[0]: namespace = namespace.replace('*','')
	if '*' in namespace: print 'Error: unexpected namespace is found: ' + namespace + '::' + TARGET_CLASS + '::' + funcionName
	return namespace, className, functionName

def processDefResultsToMap(file):
	sourceSigs = {} # sig -> namespace -> isDefined
	count = 0
	func = ''
	for r in file:
		r = r.strip()
		if count == 0:
			func = r.replace('::','')
			func = func[:-1]
			count += 1
			continue
		if count > 0:
			if r == '--------------------':
				count = 0
				continue
			else:
				count += 1
				r = r.split(':', 1)
				namespace, className, sig = processQualSig(r[1])
				if className != TARGET_CLASS: continue
				if sig not in sourceSigs: sourceSigs[sig] = {}
				elif namespace in sourceSigs[sig]: 'Error: function is overloaded and overload is not detected in header files: ' + namespace + '::' + TARGET_CLASS + ':: ' + sig + '( is found more than once'
				sourceSigs[sig][namespace] = 1
	return sourceSigs
			
def checkDefinitions(paths, functionsFilePath, results, ignoredFile):
	omrHeaders = getHeaders(paths[0], 'OMR')
	openj9Headers = getHeaders(paths[1], 'J9')
	sigList = getFunctionsList(functionsFilePath)
	headerSigs, ignoredFunctions = checkHeaders(omrHeaders, sigList)
	openJ9Sigs, ignoredFunctions = checkHeaders(openj9Headers, ignoredFunctions)
	append(headerSigs, openJ9Sigs)
	sourceSigs = processDefResultsToMap(results[0])
	sourceSigsOpenJ9 = processDefResultsToMap(results[1])
	append(sourceSigs, sourceSigsOpenJ9)
	
	global PRINT_NO_IMPLEMENTATION
	if PRINT_NO_IMPLEMENTATION:
		for sig in headerSigs:
			for namespace in headerSigs[sig]:
				if headerSigs[sig][namespace] == 0:
					if namespace not in sourceSigs[sig] or sourceSigs[sig][namespace] == 0: 
						print sig + ' has no implementation in: ' + namespace
	
	printIgnoredFunctions(ignoredFunctions, ignoredFile)

# Configuration
PRINT_1 = 0
PRINT_OVERLOADS = 0
PRINT_NO_IMPLEMENTATION = 0
TARGET_CLASS = sys.argv[3]

omrResults = open('callResults.omr')
openj9Results = open('callResults.openj9')
functionsFilePath = 'functions-raw'
ignoredFile = open('ignored','w')
omrGrepResults = open('defResults.omr','r')
openj9GrepResults = open('defResults.openj9','r')

changeCPPs(omrResults)
changeCPPs(openj9Results)
changeHPPs([sys.argv[1], sys.argv[2]],functionsFilePath, ignoredFile)
checkDefinitions([sys.argv[1], sys.argv[2]], functionsFilePath, [omrGrepResults, openj9GrepResults], ignoredFile)