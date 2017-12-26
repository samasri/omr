struct Hierarchy { //Additions to the structure
	std::hash_map<std::string, MethodTracker> methodName2MethodTracker;
}
class MethodTracker {
	std::string methodName;
	std::string methodSignature;
	bool firstOccurence; //Specifies if this is the first occurrence of this function name or not (for overload)
	int nbOfOccurences; //How many times overridden
	std::string baseClassName; //The first occurrence of this signature, this value includes namespace
	std::unordered_set<std::string>* classesOverridden; //Tracks the classes where this method was overridden
	
	MethodTracker(std::string qualifiedMethodSignature, firstOccurence) {
		gets methodName, methodSignature, baseNamespace, and baseClassname out of the qualified signature
		nbOfOccurences = 0;
		create new set classesOverridden
		firstOccurence = firstOccurence
	}
	
	void addOccurence {
		nbOfOccurences++;
		add to classesOverridden set
	}
}

void collectMethodInfo(class2methodsMap) {
	for(each class in each hierarchy) {
		methods = pull method list from class2methodsMap
		for(each method in methods) {
			search for methodTracker with methodSignature
			if(tracker found) //this is an override
				tracker.addOccurence()
			else {
				methodName = get method name;
				if(tracker found with same name) //this is an overload
					isFirstOccurence = false
				else //this is the first occurrence of this method
					isFirstOccurence = true
				create methodTracker and add it to methodName2MethodTracker map
			}
		}
	}
}

void printOverrides() {
	for(each tracker in each hierarchy) {
		for(each className in tracker.classesOverriden) 
			print a csv record showing the override relation between that class and the class before it in tracker.classesOverriden
	}
}

void printOverloads() {
	for(each record in methodName2MethodTracker) {
		for(each methodTracker in record.second) {
			baseNamespace = get from className string
			baseClassName = get from className string
			print name /*(record.first)*/, signature, whether its a firstOccurence, baseNamespace, and baseClassName
		}
	}
}
