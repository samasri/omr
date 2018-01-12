![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case2.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | Ruby | A | f() | TR | A |
| 2 | OMR | A | f() | Ruby | A |
| 3 | OMR | A | h() | Ruby | A |
| 4 | Ruby | A | h() | TR | A |
| 5 | Ruby | A | h(int) | TR | A |

For overloads:

Number | FunctionName | FunctionSignature | Type | Namespace | ClassName |
| --- | --- | --- | --- | --- | --- |
| 2 | h | h() | firstOccurence | OMR | A |
| 3 | h | h(int) | Overload | Ruby | A |
