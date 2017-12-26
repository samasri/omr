![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case2.png)

For overrides:

Number | BaseNamespace | BaseClassName | BaseSignature | OverridenNamespace | OverridenClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | override | TR | A | f() | Ruby | A |
| 2 | override | Ruby | A | f() | OMR | A |
| 3 | override | Ruby | A | h() | OMR | A |
| 4 | override | TR | A | h() | Ruby | A |
| 5 | override | TR | A | h(int) | Ruby | A |

For overloads:

Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | h | h() | Overload | OMR | A |
| 3 | h | h(int) | firstOccurence | Ruby | A |
