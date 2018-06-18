# This file collects information needed in the SPLC paper, it serves as a way to fill the following [table](https://github.com/ualberta-smr/paper-almasri-SPLC/wiki/Impact-Section-Data). Also, it is assumed that the database schema is as described [here](https://github.com/samasri/omr/blob/d9f9cab1b5e19a118b436d9c5d88f02d6689454b/tools/compiler/OMRStatistics/doc/resources/Database.png)

WARNINGS = 0 # Change to true to print warnings

import csv
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))[:-20] #Assuming this file is in a directory named output

# load the hierarchies in program memory
f = open(path + 'visualization/Hierarchy/hierarchy', 'r')
hierarchies = [] # consits of arrays of classes, each representing a hierarchy
rc = 0
for row in f:
	rc += 1
	if rc == 1: continue
	row = row.split(';')
	if not bool(int(row[0])): continue # skip non-extensible classes
	classes = row[1].split(' --> ')
	for i, c in enumerate(classes): classes[i] = c.strip()
	hierarchies.append(classes)

# Takes a CSV file (delimiter = '\t') that has |namespace|ClassName|Signature|
# Returs a map between each class and all the signatures in its hierarchies
# ignoredClasses is an out parameter
# Assumes that hierarchies is a global variable representing all the known hierarchies 
def getClassSigs(file, ignoredClasses):
	classSigs = {}
	for r in file:
		if not r: continue
		r = r.split('\t')
		namespace = r[0].strip()
		className = r[1].strip()

		qualClassName = className if namespace == '' else namespace + '::' + className

		sig = r[2].strip()
		
		# Ignore classes that are not in the hierarchies classes
		isFound = 0
		for h in hierarchies:
			for c in h:
				if qualClassName == c: isFound = 1
		if not isFound: ignoredClasses.add(qualClassName.strip())
		
		# Record sig in class
		if qualClassName not in classSigs: classSigs[qualClassName] = set()
		classSigs[qualClassName].add(sig)
	return classSigs

# Takes classSigs - a mapping between each class and its signature
# ignoredClasses is an output parameter
# Returns a compilation of the set of signatures in each hierarchy using the (assumed) global variable - hierarchies
def getHierarchySigs(classSigs, ignoredClasses):
	hierarchySigs = {}
	hierarchyID = 0
	visitedClasses = set() # Records already visited classes
	for h in hierarchies:
		hierarchyID += 1
		hierarchySigs[hierarchyID] = set()
		for currentClass in h:
			if currentClass in visitedClasses: continue # skip already visited classes
			if currentClass not in classSigs: 
				ignoredClasses.add(currentClass)
				continue # Ignoring classes with no functions and non-extensible classes
			visitedClasses.add(currentClass)
			for sig in classSigs[currentClass]: hierarchySigs[hierarchyID].add(sig)
	return hierarchySigs


# ----------------------------------Addressing data #1 ----------------------------------
# select count(*) from class;
# select count(*) from class where isExtensible=1;
print "On average, X% of classes are extensible"

# ----------------------------------Addressing data #2----------------------------------

# SELECT DISTINCT oc.namespace, oc.classname, bc.namespace, bc.classname
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1;

file = open('1')
recordSet = set()
for row in file:
	if not row: continue
	row = row.split('\t')
	r1 = row[0].strip() + '::' + row[1].strip() # Get first qualified class name in record
	#r2 = row[2].strip() + '::' + row[3].strip() # Get second qualified class name in record
	recordSet.add(r1)
	#recordSet.add(r2)

print 'Number of extensible classes with overridden functions: ' + str(len(recordSet))

# ----------------------------------Addressing data #3----------------------------------


# SELECT namespace, classname, signature
# FROM function as f
# INNER JOIN class as c on c.id = f.classID
# where c.isExtensible = 1;
file = open('2')
ignoredClasses = set()
classSigs = getClassSigs(file, ignoredClasses)
hierarchySigs = getHierarchySigs(classSigs, ignoredClasses)

# Calculate total number of methods in all extensible classes
totalSigs = 0
for key, value in hierarchySigs.iteritems(): totalSigs += len(value)
print 'Number of methods inside extensible classes: ' + str(totalSigs)
if WARNINGS and len(ignoredClasses) > 0: print '\tWarning: some classes (' + str(len(ignoredClasses)) + ') were ignored when getting this result'

# ----------------------------------Addressing data #4----------------------------------

# SELECT DISTINCT bc.namespace, bc.classname, bf.signature
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1;
file = open('3')
ignoredClasses = set()
classSigs = getClassSigs(file, ignoredClasses)
hierarchySigs = getHierarchySigs(classSigs, ignoredClasses)

# Calculate total number of methods in all extensible classes
totalSigs = 0
for key, value in hierarchySigs.iteritems(): totalSigs += len(value)
print 'Number of overridden methods inside extensible classes: ' + str(totalSigs)
if WARNINGS and len(ignoredClasses) > 0: print '\tWarning: some classes (' + str(len(ignoredClasses)) + ') were ignored when getting this result'

# ----------------------------------Addressing data #5----------------------------------

# SELECT DISTINCT bc.namespace, bc.classname, bf.signature
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1 and oc.namespace='TR';
file = open('4')
ignoredClasses = set()
classSigs = getClassSigs(file, ignoredClasses)
hierarchySigs = getHierarchySigs(classSigs, ignoredClasses)

# Calculate total number of methods in all extensible classes
totalSigs = 0
for key, value in hierarchySigs.iteritems(): totalSigs += len(value)
print 'Number of overridden methods inside TR:: extensible classes: ' + str(totalSigs)
if WARNINGS and len(ignoredClasses) > 0: print '\tWarning: some classes (' + str(len(ignoredClasses)) + ') were ignored when getting this result'

# ----------------------------------Addressing data #6-7 ----------------------------------
# Get number of hierarchies
f = open(path + 'visualization/Hierarchy/hierarchy', 'r')
f = csv.reader(f, delimiter=';')

extensibleCounter = 0
allCounter = 0
classCounter = 0
for row in f:
	isExtensible = row[0]
	hierarchy = row[1]
	classes = hierarchy.split(' --> ')
	if isExtensible == '1': 
		extensibleCounter += 1
		classCounter += len(classes)
	allCounter += 1

avgLength = float(classCounter) / float(extensibleCounter)
print 'Number of extensible hierarchies: ' + str(extensibleCounter)
print 'Average number of classes in extensible hierarchies: ' + str(avgLength)

# ----------------------------------Addressing data #8----------------------------------


# SELECT namespace, classname, signature
# FROM function as f
# INNER JOIN class as c on c.id = f.classID
# where c.isExtensible = 1;
file = open('2')
ignoredClasses = set()
classSigsAll = getClassSigs(file, ignoredClasses)

# SELECT DISTINCT bc.namespace, bc.classname, bf.signature
# FROM Override as o
# INNER JOIN Function as bf on bf.id = o.BaseFunctionID
# INNER JOIN Function as of on of.id = o.overridingFunctionID
# INNER JOIN Class as bc on bc.id = bf.classID
# INNER JOIN Class as oc on oc.id = of.classID
# WHERE bc.isExtensible = 1 and oc.isExtensible = 1;
file = open('3')
ignoredClasses = set()
classSigsOverridden = getClassSigs(file, ignoredClasses)

percentageOverridden = []
for h in hierarchies:
	totalFunctions = 0
	overriddenFunctions = 0
	for c in h:
		if c not in classSigsAll: 
			ignoredClasses.add(c)
			continue # Ignoring classes with no functions and non-extensible classes
		if c not in classSigsOverridden: 
			ignoredClasses.add(c)
			continue # Ignoring classes with no functions and non-extensible classes
		totalFunctions += len(classSigsAll[c])
		overriddenFunctions += len(classSigsOverridden[c])
		percentageOverridden.append(float(overriddenFunctions)/float(totalFunctions))

total = 0.0
for p in percentageOverridden: total += p
print 'Average of the percentage of overridden methods per hierarchy: ' + str(total/len(percentageOverridden))