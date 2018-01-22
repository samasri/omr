var map = new Map();
function hideDisplay(result) {
	var correspondingSigsDiv = map.get(this);
	if(correspondingSigsDiv.style.display == "") correspondingSigsDiv.style.display = 'block';
	else if(correspondingSigsDiv.style.display == "none") correspondingSigsDiv.style.display = 'block';
	else if(correspondingSigsDiv.style.display == "block") correspondingSigsDiv.style.display = 'none';
}

window.onload = start;
function start() {
	var functionNames = document.getElementsByClassName("parent");
	var sigsDivs = document.getElementsByClassName("overriding");
	
	//Map each signature Div to its corresponding signatures Div
	for(var i = 0; i < functionNames.length; i++) {
		map.set(functionNames[i], sigsDivs[i]);
		functionNames[i].onclick = hideDisplay;
	}
}

