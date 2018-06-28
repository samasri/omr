This directory contains progress about virtualized functions in OMR. Each md file in this directory is named after a hierarchy name; it includes a table of all overridden functions and whether they are virtualized or not yet.

The script used to get these results can be found [here](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/sourceCodeProcessors/getSignaturesToOverride.py)

The table follows the following format:

| Signature | First occurrence of function in hierarchy (starting the search from base class) | isVirtualized |
| --- | --- | --- |