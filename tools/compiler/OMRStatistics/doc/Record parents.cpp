recordParent(childClassName, parentClassName) {
	if(parentClassName != childClassName) {
		vector = map.find(childClassName)
		if(!vector) create new vector
		vector.add(parentClassName)
	}
}

recordParents(classDecl) {
	currentName = classDecl->getNameAsString();
	BI = classDecl->bases_begin();
	BE = classDecl->bases_end();
	for(BC = BI; BC != BE; BC++) { //iterate through all bases
		parent = BC->getType()
		parentName = parent->getAsString()
		if(shouldIgnoreClassName(parentName)) continue
		recordParent(currentName, parentName)
		parentDecl = parent->getCXXRecord()
		if(parentDecl) recordParents(parentDecl)
	}
}

