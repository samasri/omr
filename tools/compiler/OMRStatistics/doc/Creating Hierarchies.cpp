struct LinkedNode { //Changes to structures
	std::vector<LinkedNode*> parents; 
}

struct Hierarchy {
	std::vector<std::map<std::string, std::vector<MethodTracker>*>> methodName2MethodTrackerVec;
}

fillHierarchies(classHierarchyMap) {
	for(itr : classHierarchyMap) {
		std::string child = itr.first;
		std::vector<std::string> parents = itr.second;
		for(parent : parents) {
			LinkedNode newNode = new LinkedNode;
			
			if(both child and parent found in hierarchy) {
				if(parent is a base of a hierarchy) { //parent has no children
					child.parent = createNewVector();
					child.parent.push_back(parent);
					deleteHierarchy(parent)
				}
				else { //if parent has children
					child.parent.push_back(parent);
				}
			}
			
			else if(child found only) {
				emplace newNode in class2Address
				std::vector<std:string> subParents = child.parents;
				if(!subParents) createNewVector();
				subParents.push_back(newNode);
			}				
			else if(parent found only) {
				emplace newNode in class2Address
				std::vector<std:string subParents = newNode.parents;
				if(!subParents) createNewVector();
				subParents.push_back(parent);
				if(parent is base of Hierarchy) modifyBase(parent, newNode);
				else { //parent has one or more children
					newHierarchy = createNewHierarchy();
					newHierarchy.base = newNode
					hierarchies.push_back(hierarchy)
				}
				
			}
			
			else /*if(both child and parent not found in hierarchy)*/ {
				make new Hierarchy;
				add hierarchy to hierarchies map
				make new LinkedNode for child
				emplace both, child & parent, in class2Address map
			}
		}
	}
}

collectMethodInfo(class2Methods) {
	for(hierarchy : hierarchies) {
		std::vector<std::vector<std::string>> subHierarchies = getTopToBaseAsArray(hierarchy);
		int subHierarchyIndex = 0;
		for(std::vector<std::string> subHierarchy : subHierarchies) {
			//Get right methodTracker vector (based on subHierarchy)
			methodName2MethodTracker = new vector;
			hierarchy->methodName2MethodTrackerVec.push_back(methodName2MethodTracker);
			//Process each method in each class of subHierarchy
			for(LinkedNode current : subHierarchy) {
				className = current.name
				if(className not found in class2methods) continue
				methods = class2methods.find(className)
				for(method : methods) {
					sameName = new bool;
					tracker = searchForTracker(methodName2MethodTracker, method, &sameName)
					if(tracker) //This is an override
						tracker.addOccurence(className);
					else {
						methodName = getName(method);
						isFirstOccurence = true;
						if(sameName) { //This is an overload
							isFirstOccrence = false;
							trackers = methodName2MethodTracker.find(methodName)->second
						}
						else { //This is a completely new function
							trackers = new vector();
							methodName2MethodTracker.emplace(methodName, trackers);
						}
						MethodTracker newTracker(className, method, isFirstOccurence);
						trackers->emplace_back(newTracker);
						subHierarchyIndex++;
					}
				}
			}
		}
	}
}

getTopToBaseAsArray(hierarchy) {
	array = new vector<std::string>;
	stack = new vector<std::string>;
	getTopToBaseAsArray(hierarhchy->base, array, stack)
	subHierarchies = new vector<std::vector<std::string>>;
	subHierarchies.add(new vector<std::string>);
	for(node : array) { //Traverse from last node to first node
		currentHierarchy = subHierarchies.back() //get last element
		currentHierarchy.add(node);
		if(node == hierarchy.base) subHierarchies.add(new vector<std::string>);
	}
	subHierarchies.pop_back; //remove last element since its an empty vector
	return subHierarchies;
}

void getTopToBaseAsArray(node, array, stack) {
	stack.add(node)
	array.add(node)
	int counter = 0;
	for(parent : node.parents) {
		if(node.parents.size > 1 && counter > 0) for(n : stack) array.add(n) //add everything on the stack
		getTopToBaseAsArray(parent, array, stack)
		counter++;
	}
	stack.remove(node)
}

//TODO: edit method tracker (addOccurrence) to handle overrides in subHierarchies? Not really right?
//TODO: edit searchForTracker (same algorithm, just use different signature)