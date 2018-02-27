# Collect Method Info Algorithm
```python
Convert hierarchy data structure from the base->top to top->base order
for each hierarchy:
	for each subHierarchy in hierarchy:
		trackersMap = new map //map that contains all methodTrackers for this subHierarchy; it links each methodName to all its trackers; format: methodName --> list of MethodTrackers
		for each class in subHierarchy:
			for each method in class:
					tracker = search for methodTracker in subHierarchy
					if tracker is found: //this is an override
						tracker.addOccurence(class)
					else:
						methodName = name of method
						if method has the same name as one of the trackersMap: //this is an overload
							newTracker = create new tracker with new signature
							trackers = get trackers vector from trackersMap with key: methodName
							trackers.add(newTracker)
						if methodName is not found in any of the trackersMap: //this is a completely new function
							newTracker = create new tracker with new signature
							trackers = new list of trackers
							trackers.add(newTracker)
							trackersMap.add(methodName, trackers)
```