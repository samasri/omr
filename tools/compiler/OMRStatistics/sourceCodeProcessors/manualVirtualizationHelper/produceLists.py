# This script takes the overridden function query (found below) output from the database in a file (whose name is passed as an argument) and processes it to produce 2 outputs:
# 'list-raw': a file that contains all the signatures that should be virtualized.
# 'list': contains the queries that should be searched for in the source code to find all calls (that uses `self()`) of the above list of functions.

# SELECT DISTINCT bc.namespace, bc.classname, of.signature, oc.namespace, oc.classname
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1 and bf.isVirtual = 0 and of.isVirtual = 0 and bf.isImplicit = 0 and of.isImplicit = 0 and bc.className='CodeGenerator';
import sys

f = open(sys.argv[1])
list = open('list', 'w')
rawlist = open('list-raw', 'w')

# Convert file to array of strings
rows = []
for r in f: rows.append(r)

list.write('LIST += \\\n')
count = 0
max = len(rows) # Get max to identify last row
for row in rows:
	count += 1
	if count < 3: continue
	row = row.split(' | ')
	row[0] = row[0][1:].strip()
	row[1] = row[1].strip()
	row[2] = row[2][:-2].strip()
	sig = row[0][:row[0].index('(')]
	
	# Print list of files for make
	end = '\\\n' if count != max else ''
	if row[2] != '1': list.write("'self()->" + sig + "(' " + end)
	
	# Print list of files for manual checking
	end = '\n' if count != max else ''
	if row[2] != '1': rawlist.write(row[0] + end)	