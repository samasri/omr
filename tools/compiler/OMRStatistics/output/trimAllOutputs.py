#Takes the tool's output file path+name as an argument (without the suffix; that is: .hierarchy, .overrides, and .overloads) and trim them in a file named the same as the filename, but suffixing it with '.trimmed'
#Trimming consists of remove duplicate lines and any line that contains the substring 'std::'
#Example command: python trim3Outputs.py amd64

import sys
reads = []
writes = []
reads.append(open(sys.argv[1] + '.hierarchy','r'))
writes.append(open(sys.argv[1] + '.hierarchy.trimmed', 'w'))
reads.append(open(sys.argv[1] + '.overloads','r'))
writes.append(open(sys.argv[1] + '.overloads.trimmed', 'w'))
reads.append(open(sys.argv[1] + '.overrides','r'))
writes.append(open(sys.argv[1] + '.overrides.trimmed', 'w'))
reads.append(open(sys.argv[1] + '.weirdHierarchy','r'))
writes.append(open(sys.argv[1] + '.weirdHierarchy.trimmed', 'w'))
reads.append(open(sys.argv[1] + '.allFunctions','r'))
writes.append(open(sys.argv[1] + '.allFunctions.trimmed', 'w'))

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

for (read, write) in zip(reads, writes):
	S = set()
	list = []
	trim(read, write)