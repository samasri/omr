#Takes the path of the overrides output file (of all the classes) as an argument
import random
import sys
import os
import filecmp
import csv

def executeSanityCheck(input):
	success = 1
	for row in input:
		if not row: continue
		list = []
		if row[0] == "TR":
			className = row[1]
			signature = row[2]
			index = signature.find('(');
			signatureName = signature[0:index];
			if signatureName.lower() == className.lower():
				list.append(row)
		if len(list) > 0:
			success = 0

	if success: 
		print("Sanity check succeeded")
		return 1
	else: 
		print("Sanity check failed")
		return 0


inputDir = "tests/input"
count = 0
hasEverFailed = 0
for input in os.listdir(inputDir):
    count += 1
    output1 = "tests/" + input.replace("cpp", "hierarchy")
    output2 = "tests/" + input.replace("cpp", "overrides")
    output3 = "tests/" + input.replace("cpp", "overloads")
    expectedOutput1 = "tests/expectedOutput/" + input.replace("cpp", "hierarchy")
    expectedOutput2 = "tests/expectedOutput/" + input.replace("cpp", "overrides")
    expectedOutput3 = "tests/expectedOutput/" + input.replace("cpp", "overloads")
    if (not filecmp.cmp(output1, expectedOutput1)) or (not filecmp.cmp(output2, expectedOutput2)) or (not filecmp.cmp(output3, expectedOutput3)):
        hasEverFailed = 1
        testName = input.replace(".cpp","")
        print("Failed on Test: " + testName)

overridesOutputFile = csv.reader(open(sys.argv[1],'r'), delimiter=";")
if not executeSanityCheck(overridesOutputFile):
	hasEverFailed = true

if hasEverFailed: print("Other than that, all test cases succeeded")
else: print("All test cases succeeded")