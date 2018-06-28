This directory contains progress about virtualized functions in OMR. Each md file in this directory is named after a hierarchy name; it includes a table of all overridden functions and whether they are virtualized or not yet.

The overridden functions are subject to the following constraints:
* The host classes are extensible
* The functions are not virtual
* The functions are not implicit

The script used to get these results can be found [here](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/sourceCodeProcessors/getSignaturesToOverride.py)

The table follows the following format:

| Signature | First occurrence of function in hierarchy (starting the search from base class) | isVirtualized |
| --- | --- | --- |