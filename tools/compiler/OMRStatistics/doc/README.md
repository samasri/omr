# Overview
This is a clang plugin that runs on the source code of the file provided in the makefile and collects information about it.

This plugin has 2 main functions:
## 1. Print hierarchies
Prints out all class hierarchies in this source file (and all its includes).

## 2. Print Method Information
Prints out each method in each of the class hierarchies, which classes it is overridden in, and how many times it is overloaded in each class.

# How to build and run
* Running `make sample` will build the plugin and run it on _OMRCodeGenerator.cpp_ (in _omr/compiler/codegen_)
* Running `make test` will test the plugins on all the available test cases and makes sure all outputs are as expected

# Assumptions
* All classes are expected to be processed when the tool is triggered and added in the output (not only OMR_EXTENSIBLE files)
* Source files for all combinations and architectures are expected to be processed and added to the same output file
* There exists no class that has multiple parents
* `std` and `__gnu_cxx` namespaces are out of the scope of the tool.


# Output Format
## 1. First functionality (printing hierarchies)
`<Base Class Name> --> <Parent Class Name> --> ... --> <Top Class Name>`

## 2. Second functionality (printing method information)
The output is in csv format. 

* When a method overload is encountered, a record shows the class where the method is overloaded and the name of the overloading method. Hence, multiple overloads of a method will result in multiple records in the CSV file. The output record format for overloads is:
```
<BaseNamespace>,<BaseClassname>,<MethodSignature>,<Namespace where overload happens>,<Classname where overload happens>, <isImplicit>
```

* In case of a method override, a record in the CSV file shows the name of the namespace and class where this method is overridden. The output format for overrides is:
```
<FunctionName>,<MethodSignature>,<isFirstOccurence>, <Namespace where occurrence happens>,<Class name where occurrence happens>, <isImplicit>
```

The _isImplicit_ field distinguishes implicit declarations from user defined ones.

# Output Sample
Please refer to the 3 controversial cases ([ControversialCase1.md](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/ControversialCase1.md) [ControversialCase2.md](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/ControversialCase2.md), and [ControversialCase3.md](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/ControversialCase3.md)) for more detailed outputs.

# Triggering Functionality
By default, the tool prints the overrides on the default output stream in a CSV format. 

Passing _OMR_STAT_PRINT_OVERLOADS_ in the command line options when running the tool allows the tool to print the overload information also. 

In order to trigger the hierarchy functionality of, _OMR_STAT_PRINT_HIERARCHY_ should be passed.

In order to print the information in 3 separate CSV files, one for each functionality, the path for the filename should be passed in the command line options. For example passing _./output_ to the tool triggers the tool to create 3 files: _./output.hierarchy_, _./output.overrides_, _./output.overloads_

# General Design
The tool works as follows:
1. Visits every class declaration in the target source code and iterates through it's parents
2. Every time the program jumps from one class/parent to its parent, it records the relationship between these 2 classes in a binary map (let us call it _hierarchy_ map). Since it passes to every class and process all its parents, the tool is expected to find classes that were already processed (when processing the parents of another class lower in the hierarchy); hence the tool would skip any already processed classes.
3. When it finds no more parents, the tool goes back to X and records all its methods in another map (let us call it _function_ map)
4. After visiting all classes in the source code, the processing of these 2 maps starts
5. The tool iterates through all the records in the _hierarchy_ map processing each child/parent relationship to create `Hierarchy` structures. A `Hierarchy` is a data structure that represents a hierarchy of classes, keeping track of the base class and other important information.
6. After that, the tool iterates through the records in the _function_ map creating a `MethodTracker` class. A `MethodTracker` keeps track of the occurrence information of a unique function across all classes in a hierarchy. Hence, each _Hierarchy_ structure contains an array of `MethodTracker`s, one for each unique method.

PS: More detailed algorithms for each functionality are found in the 2 files: [Collecting Method Information Algorithm.cpp](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/Collecting%20Method%20Information%20Algorithm.cpp) and [Creating Hierarchies Algorithm.md](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/Creating%20Hierarchies%20Algorithm.md)

# Building & running OMRStatistics on different architectures
The OMRStatistics is built in the [_SO_ target](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/makefile#L24) of the main makefile

To run OMRStatistics on different architectures, a different set of defines and includes should be used when running each architecture. The set of defines and includes are stored in variables as [part of the build system](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/crossCompilationDefines.mk).
A sample of how the tool runs is found in my [_sample_ target](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/makefile#L34) of the main makefile.

# Testing
This tool has 13 test cases so far (more to be added as development progresses). The test inputs and expected outputs are found in the _test_ directory under the main OMRStatistics directory.

To run all tests and identify the failed ones, run `make test` in the main OMRStatistics directory.

# Future steps
* Run OMRStatistics over bruteclang to collect results from all architectures
* Package OMRStatistics as a command-line tool
* Consider using Doxygen as our documentation tool
