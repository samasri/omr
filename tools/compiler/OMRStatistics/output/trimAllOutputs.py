#Takes the tool's output file path+name as an argument (without the suffix; that is: .hierarchy, .overrides, and .overloads) and trim them in a file named the same as the filename, but suffixing it with '.trimmed'
#Trimming consists of remove duplicate lines and any line that contains the substring 'std::'
#Example command: python trim3Outputs.py amd64

import sys

outputs = ['hierarchy', 'weirdHierarchy', 'allClasses', 'overloads', 'allFunctions', 'overrides', 'functionLocation', 'avg']

reads = []
writes = []
for output in outputs:
	reads.append(open(sys.argv[1] + '.' + output,'r'))
	writes.append(open(sys.argv[1] + '.' + output + '.trimmed', 'w'))

def trim(f, r):
	while True:
		x = f.readline()
		x = x.rstrip()
		if not x: break
		if "std::" in x: continue
		if 'Arch:' in x: list.append(x)
		elif not x in S: list.append(x)
		S.add(x)

	for line in list:
		r.write(line + "\n")

for (read, write) in zip(reads, writes):
	S = set()
	list = []
	trim(read, write)