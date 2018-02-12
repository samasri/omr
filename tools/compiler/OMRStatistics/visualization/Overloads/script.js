var map = new Map();
function hideDisplay(result) {
	var correspondingSigsDiv = map.get(this);
	if(!correspondingSigsDiv) return;
	if(correspondingSigsDiv.style.display == "") correspondingSigsDiv.style.display = 'block';
	else if(correspondingSigsDiv.style.display == "none") correspondingSigsDiv.style.display = 'block';
	else if(correspondingSigsDiv.style.display == "block") correspondingSigsDiv.style.display = 'none';
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
	var functionNames = document.getElementsByClassName("functionName");
	var sigsDivs = document.getElementsByClassName("overriding");
	
	//Map each signature Div to its corresponding signatures Div
	for(var i = 0; i < functionNames.length; i++) {
		var id = functionNames[i].id;
		var nb = id.substr(1, id.length - 1);
		var sigUl = document.getElementById("s" + nb);
		map.set(functionNames[i], sigUl);
		functionNames[i].onclick = hideDisplay;
		document.getElementById('showImplicit').onclick = toggleImplicitDecls;
	}
}

