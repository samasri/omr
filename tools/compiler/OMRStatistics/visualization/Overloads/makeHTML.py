#Takes the overrides csv path+name as input and produces an html file with the same name (suffixed by ".html")

import csv
import sys
isImplicitMap = {}
isVirtualMap = {}

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
	
	def addSig(self, sig, isImplicit, isVirtual):
		self.methodSigs.append(sig)
		isImplicitMap[sig] = isImplicit
		isVirtualMap[sig] = isVirtual

def searchMethodName(methodName, methods):
	for method in methods:
		if method.methodName == methodName:
			return method
	return -1

def processOverloadsCSV(r, f):
	firstTime = 1
	methodName = ""
	methods = []
	for row in f:
		if not row: continue
		result = searchMethodName(row[0], methods)
		if result != -1:
			result.addSig(row[3] + "::" + row[4] + "::" + row[1], row[5], row[6])
		else:
			n = methodStruct(row[0])
			n.addSig(row[3] + "::" + row[4] + "::" + row[1], row[5], row[6])
			methods.append(n)
	return methods
			

def printOverloadsBody(r, f):
	r.write("<body>\n")
	r.write("	 <button id='showImplicit'>Show Implicit Declarations</button>")
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
				className = ""
				if isImplicitMap[sig] == '1':
					className = " class='implicit'"
				elif isVirtualMap[sig] == '1':
					className = " class='virtual'"
				r.write("				<li" + className + "><p>" + sig + "</p></li>\n")
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

if sys.argv[1] == '': sys.exit()
overloadsCSV = csv.reader(open(sys.argv[1],'r'), delimiter=";")
overloadsOut = open(sys.argv[1] + '.html', 'w')
printOverloadsHTML(overloadsOut, overloadsCSV)