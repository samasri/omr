![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case3.png)

For overrides:

Number | BaseNamespace | BaseClassName | BaseSignature | OverridenNamespace | OverridenClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | override | Ruby | A | f() | OMR | A |
| 2 | override | Ruby | A | h() | OMR | A |
| 3 | override | TR | A | h(int) | OMR | A |
| 4 | override | TR | A | h() | Ruby | A |

For overloads:

Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | f | f(int) | Overload | TR | A |
| 3 | h | h(int) | firstOccurence | OMR | A |
| 4 | h | h() | Overload | OMR | A |
