f = open('amd64.hierarchy','r')
r = open('amd64.hierarchy.clean', 'w')
S = set()
list = []
while True:
	x = f.readline()
	x = x.rstrip()
	if not ("std::" in x): 
		list.append(x)
	if not x: break

for line in list:
	r.write(line + "\n")