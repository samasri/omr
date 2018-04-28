# This file collects information needed in the SPLC paper

import csv
import sys
import os


path = os.path.dirname(os.path.abspath(__file__))[:-20] #Assuming this file is in a directory named output

# Get number of hierarchies
f = open(path + 'visualization/Hierarchy/hierarchy', 'r')
f = csv.reader(f, delimiter=';')

extensibleCounter = 0
allCounter = 0
for row in f:
	isExtensible = row[0]
	hierarchy = row[1]
	if isExtensible == '1': extensibleCounter += 1
	allCounter += 1
print 'Number of extensible hierarchies: ' + str(extensibleCounter)