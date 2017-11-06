import re

f = open('csv','r')
content = f.readlines()

class Class:
	name = ""
	methods = []
	methodNames = set() # Cache names for faster searching

class Method:
	name = ""
	override = [] # Class names where this method was overriden
	overload = {} # Class names where this method was overloaded, and the respective number of times the method was overloaded in each class

def getMethod(name, methods):
	for method in methods:
		if method.name == name: return method
	return -1

c = 0

classes = []

for line in content:
	if re.match('[T][R][:][:]', line): 
		c = Class()
		c.name = line[:len(line)-2].strip()
		classes.append(c)
	else:
		# Get the method
		lines = line.strip().split(',')
		if lines[0] not in c.methodNames:
			m = Method()
			m.name = lines[0].strip()
			c.methods.append(m)
			c.methodNames.add(m.name)
		else:
			m = getMethod(lines[0], c.methods)
		
		# Update the method
		if lines[1] is "overload":
			m.overload.update({lines[2], lines[3]})
		else:
			m.override.append(lines[2])


for currentClass in classes:
	if currentClass.name == "TR::CodeGenerator": 
		for method in currentClass.methods