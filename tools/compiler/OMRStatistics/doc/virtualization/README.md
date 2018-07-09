This directory contains progress about virtualized functions in OMR. Each md file in this directory is named after a hierarchy name; it includes a list of all virtualized functions. The file also includes functions that are declared pure virtual (since they would have no implementation) and functions that are provided with default implementation.

The overridden functions are subject to the following constraints:
* The host classes are extensible
* The functions are not virtual
* The functions are not implicit

The script used to get these results can be found [here](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/sourceCodeProcessors/getSignaturesToOverride.py)