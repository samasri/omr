import random
import sys
import os
import filecmp

inputDir = "tests/input"
count = 0
hasEverFailed = 0
for filename in os.listdir(inputDir):
    count += 1
    inputFile = "tests/" + filename.replace("cpp", "out")
    outputFile = "tests/expectedOutput/" + filename.replace("cpp", "outC")
    if not filecmp.cmp(inputFile, outputFile):
        hasEverFailed = 1
        testNb = inputFile[len(inputFile)-5]
        print("Failed on Test #" + testNb)
if hasEverFailed: print("Other than that, all test cases succeeded")
else: print("All test cases succeeded")