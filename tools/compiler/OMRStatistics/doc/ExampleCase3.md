![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case3.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | OMR | A | f() | Ruby | A |
| 2 | OMR | A | h() | Ruby | A |
| 3 | OMR | A | h(int) | TR | A |
| 4 | Ruby | A | h() | TR | A |

For overloads:

Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | f | f(int) | Overload | TR | A |
| 3 | h | h(int) | firstOccurence | OMR | A |
| 4 | h | h() | Overload | OMR | A |
