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

function processCSV(csv) {
	var array = CSVToArray(csv, ";");
	var content = document.getElementById('content');
	var string = "";
	var functionSig2id = {};
	var functionSigs2id = {}
	for(var i = 0; i < array.length; i++) {
		var row = array[i];
		var baseClassName = row[0] + "::" + row[1];
		var overridingClassName = row[3] + "::" + row[4];
		var signature = row[2];
		var counter = 0;
		
		if(!functionSig2id[signature]) {
			var div = document.createElement("DIV");
			div.className = "function";
			content.appendChild(div);
			
			var p = document.createElement("P");
			p.className = "parent";
			div.appendChild(p);
			p.innerHTML = baseClassName + "::" + signature;
			
			var ul = document.createElement("UL");
			ul.className = "overriding";
			div.appendChild(ul);
			
			var li = document.createElement("LI");
			li.className = "container";
			ul.appendChild(li);
			
			p = document.createElement("P");
			p.innerHTML = overridingClassName;
			li.appendChild(p);
			
			functionSig2id[signature] = div;
		}
		
		else { //When signature has more than one record
			var div = functionSig2id[signature];
			
			//iterate through children to find the baseClassName
			var child = div.childNodes[1];
			var rightP = getParagraphWithHTML(child, baseClassName);
			if(rightP != -1) { //Case the we have a nested override
				var parentLI = rightP.parentNode;
				parentLI.className = "container";
				
				var ul = document.createElement("UL");
				parentLI.appendChild(ul);
				
				var li = document.createElement("LI");
				ul.appendChild(li);
				
				var p = document.createElement("P");
				p.innerHTML = overridingClassName;
				li.appendChild(p);
			}
			else {
				//alert("Not found: " + signature + " -- " + baseClassName + " -- " + overridingClassName);
			}
		}
	}
}

function hideDisplay() {
	var ul = this.childNodes[1];
	if(ul.style.display == "") ul.style.display = 'block';
	else if(ul.style.display == "none") ul.style.display = 'block';
	else if(ul.style.display == "block") ul.style.display = 'none';
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

window.onload = start;
function start() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = handleRequest;
	request.open('Get', 'amd64.overrides');
	request.send();
	
	
}