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