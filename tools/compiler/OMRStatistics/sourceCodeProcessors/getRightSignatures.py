# This file takes the data file that contains function information and returns signatures of functions that appear in the same class name under the 3 architecture nameSpaces: X86, Power, and Z
import sys
import os
import csv

path = os.path.dirname(os.path.abspath(__file__))

f = open(path + '/data', 'r') # CSV file containing 'functionSignature; nameSpace; className'

# Store Class information
class Tuple:
	def __init__(self, nameSpace, className):
		self.nameSpace = nameSpace
		self.className = className
		if self.className[-1] == '\n': self.className = self.className[:-1]
	
	def __eq__(self, other):
		classNameEq = (self.className == other.className)
		nameSpaceEq = (self.nameSpace == other.nameSpace)
		return classNameEq and nameSpaceEq
	def __repr__(self):
		return self.nameSpace + '::' + self.className

map = {} # Mapping every signature to what classes it belongs to
for row in f:
	row = row.split(';')
	sig = row[0]
	className = row[1]
	nameSpace = row[2]
	clas = Tuple(className,nameSpace)
	if sig not in map: 
		classes = []
		classes.append(clas)
		map[sig] = classes
	else:
		classes = map[sig]
		if clas in classes:
			print 'Duplicate Entry in source file: ' + row
		else:
			classes.append(clas)

toPrint = ''
#toPrint += 'VAR =\\\n'

for sig in map:
	clasList = map[sig]
	
	isPrint = 0
	
	clas2NameSpace = {}
	for clas in clasList: # Link each class to the nameSpaces it appears in
		if clas.className not in clas2NameSpace:
			nameSpaces = set()
			clas2NameSpace[clas.className] = nameSpaces
		else:
			nameSpaces = clas2NameSpace[clas.className]
		nameSpaces.add(clas.nameSpace)
	
	# Check if the signature is appearing in the same class in multiple nameSpaces
	for className in clas2NameSpace:
		nameSpaces = clas2NameSpace[className]
		
		isOMR = 0
		isX86 = 0
		isPower = 0
		isZ = 0
		isARM = 0
		
		for nameSpace in nameSpaces:	
			if nameSpace == 'OMR': isOMR = 1
			if nameSpace == 'OMR::X86': isX86 = 1
			if nameSpace == 'OMR::Power': isPower = 1
			if nameSpace == 'OMR::Z': isZ = 1
			if nameSpace == 'OMR::ARM': isARM = 1
		if isX86 and isPower and isZ: isPrint = 1
	if isPrint: print sig[:sig.index('(') + 1] 