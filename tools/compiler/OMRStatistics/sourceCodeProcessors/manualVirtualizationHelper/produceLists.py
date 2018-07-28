# This script takes the overridden function query (found below) output from the each database (omr and openj9) in files (whose names are passed as arguments) and processes them to produce 2 outputs (for each database):
# 'functions-raw': a file that contains all the signatures that should be virtualized.
# 'functions': contains the queries that should be searched for in the source code to find all calls (that uses `self()`) of the above list of functions.

# SELECT DISTINCT bc.namespace, bc.classname, of.signature, oc.namespace, oc.classname
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1 and bf.isVirtual = 0 and of.isVirtual = 0 and bf.isImplicit = 0 and of.isImplicit = 0 and bc.className='CodeGenerator';
import sys

def convertToArray(file):
	rows = []
	for r in file: rows.append(r)
	return rows

def createList(sigs, functionsOut, rawOut):
	functionsOut.write('LIST += \\\n')
	count = 0
	max = len(sigs) # Get max to identify last row
	for sig in sigs:
		count += 1
		sig = sig.strip()
		sigQuery = sig[:sig.index('(')]
		
		# Print list of files for make
		end = '\\\n' if count != max else ''
		functionsOut.write("'self()->" + sigQuery + "(' " + end)
		
		# Print list of files for manual checking
		end = '\n' if count != max else ''
		rawOut.write(sig + end)

isFirstUse = 1 # Tracks if createDocPage function has been used before
def createDocPage(dbRows, docPage):
	global isFirstUse
	omrcount = 0 # Keep track of signature count of functions in a class belonging to an OMR namespace
	j9count = 0 # Keep track of signature count of functions in a class belonging to a J9 namespace
	sigSet = {} # Store sigs that need to be virtualized
	for row in dbRows:
		if not row: continue
		row = row.split('\t')
		bn = row[0].strip()
		bc = row[1].strip()
		sig = row[2].strip()
		on = row[3].strip()
		oc = row[4].strip()
		if sig in sigSet: continue
		sigSet[sig] = bn + '::' + on
		if 'J9' in on or 'J9' in bn: j9count += 1
		elif 'OMR' in on or 'OMR' in bn: omrcount += 1
		else: warnings.warn('Class found that is neither in OMR nor J9: ' + bn + ' --> ' + on, Warning)

	if isFirstUse:	
		docPage.write('# Functions to virtualize')
		isFirstUse = 0
	for sig in sigSet: docPage.write("* " + sig + "\n")
	return sigSet


docPage = open('doc', 'w')
list = open('functions', 'w')
rawlist = open('functions-raw', 'w')
dbFile = open(sys.argv[1])

dbRows = convertToArray(dbFile)
sigSet = createDocPage(dbRows, docPage)
createList(sigSet, list, rawlist)