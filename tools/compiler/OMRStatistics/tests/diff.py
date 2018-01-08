import random
import sys
import os
import filecmp

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
if hasEverFailed: print("Other than that, all test cases succeeded")
else: print("All test cases succeeded")