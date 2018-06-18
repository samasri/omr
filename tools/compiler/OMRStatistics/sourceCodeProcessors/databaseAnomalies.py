# This script compares the Class.sql generated by running OMRStatistics on OMR and OpenJ9 to find anomalies and inconsistencies; it is serving [issue #54](https://github.com/samasri/omr/issues/54)

omr = open('/home/sam/omr/tools/compiler/OMRStatistics/database/Class.sql')
openj9 = open('/home/sam/3openj9-omrstatistics/openj9-openjdk-jdk9/build/linux-x86_64-normal-server-release/vm/omr/tools/compiler/OMRStatistics/database/Class.sql')


# Represents a record in the Class table
class Query:	
	def __init__(self, id, namespace, classname, isextensible):
		self.id = id
		self.namespace = namespace
		self.classname = classname
		self.isextensible = isextensible
	
	def __str__(s):
		return '[' + s.id + ', ' + s.namespace + ', ' + s.classname + ', ' + s.isextensible + ']'
	
	def getQualName(self):
		return self.namespace + '::' + self.classname if self.namespace != '' else self.classname

# Processes a row in the CSV file and converts it into a Query object
def getQuery(query):
	id = query[0].strip().replace("'", "")
	namespace = query[1].strip().replace("'", "")
	classname = query[2].strip().replace("'", "")
	isextensible = query[3].strip().replace("'", "")
	return Query(id, namespace, classname, isextensible)

classes = set() # all visited classes
rc = 0
for r in openj9:
	rc += 1
	if rc < 10: continue
	if not r: continue
	query = r[r.index('(') + 1:r.rfind(')')].split(",")
	query = getQuery(query)
	
	key = query.getQualName()
	classes.add(key)

rc = 0
namespaces = {}
counter = 0
for r in omr:
	rc += 1
	if rc < 10: continue
	if not r: continue
	query = r[r.index('(') + 1:r.rfind(')')].split(",")
	query = getQuery(query)
	
	key = query.getQualName()
	if key not in classes:
		if 'testing' in query.namespace or 'TestCompiler' in query.namespace: continue # ignore classes that are not expected to be found in OpenJ9 project
		counter += 1
		if query.namespace not in namespaces: namespaces[query.namespace] = set()
		namespaces[query.namespace].add(query)

for n in namespaces: 
	for q in namespaces[n]: print q

print counter