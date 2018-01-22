f = open('amd64.hierarchy','r')
r = open('amd64.hierarchy.trimmed', 'w')
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