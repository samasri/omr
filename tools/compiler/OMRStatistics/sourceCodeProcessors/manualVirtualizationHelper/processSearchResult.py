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
	fileChanges = processCallResultsToMap(file)
	applyCPPEdits(fileChanges)
	
def getListFromFile(file):
	list = set()
	for row in file:
		row = row.strip()
		if not row: continue
		list.add(row[:row.index('(')])
	return list

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

def append(sigs1, sigs2):
	for sig in sigs2:
		if sig not in sigs1: sigs1[sig] = {}
		for namespace in sigs2[sig]:
			if namespace in sigs1[sig]: continue# Do not change already existing results
			sigs1[sig][namespace] = sigs2[sig][namespace]

def handleEndOfDef(line, sigs, sig, namespace, isDef, ignoredFunctions):
	if sig not in sigs: sigs[sig] = {}
	elif namespace in sigs[sig]: 
		# print 'Function is overloaded (in ' + namespace + '): ' + sig
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
				if '//' in line: line = line[:line.index('//')] # Remove comments
				if not line: continue
				if continued or sig in line:
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
				elif namespace in sourceSigs[sig]: 'Function is overloaded: ' + namespace + '::' + TARGET_CLASS + ':: ' + sig + '( is found more than once'
				sourceSigs[sig][namespace] = 1
	return sourceSigs
			
def checkDefinitions(paths, functionsFile, results):
	omrHeaders = getHeaders(paths[0], 'OMR')
	openj9Headers = getHeaders(paths[1], 'J9')
	sigList = getListFromFile(functionsFile)
	headerSigs, ignoredFunctions = checkHeaders(omrHeaders, sigList)
	openJ9Sigs, ignoredFunctions = checkHeaders(openj9Headers, ignoredFunctions)
	append(headerSigs, openJ9Sigs)
	sourceSigs = processDefResultsToMap(results[0])
	sourceSigsOpenJ9 = processDefResultsToMap(results[1])
	append(sourceSigs, sourceSigsOpenJ9)
	
	# for sig in headerSigs:
		# print sig + ':'
		# for namespace in headerSigs[sig]:
			# print '\t' + namespace + ': ' + str(headerSigs[sig][namespace])
	# print '----------------------------'
	# for sig in sourceSigs:
		# print sig + ':'
		# for namespace in sourceSigs[sig]:
			# print '\t' + namespace + ': ' + str(sourceSigs[sig][namespace])
	
	for sig in headerSigs:
		for namespace in headerSigs[sig]:
			if headerSigs[sig][namespace] == 0:
				if namespace not in sourceSigs[sig] or sourceSigs[sig][namespace] == 0: 
					print sig + ' has no implementation in: ' + namespace
		
		
	
	#print warning
	return ignoredFunctions

omrResults = open('callResults.omr')
openj9Results = open('callResults.openj9')
functionsFile = open('list-raw')
ignoredFile = open('ignored','w')
omrGrepResults = open('defResults.omr','r')
openj9GrepResults = open('defResults.openj9','r')
TARGET_CLASS = sys.argv[3]

# changeCPPs(omrResults)
# changeCPPs(openj9Results)
# changeHPPs(sys.argv[1],functionsFile, 'omr', ignoredFile)
# changeHPPs(sys.argv[2],functionsFile, 'j9', ignoredFile)
checkDefinitions([sys.argv[1], sys.argv[2]], functionsFile, [omrGrepResults, openj9GrepResults])