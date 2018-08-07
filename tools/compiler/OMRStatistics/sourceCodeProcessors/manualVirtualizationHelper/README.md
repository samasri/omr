# Overview
The system aims to automate the virtualization of classes in OMR. It does the following:
1. Extracts the list of functions that need to be virtualized from the database query pointed to in the configuration
2. Greps for the function calls and definitions in the source code
3. Use the grep results, in addition to seaching the header files to virtualize functions

To execute the program, specify the confurations in the makefile and _processSearchResults.py_, then run `make`

# Features
* Virtualizes function definitions
* Removes `self()->` from all calls for the target functions
* Detects unimplemented functions

# Configuration:
* In processSearchResults.py
	* Target class: Class to be virtualized
	* Location of file cotaining raw list of functions
	* Location of file to write dump list of ignored functions
	* PRINT_1: Triggers MVH to print the cases described in _PRINT\_1 case_ in [Checking for unimplemented function section]()
	* PRINT_OVERLOADS: Triggers MVH to print the cases where an overload is detected
* In Makefile:
	* Location of OMR and OpenJ9 directories to read and virtualize functions
	* Location of file containig the output of the following query when run in the database:

```
SELECT DISTINCT bc.namespace, bc.classname, of.signature, oc.namespace, oc.classname
FROM Override as o
INNER JOIN Function as bf on bf.id = o.BaseFunctionID
INNER JOIN Function as of on of.id = o.overridingFunctionID
INNER JOIN Class as bc on bc.id = bf.classID
INNER JOIN Class as oc on oc.id = of.classID
WHERE bc.isExtensible = 1 and oc.isExtensible = 1 and bf.isVirtual = 0 and of.isVirtual = 0 and bf.isImplicit = 0 and of.isImplicit = 0 and bc.className='CodeGenerator';
```

# Assumptions and known unsupported cases
* Ignored functions are: overloaded functions + functions where definition is not found in source code
* OMR and J9 namespaces are hard coded in the code, changing the namespace targets means changing the code
* OMR and J9 header file paths are hard coded in the code, changing the namespace targets means changing the code. Paths like the following (including but not limited to):
	* When `runtime/compiler/codegen/` is found in the file path, it is considered the header for `J9` namesapce
	* When only `compiler/codegen/` is found in the file path, it is considered the header for `OMR` namesapce
* In OpenJ9's source code (_runtime/codegen/J9CodeGenerator.cpp_), the following statement is found `OMR::CodeGenerator::processRelocations();`. Although this does not indicate an implementation for a function, MVH considers that as an implementation.
* Cases where a function is defined in `OMR` but implemented in `J9` are not supported
* Functions are not expected to return instances of classes in the `OMR` or `J9` namespaces. For example, a function of the signature `OMR::CodeGenerator OMR::ElfRelocationResolver::resolveRelocationType()` would not be supported.

# Cases supported by MVH

## General
* Function overloads are checked in header files, if a function is defined more than once in the same file (that is, in the same class of the same namespace) it considered overloaded
* Ignored functions are printed to a file whose path is specified in the configuration

## Virtualizing functions
* If function is found in `OMR` namespace, it is only virtualized there
* If function is not found in `J9` namespace, it is not virtualized in any other `J9` subnamespace
* If a function is found in an `X86` namespace, it is not virtualized in any of that `X86` subnamespaces
* Overloaded functions, although found in the ignored function list, will have the first definition occurrence in the file where they were overloaded virtualized
* After virtualizing the definition, all calls for a function of the following form: `self()->yankIndexScalingOp()` are grepped and stored in a file. The python script searches for the grep results in the files, and removes the `self()->` occurrences. For example, when virtualizing `yankIndexScalingOp()`:
	* All `self()->yankIndexScalingOp()` are grepped in OMR and OpenJ9 directories.
	* The python script searches each line of each file in the OMR and OpenJ9 source codes for each result from grep.
	* When the result is found in a line, the result (`self()->yankIndexScalingOp()`) is replaced by `yankIndexScalingOp()` in the line.
	* After the file is done, it is rewritted with all the edited lines.
* In the above case, the python script makes sure that not all `self()->` occurrences are replaced, only `self()->` occurrences followed by the target functions. Because some cases can be as follows:
	* When trying to replace `self()->yankIndexScalingOp()`, the line might look like this: `if(self()->cond() && self()->yankIndexScalingOp()) {`. In that case, we only need to remove the right `self()` occurrence (this case is handled).


## Checking for unimplemented function
* When `//` is found, it is trimmed away from the line, so comments that are found this way are handled. That is, if a function implementation is between a `/* */` comment block, it is considered as an implemented function.
* Function implementations that span one or more lines in the header file are handled.
	* Function definition is considered to have implementation if it ends with `{`
	* Function definition is considered to not have implementation if it ends with `;`
* Function implementations in the source code are handled
	* Function implementations from source code are found by grepping for the function name prefixed by `::` (such as `::yankIndexScalingOp()`).
	* Grep results that are splitted by spaces, the part that has `OMR::` or `J9::` is considered the function call being searched for. So for example, if a function returns a class of type other than `TR`, it is not considered.
	* Function definition is considered to have implementation if it is of the following form: `OMR::X86::CodeGenerator::yankIndexScalingOp()` (last part is function name, before last part is class name, the rest is the namespace)
	* Function implementation is checked to be for the right class before considering it implemented. For instance in `OMR::X86::CodeGenerator::yankIndexScalingOp()`, the className is extracted and compared to `CodeGenerator` to make sure `yankIndexScalingOp()` belongs to the target class.
* Function is considered unimplemented if it is not implemented in neither header files nor source files.
* If a function definition is found in `OMR`, its status is not affected by finding it again in `J9`. (_PRINT\_1_ case)
	* If a function is found to be implemented in `OMR`, but then a definition is found in `J9` where there is no implementation, MVH still considers the function implemented.
	* If a function is found to be unimplemented in `OMR`, but then an implementation is found in `J9`, MVH still considers the function unimplemented.