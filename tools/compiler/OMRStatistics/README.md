# Overview
This is a clang plugin that runs on the source code of the file provided in the makefile and collects information about it.

# How to build and run
Running make will build the plugin and run it on OMRCodeGenerator.cpp (in omr/compiler/codegen)
Running make test will test the plugins on all the test cases available so far and makes sure all outputs are as expected

## Functionality of the plugin
## Print hierarchies
Prints out all class hierarchies in this source file (and all its includes).
### Output Format
`<Base Class Name> --> <Parent Class Name> --> ... --> <Top Class Name>`
## Known bug
When a class has 2 children, one of the hierarchies in the plugin output is broken. This case is elaborated in one of the test cases.

## Print Method Information
Prints out each method in each of the class hierarchies, which classes it is overriden in, and how many times it is overloaded in each class.
### Output Format
```
<Hierarchy base class name>
	<Method Name>
		Overriden in:
			<className where it is overloaded>
			<className where it is overloaded>
			<className where it is overloaded>
			...
		Overloaded in:
			<className where it is overloaded>, <# of times overloaded>
			<className where it is overloaded>, <# of times overloaded>
			<className where it is overloaded>, <# of times overloaded>
			...
```

# Testing
This plugin has 5 test cases till now:
* Test 1: Testing the hierarchy functionality
* Test 2: Testing the override functionality when printing method information
* Test 3: Testing the overload functionality when printing method information
* Test 4: Testing the override and overload functionalities together
* Test 5: This should fail, this case elaborates the previously described bug
