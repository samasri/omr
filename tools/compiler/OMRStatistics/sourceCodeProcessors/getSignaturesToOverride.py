# This script takes a file '1' that is the output of the following SQL query, processes the file and generate a list of all unique signatures of the found functions in a table based on documentation [here](https://github.com/samasri/omr/tree/master/tools/compiler/OMRStatistics/doc/virtualization). The SQL query is inteded to find overridden functions in a specific hierarchy (specified in `bc.className=<hierarchyName>`)

# SELECT DISTINCT bc.namespace, bc.classname, of.signature, oc.namespace, oc.classname
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1 and bf.isVirtual = 0 and of.isVirtual = 0 and bf.isImplicit = 0 and of.isImplicit = 0 and bc.className='CodeGenerator';

import warnings

f = open('1')

omrcount = 0 # Keep track of signature count of functions in a class belonging to an OMR namespace
j9count = 0 # Keep track of signature count of functions in a class belonging to a J9 namespace
keySet = {}
for row in f:
	if not row: continue
	row = row.split('\t')
	bn = row[0].strip()
	bc = row[1].strip()
	sig = row[2].strip()
	on = row[3].strip()
	oc = row[4].strip()
	if sig in keySet: continue
	keySet[sig] = bn + '::' + on
	if 'J9' in on or 'J9' in bn: j9count += 1
	elif 'OMR' in on or 'OMR' in bn: omrcount += 1
	else: warnings.warn('Class found that is neither in OMR nor J9: ' + bn + ' --> ' + on, Warning)

print "| Signature | First occurrence of function in hierarchy (starting the search from base class) | isVirtualized |"
print "| --- | --- | --- |"
for sig in keySet: print "| " + sig + " | " + keySet[sig] + " | 0 |"