#This sanity check takes the overrides from all architectures and makes sure there is no record of any function being overridden in the TR NameSpace, other than the constructors

import csv
import sys

path = ''
if len(sys.argv) > 1: path = sys.argv[1] + '/'
try: amd64 = open(path + 'amd64.overrides', 'r')
except IOError as e: amd64 = 0
if amd64: amd64 = csv.reader(amd64, delimiter=";")

try: i386 = open(path + 'i386.overrides', 'r')
except IOError as e: i386 = 0
if i386: i386 = csv.reader(i386, delimiter=";")

try: p = open(path + 'p.overrides', 'r')
except IOError as e: arm = 0
if p: p = csv.reader(p, delimiter=";")

try: z = open(path + 'z.overrides', 'r')
except IOError as e: z = 0
if z: z = csv.reader(z, delimiter=";")

try: arm = open(path + 'arm.overrides', 'r')
except IOError as e: arm = 0
if arm: arm = csv.reader(arm, delimiter=";")

def isConstructor(className, functionSignature):
	pos = functionSignature.find('(')
	functionName = functionSignature[:pos]
	return (functionName == className)

def printErrors(f):
	list = []
	for row in f:
		if not row: continue
		if 'Arch:' in row[0]: continue
		baseClassName = row[1]
		functionSignature = row[2]
		if row[3] == 'TR' and not isConstructor(baseClassName, functionSignature):
			counter = 0
			for r in row:
				counter += 1;
				sys.stdout.write(r)
				if counter != len(row): sys.stdout.write(';')
				else: print('')

if amd64: printErrors(amd64)
if i386: printErrors(i386)
if p: printErrors(p)
if z: printErrors(z)
if arm: printErrors(arm)