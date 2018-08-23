# This script takes the overridden function query output from the database in a file (whose name is passed as an argument) and processes it to produce 2 outputs:
# 'functions-raw': a file that contains all the signatures that should be virtualized.
# 'functions': contains the queries that should be searched for in the source code to find all calls (that uses `self()`) and function defs in source code (`::functionName(`) of the above list of functions. In addition, the file contains the queries

import sys

def convertToArray(file):
	rows = []
	for r in file: rows.append(r)
	return rows

def createLists(sigs, functionsOut, rawOut):
	callsList = ''
	rawList = ''
	defsList = ''
	max = len(sigs) # Get max to identify last row
	for sig in sigs:
		sig = sig.strip()
		sigQuery = sig[:sig.index('(')]
		
		callsList += "'self()->" + sigQuery + "(' \\\n"
		rawList += sig + '\n'
		defsList += "'::" + sigQuery + "(' \\\n"
	
	functionsOut.write('CALLS_LIST += \\\n' + callsList[:-3])
	functionsOut.write('\n\nDEFS_LIST += \\\n' + defsList[:-3])
	rawOut.write(rawList[:-1])

isFirstUse = 1 # Tracks if createDocPage function has been used before
def createDocPage(dbRows, docPage):
	global isFirstUse
	global TARGET_CLASS
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
		if bc != TARGET_CLASS or oc != TARGET_CLASS:
			print 'Warning: some rows in the db are not related to ' + TARGET_CLASS + ': ' + row
			continue
		if 'operator ' in sig: continue
		if sig in sigSet: continue
		sigSet[sig] = bn + '::' + on
		if 'J9' in on or 'J9' in bn: j9count += 1
		elif 'OMR' in on or 'OMR' in bn: omrcount += 1
		else: warnings.warn('Class found that is neither in OMR nor J9: ' + bn + ' --> ' + on, Warning)

	if isFirstUse:	
		docPage.write('# Functions to virtualize')
		isFirstUse = 0
	i = 0
	for sig in sigSet:
		docPage.write(str(i) + ". " + sig + "\n")
		i += 1
	return sigSet

dbFile = open(sys.argv[1])
TARGET_CLASS = sys.argv[2]
docPage = open('doc', 'w')
listFile = open('functions', 'w')
rawlistFile = open('functions-raw', 'w')

dbRows = convertToArray(dbFile)
sigSet = createDocPage(dbRows, docPage)
createLists(sigSet, listFile, rawlistFile)