#Takes the tool's output file path+name as an argument (without the suffix; that is: .hierarchy, .overrides, and .overloads) and trim them in a file named the same as the filename, but suffixing it with '.trimmed'
#Trimming consists of remove duplicate lines and any line that contains the substring 'std::'
#Example command: python trim3Outputs.py amd64

import sys
f1 = open(sys.argv[1] + '.hierarchy','r')
r1 = open(sys.argv[1] + '.hierarchy.trimmed', 'w')
f2 = open(sys.argv[1] + '.overloads','r')
r2 = open(sys.argv[1] + '.overloads.trimmed', 'w')
f3 = open(sys.argv[1] + '.overrides','r')
r3 = open(sys.argv[1] + '.overrides.trimmed', 'w')

def trim(f, r):
	while True:
		x = f.readline()
		x = x.rstrip()
		if not x: break
		if "std::" in x: continue
		if not x in S: list.append(x)
		S.add(x)

	for line in list:
		r.write(line + "\n")

S = set()
list = []
trim(f1, r1)
S = set()
list = []
trim(f2, r2)
S = set()
list = []
trim(f3, r3)