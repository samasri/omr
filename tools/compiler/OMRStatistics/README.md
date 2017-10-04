# Overview
This is a clang plugin that runs on the source code of the file provided in the makefile and collects information about it.

# How to build and run
* Running `make` will build the plugin and run it on _OMRCodeGenerator.cpp_ (in _omr/compiler/codegen_)
* Running `make test` will test the plugins on all the available test cases and makes sure all outputs are as expected

# Functionality of the plugin
This plugin has 2 main functions:
## 1. Print hierarchies
Prints out all class hierarchies in this source file (and all its includes).
### Output Format
`<Base Class Name> --> <Parent Class Name> --> ... --> <Top Class Name>`
### Known bug
When a class has 2 children, one of the hierarchies in the plugin output is broken. This case is elaborated in one of the test cases.

## 2. Print Method Information
Prints out each method in each of the class hierarchies, which classes it is overriden in, and how many times it is overloaded in each class.
### Output Format
The output is in csv format. If a method is overloaded, a record will be shown including the class where it was overloaded and the number of times it was overloaded in that class. Whereas if the method was overriden, the output will contain multiple records, each representing an occurence of the method in the specified class (the _Number of Times Overloaded_ space will be kept void).
```
<Hierarchy base class name>
<Method Name>,<Type: override or overload>, <Class Name>, <Number of Times Overloaded>
```

# Testing
This plugin has 5 test cases till now:
* Test 1: Testing the hierarchy functionality by having 2 classes where one extends the other
* Test 2: Testing the hierarchy functionality by having 4 classes that extend each other
* Test 3: Testing the override functionality when printing method information by having a function that is overriden in 2 consecutive classes in a hierarchy
* Test 4: Testing the override functionality when printing method information by having a function that is overriden in 2 non-consecutive classes (having some classes in between) in a hierarchy
* Test 5: Testing the overload functionality when printing method information
* Test 6: Testing the override and overload functionalities together
* Test 7: This should fail, this case elaborates the previously described bug


