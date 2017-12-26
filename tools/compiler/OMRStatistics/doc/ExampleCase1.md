![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case1.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | TR | A | f() | Ruby | A |
| 2 | Ruby | A | f() | OMR | A |
| 3 | Ruby | A | h() | OMR | A |
| 4 | Ruby | A | h(int) | OMR | A |
| 5 | TR | A | h() | Ruby | A |
| 6 | TR | A | h(int) | Ruby | A |

For overloads:

Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | h | h(int) | firstOccurence | OMR | A |
| 3 | h | h() | Overload | OMR | A |
