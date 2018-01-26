import csv

#Print the head tag for all web pages
def printHead(r):
	r.write("<head>\n")
	r.write("	<title>Overloads</title>\n")
	r.write("	<meta charset='utf-8'/>\n")
	r.write("	<link href='style.css' rel='stylesheet'>\n")
	r.write("	<script type='text/javascript' src='script.js'></script>\n")
	r.write("</head>\n")

#Used in printing the overloads HTML file
class methodStruct:
	def __init__(self, name):
		self.methodName = name
		self.methodSigs = []
	
	def addSig(self, sig):
		self.methodSigs.append(sig)

def processOverloadsCSV(r, f):
	firstTime = 1
	methodName = ""
	methods = []
	for row in f:
		if not row: continue
		if methodName != row[0]:
			n = methodStruct(row[0])
			n.addSig(row[3] + "::" + row[4] + "::" + row[1])
			methods.append(n)
		else:
			methods[-1].methodSigs.append(row[3] + "::" + row[4] + "::" + row[1])
		methodName = row[0]
	return methods
			

def printOverloadsBody(r, f):
	r.write("<body>\n")
	r.write("    <div id='content'>\n")
	methods = processOverloadsCSV(r, f)
	counter= 0
	for m in methods:
		counter += 1
		r.write("		<div class='function'>\n")
		className = "functionName"
		if len(m.methodSigs) > 1: className += " multiple"
		r.write("			<p class='" + className + "' id='n" + str(counter) + "'>" + m.methodSigs[0] + "</p>\n")
		if len(m.methodSigs) > 1:
			r.write("			<ul class='signatures' id='s" + str(counter) + "'>\n")
			isFirst = 1
			for sig in m.methodSigs:
				if isFirst:
					isFirst = 0
					continue
				r.write("				<li><p>" + sig + "</p></li>\n")
			r.write("			</ul>\n")
		r.write("		</div>\n")
	r.write("	</div>\n")
	r.write("</body>\n")

def printOverloadsHTML(r, f):
	r.write("<!doctype html>\n")
	r.write("<html>\n")
	printHead(r)
	printOverloadsBody(r, f)
	r.write("</html>\n")


overloadsCSV = csv.reader(open('amd64.overloads','r'), delimiter=";")
overloadsOut = open('amd64.overloads.html', 'w')
printOverloadsHTML(overloadsOut, overloadsCSV)