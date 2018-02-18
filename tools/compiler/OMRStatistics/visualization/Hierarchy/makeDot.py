f = open('hierarchy', 'r')
o = open('graph.dot', 'w')

o.write('graph {\n')
uniqueLines = set()
for row in f:
	row = row.strip().split(" --> ")
	prevClas = -1
	for clas in row:
		if prevClas == -1: 
			prevClas = clas
			continue
		toWrite = '"' + prevClas + '" -- "' + clas + '"\n'
		if toWrite in uniqueLines:
			prevClas = clas
			continue
		uniqueLines.add(toWrite)
		o.write(toWrite)
		prevClas = clas
o.write('}')