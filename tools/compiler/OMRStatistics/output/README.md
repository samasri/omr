# Output
This directory contains the output of the tool when run on all source files in amd64 and i386.

The tool creates 3 files:
* Hierarchy file: contains all the hierarchies, each one on a new line. Each hierarchy consists of class names separated by arrows ("-->"); the left side is the child and the right side is the parent.
* Overrides file: contains the overrides of each processed function; the file is in csv format with the following fields:
	- Base namespace: namespace of the function being overridden
	- Base class name: class name of the function being overridden
	- Function signature: signature of the function being overridden
	- Overriding namespace: namespace of the overriding function
	- Overriding class name: class name of the overriding function
* Overloads file: contains the overloads of each processed function; the file is in csv format with the following fields:
	- Function name: name of the processed function. Note that even if a function only appeared once (was not overloaded), it appears in this output
	- Function signature: signature in which the function appeared
	- IsFirstOccurence: specifies whether this is the first occurrence of the function in the class hierarchy it belongs to.
	- Namespace: the namespace where this function appeared
	- Class name: the class name where this function appeared