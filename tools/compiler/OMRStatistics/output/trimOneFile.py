#Takes the a file path+name as an argument and trim it in a file named the same as the filename, but suffixing it with '.trimmed'
#Trimming consists of remove duplicate lines and any line that contains the substring 'std::'
#Example command: python trimOneOutput.py amd64.hierarchy

import sys
f = open(sys.argv[1],'r')
r = open(sys.argv[1] + '.trimmed','w')


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

S = set()
list = []
trim(f, r)