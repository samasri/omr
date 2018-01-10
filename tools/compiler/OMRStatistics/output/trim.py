f = open('i386.overloads','r')
r = open('i386.overloads.trimmed', 'w')
S = set()
list = []
while True:
	x = f.readline()
	x = x.rstrip()
	if not x: break
	if not x in S: list.append(x)
	S.add(x)

for line in list:
	r.write(line + "\n")