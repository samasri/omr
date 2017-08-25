# OMR Statistics
This is a clang plugin built for clang-3.8 that runs on the source code of the file provided in the makefile and collects information about it. Listed below is each of this plugins functionalities.

# Print hierarchies
Prints out all class hierarchies in this source file (and all its includes).
## Output Format
```
<Base Class Name> --> <Parent Class Name> --> ... --> <Top Class Name>
```
## Known bug
Sometimes (in 2 cases to be exact) a class would have 2 children, which results in one of the hierarchies to be broken.
To explain when does this bug occur, consider the following 2 example hierarchies:
```c++
class A {};
class B : A {};
class C : B {};
class D : B {};
```
The hierarchies from this plugin will be as follows:
C --> B --> A
D --> B

# Print Method Information
Prints out each method in each of the class hierarchies, which classes it is overriden in, and how many times it is overloaded in each class.
## Output Format
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
