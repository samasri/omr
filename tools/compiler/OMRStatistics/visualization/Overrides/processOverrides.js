//Assumes that the CSV input file is in the same directory and is named 'overrides'
//Uses that file to fill the HTML DOM with the right objects
function CSVToArray( strData, strDelimiter ){
	// Check to see if the delimiter is defined. If not,
	// then default to comma.
	strDelimiter = (strDelimiter || ",");

	// Create a regular expression to parse the CSV values.
	var objPattern = new RegExp(
		(
			// Delimiters.
			"(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

			// Quoted fields.
			"(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

			// Standard fields.
			"([^\"\\" + strDelimiter + "\\r\\n]*))"
		),
		"gi"
		);


	// Create an array to hold our data. Give the array
	// a default empty first row.
	var arrData = [[]];

	// Create an array to hold our individual pattern
	// matching groups.
	var arrMatches = null;


	// Keep looping over the regular expression matches
	// until we can no longer find a match.
	while (arrMatches = objPattern.exec( strData )){

		// Get the delimiter that was found.
		var strMatchedDelimiter = arrMatches[ 1 ];

		// Check to see if the given delimiter has a length
		// (is not the start of string) and if it matches
		// field delimiter. If id does not, then we know
		// that this delimiter is a row delimiter.
		if (
			strMatchedDelimiter.length &&
			strMatchedDelimiter !== strDelimiter
			){

			// Since we have reached a new row of data,
			// add an empty row to our data array.
			arrData.push( [] );

		}

		var strMatchedValue;

		// Now that we have our delimiter out of the way,
		// let's check to see which kind of value we
		// captured (quoted or unquoted).
		if (arrMatches[ 2 ]){

			// We found a quoted value. When we capture
			// this value, unescape any double quotes.
			strMatchedValue = arrMatches[ 2 ].replace(
				new RegExp( "\"\"", "g" ),
				"\""
				);

		} else {

			// We found a non-quoted value.
			strMatchedValue = arrMatches[ 3 ];

		}


		// Now that we have our value string, let's add
		// it to the data array.
		arrData[ arrData.length - 1 ].push( strMatchedValue );
	}

	// Return the parsed data.
	return( arrData );
} //Source: https://stackoverflow.com/questions/1293147/javascript-code-to-parse-csv-data

var list;
function iterateChildren(node) {
	var children = node.childNodes;
	for(var i = 0; i < children.length; i++) {
		list.push(children[i])
	}
	for(var i = 0; i < children.length; i++) {
		iterateChildren(children[i], list)
	}
}


function getParagraphWithHTML(node, className) {
	list = [];
	iterateChildren(node);
	var result = -1;
	for(var i = 0; i < list.length; i++)
		if(list[i].tagName == "P" && list[i].innerHTML == className) result = list[i];
	return result;
}

function addNewFunction(content, signature, baseClassName, overridingClassName) {
	var li = document.createElement("LI");
	li.className = "container function";
	content.appendChild(li);
	
	var p = document.createElement("P");
	p.className = "functionP";
	li.appendChild(p);
	p.innerHTML = baseClassName + "::" + signature;
	
	var ul = document.createElement("UL");
	ul.className = "overriding";
	ul.style.display = "none";
	li.appendChild(ul);
	
	var subLI = document.createElement("LI");
	ul.appendChild(subLI);
	
	p = document.createElement("P");
	p.innerHTML = overridingClassName;
	subLI.appendChild(p);
	
	return li
}

function processCSV(csv) {
	var array = CSVToArray(csv, ";");
	var content = document.getElementById('content');
	var string = "";
	var functionSig2id = {};
	var functionSigs2FirstOccurrence = {}
	for(var i = 0; i < array.length; i++) {
		var row = array[i];
		var baseClassName = row[0] + "::" + row[1];
		var overridingClassName = row[3] + "::" + row[4];
		var signature = row[2];
		var isImplicit = row[3];
		var counter = 0;
		
		if(!functionSig2id[signature]) {
			var li = addNewFunction(content, signature, baseClassName, overridingClassName);
			
			functionSig2id[signature] = li;
			functionSigs2FirstOccurrence[signature] = baseClassName;
		}
		
		else { //When signature has more than one record
			var li = functionSig2id[signature];
			
			//iterate through children to find the baseClassName
			var child = li.childNodes[1];
			var rightP = getParagraphWithHTML(child, baseClassName);
			if(rightP != -1) { //Case the we have a nested override
				var parentLI = rightP.parentNode;
				parentLI.className = "container";
				
				if(parentLI.childNodes.length == 1) {
					var ul = document.createElement("UL");
					parentLI.appendChild(ul);
				}
				
				else var ul = parentLI.childNodes[1];
				
				var li2 = document.createElement("LI");
				ul.appendChild(li2);
				
				var p = document.createElement("P");
				p.innerHTML = overridingClassName;
				if(isImplicit) {
					p.style.color = 'red';
					p.className = "implicit";
				}
				li2.appendChild(p);
			}
			else { 
				var firstOccurrence = functionSigs2FirstOccurrence[signature];
				if(firstOccurrence == baseClassName) { //Case when overload is in same hierarchy, but not nested under an already existing override
					
					var ul = li.childNodes[1];
					
					var li2 = document.createElement("LI");
					ul.appendChild(li2);
					
					var p = document.createElement("P");
					p.innerHTML = overridingClassName;
					li2.appendChild(p);
				}
				else { //Case when the function appears in a different hierarchy (we need a new list)
					var li = addNewFunction(content, signature, baseClassName, overridingClassName);
					functionSig2id[signature] = li;
					functionSigs2FirstOccurrence[signature] = baseClassName;
				}
			}
		}
	}
	var html = content.parentNode.parentNode.parentNode;
}

function hideDisplay() {
	var ul = this.childNodes[1];
	if(ul.style.display == "none") ul.style.display = 'block';
	else/*if (ul.style.display == "block")*/
		ul.style.display = 'none';
}

function makeUIpretty() {
	var functionNames = document.getElementsByClassName("function");
	for(var i = 0; i < functionNames.length; i++) functionNames[i].onclick = hideDisplay;
}

function handleRequest() {
	if(this.readyState === 4) {
		processCSV(this.responseText);
		makeUIpretty();
	}
}

function toggleImplicitDecls() {
	var decls = document.getElementsByClassName("implicit");
	if(decls[0].style.display == 'block') for(var i = 0; i  < decls.length; i++) {
		decls[i].style.display = 'none';
		this.innerHTML = "Hide Implicit Declarations";
	}
	else {
		for(var i = 0; i  < decls.length; i++) decls[i].style.display = 'block';
		this.innerHTML = "Show Implicit Declarations";
	}
}

window.onload = start;
function start() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = handleRequest;
	request.open('Get', 'overrides');
	request.send();
	document.getElementById('showImplicit').onclick = toggleImplicitDecls;
}