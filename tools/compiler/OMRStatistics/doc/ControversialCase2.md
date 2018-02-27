![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case2.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ruby | A | f() | TR | A | 0 | 0 |
| 2 | OMR | A | f() | Ruby | A | 0 | 0 |
| 3 | OMR | A | h() | Ruby | A | 0 | 0 |
| 4 | Ruby | A | h() | TR | A | 0 | 0 |
| 5 | Ruby | A | h(int) | TR | A | 0 | 0 |

For overloads:

Number | FunctionName | FunctionSignature | Type | Namespace | ClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | h | h() | firstOccurence | OMR | A | 0 | 0 |
| 3 | h | h(int) | Overload | Ruby | A | 0 | 0 |
