# Overview
This is a clang plugin that runs on the source code of the file provided in the makefile and collects information about it.

# How to build and run
* Running `make sample` will build the plugin and run it on _OMRCodeGenerator.cpp_ (in _omr/compiler/codegen_)
* Running `make test` will test the plugins on all the available test cases and makes sure all outputs are as expected

# Assumptions
* All classes are expected to be processed when the tool is triggered and added in the output (not only OMR_EXTENSIBLE files)
* Source files for all combinations and architectures are expected to be processed and added to the same output file
* There exists no class that has multiple parents

# Functionality of the plugin
This plugin has 2 main functions:
## 1. Print hierarchies
Prints out all class hierarchies in this source file (and all its includes).

### Known bug
When a class has 2 children, one of the hierarchies in the plugin output is broken. This case is elaborated in one of the test cases.

## 2. Print Method Information
Prints out each method in each of the class hierarchies, which classes it is overriden in, and how many times it is overloaded in each class.

# Output Format
## 1. First functionality (printing hierarchies)
`<Base Class Name> --> <Parent Class Name> --> ... --> <Top Class Name>`

## 2. Second functionality (printing method information)
The output is in csv format. 

* When an method overload is encountered, a record shows the class where the method is overloaded and the name of the overloading method. Hence, multiple overloads of a method will result in multiple records in the CSV file. The output record format for overloads is:
```
<BaseNamespace>,<BaseClassname>,<MethodSignature>,<Type: overload>,<Namespace where overload happens>,<Classname where overload happens>, <OverloadMethodSignature>
```

* In case of a method override, a record in the CSV file shows the name of the namespace and class where this method is overloaded. The output format for overrides is:
```
<BaseNamespace>,<BaseClassname>,<methodSignature>,<Type: override>,<OverridingNamespace>,<OverridingClassname>
```
# Triggerring Functionality
By default, the tool prints the overrides in a CSV file. Passing _OMR_STAT_PRINT_OVERLOADS_ in the command line options when running the tool allows the tool to print the overload information also (in the same CSV). In order to trigger the hierarchy functionality of, _OMR_STAT_PRINT_HIERARCHY_ should be passed.

# Output Sample
Assuming we have the below class hierarchy, the plugin would create the below csv file (it is converted into a table here for better visualization):

![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/ExampleUML.png)

| Base Namespace| Base Classname | Method Signature | Type | Overriding Namespace | Overriding Classname |
| --- | --- | --- | --- | --- | --- |
| OMR | A | f() | override | OMR::Z | A |
| OMR | A | f() | override | Ruby | A |
| ~~OMR:Z~~ | ~~A~~ | ~~f()~~ | ~~override~~ | ~~Ruby~~ | ~~A~~ |
| OMR::Z | A | g() | override | Ruby | A |

# General Design
The tool works as follows:
1. Visits every class declaration in the target source code (let us call the current class: _X_), and iterates through X's parents
2. Every time it jumps from one class/parent to its parent, it records the relationship between these 2 classes in a binary map (let us call it _hierarchy_ map). Since it passes to every class and process all its parents, the tool is expected to find classes that were already processed (when processing the parents of another class lower in the hierarchy); hence the tool would skip any already processed classes.
3. When it finds no more parents, the tool goes back to X and records all its methods in another map (let us call it _function_ map)
4. After visiting all classes in the source code, the processing of these 2 maps starts
5. The tool iterates through all the records in the _hierarchy_ map processing each child/parent relationship to create `Hierarchy` structure. A `Hierarchy` is a data structure that represents a hierarchy of classes, keeping track of the top and base classes and other important information.
6. After that, the tool iterates through the records in the _function_ map creating a `MethodTracker` class. A `MethodTracker` keeps track of the occurence information of a unique function across all classes in a hierarchy. Hence, each _Hierarchy_ structure contains an array of `MethodTracker`s, one for each unique method.

# Testing
This plugin has 5 test cases till now:
* Test 1: Testing the hierarchy functionality by having 2 classes where one extends the other
* Test 2: Testing the hierarchy functionality by having 4 classes that extend each other
* Test 3: Testing the override functionality when printing method information by having a function that is overriden in 2 consecutive classes in a hierarchy
* Test 4: Testing the override functionality when printing method information by having a function that is overriden in 2 non-consecutive classes (having some classes in between) in a hierarchy
* Test 5: Testing the overload functionality when printing method information
* Test 6: Testing the override and overload functionalities together
* Test 7: This should fail, this case elaborates the previously described bug
* Test 8: Representing the case where we have an overriden method that is also overloaded in the parent class. At the moment, OMRStatistics does not differentiate between functions with the same name but different signatures which ends up failing the test. This test projects the aim to update OMRStatistics to make it aware of methods and the need to find a good way to define a method (when a method is overriden, the signature is ignored whereas when the function is overriden the function is considered).
