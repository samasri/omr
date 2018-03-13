import sys
import csv

path = sys.argv[0][:-10]

f = csv.reader(open(path + 'hierarchy', 'r'), delimiter=";")
o = open(path + 'graph.dot', 'w')
print 'hello'
o.write('digraph {\n')
o.write('\tnode [shape=box];\n')
o.write('\trankdir=BT;\n')
o.write('\tedge[arrowhead="onormal"];\n')
uniqueLines = set()
length = []
for row in f:
	row = row[1]
	print row
	row = row.strip().split(" --> ")
	length.append(len(row))
	prevClas = -1
	for clas in row:
		if prevClas == -1: 
			prevClas = clas
			continue
		toWrite = '\t"' + prevClas + '" -> "' + clas + '"\n'
		if toWrite in uniqueLines:
			prevClas = clas
			continue
		uniqueLines.add(toWrite)
		o.write(toWrite)
		prevClas = clas
o.write('}')

average = 0;
count = 0;
for nb in length:
	average += nb
	count += 1
average = float(average) / float(count)
print 'Average hierarchy length: ' + str(float(average))