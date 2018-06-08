# Processes file sql.out to get the amount of overridden functions per hierarchy
# sql.out is the output table of an sql query that has the following format
# BaseNamespace BaseClassName Signature OverridingNamespace OverridingClassName
# The columns are separated by tabs, this script processed them, takes the unique overridden functions from each class, and joins them in a hierarchy. The results are in the [resources section](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Hierarchies%20Overridden%20Function%20Count%20(OMR%20+%20OpenJ9).md)

class Hierarchy:
	def __init__(self, name):
		self.name = name
		self.omrCounter = 0
		self.j9Counter = 0
		self.sigSet = set()
	def addOccurrence(self, namespace, sig):
		if sig not in self.sigSet:
			self.sigSet.add(sig)			
			if 'OMR' in namespace: self.omrCounter += 1
			elif 'J9' in namespace: self.j9Counter += 1
			
# Get the number of overriddes in each hierarchy
def getTable(r, sameMap):
	processedClassNames = set()
	hierarchies = []
	for row in r:
		if not row: continue
		# Get info from record
		query = row.split('\t')
		if len(query) != 5: print 'error'
		bn = query[0].strip()
		bc = query[1].strip()
		sig = query[2].strip()
		on = query[3].strip()
		oc = query[4].strip()
		# Remove self and constructors
		if sig == 'self()': continue
		if sig == bc + '()': continue
		# Since we are assuming that a hierarchy is defined by all classes having the same classname, finding an override where baseClassName != overridingClassName means this is an exceptin to the definition; we keep track of such cases in sameMap to merge them later
		if bc != oc:
			if bc not in sameMap: sameMap[bc] = []
			sameMap[bc].append(oc)
		isFound = 0
		# Add occurrence of signature in hierarchy
		for h in hierarchies:
			if h.name == bc:
				isFound = 1
				h.addOccurrence(bn, sig)
		if not isFound:
			h = Hierarchy(bc)
			h.addOccurrence(bn, sig)
			hierarchies.append(h)
	# Return each hierarchy with its corresponding counts in a list
	w = []
	for h in hierarchies:
		toPrint = '| ' + h.name + ' | ' + str(h.omrCounter) + ' | ' + str(h.j9Counter) + ' |'
		w.append(toPrint)
	return w

# Merge exceptional hierarchies together
def merge(r, sameMap):
	# Load the information from getTable() in 2 maps, connecting the className to each count
	class2omr = {}
	class2j9 = {}
	for row in r:
		split = row.split('|')
		clas = split[1].strip()
		omrCount = int(split[2].strip())
		j9Count = int(split[3].strip())
		class2omr[clas] = omrCount
		class2j9[clas] = j9Count
	
	# If the className is in sameMap, filled in getTable(), then the 2 hierarchies should be merged (by keeping the same name of the base hierarchy and adding the counts)
	toRemove = set()
	for key in class2omr:
		if key in sameMap:
			for value in sameMap[key]:
				class2omr[key] += int(class2omr[value])
				class2j9[key] += int(class2j9[value])
				toRemove.add(value)
	
	# Remove the duplicate hierarchies (after merging)
	for key in toRemove: 
		del class2omr[key]
		del class2j9[key]
	
	# Return info in a list
	w = []
	for key in class2omr:
		w.append('| ' + key + ' | ' + str(class2omr[key]) + ' | ' + str(class2j9[key]) + ' |')
	return w

# Sort the table according the the omr counter from highest to lowest
def sort(r):
	id2row = {}
	id2count = {}
	id = 0
	for row in r:
		if not row: continue
		id += 1
		id2row[id] = row
		row = row.split('|')
		id2count[id] = int(row[2])

	i = 0
	list = []
	while i < len(id2count):
		i += 1
		maxID = -1
		max = -1
		id = 0
		while id < len(id2count):
			id += 1
			count = id2count[id]
			if max < count:
				maxID = id
				max = count
		id2count[maxID] = -1
		list.append(maxID)
	
	w = []
	w.append('| ID | Hierarchy | Number of Overridden Functions in OMR | Number of Overridden functions in J9 |')
	w.append('| --- | --- | --- | --- |')
	id = 0
	for r in list:
		id += 1
		w.append('| ' + str(id) + ' ' + id2row[r])
	return w

r = open('sql.out','r')
w = []
sameMap = {}
w = getTable(r, sameMap)
w = merge(w, sameMap)
w = sort(w)
f = open('Hierarchies Overridden Function Count (OMR + OpenJ9).md', 'w')
for line in w: f.write(line + '\n')