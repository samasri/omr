![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case1.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Ruby | A | f() | TR | A | 0 | 0 |
| 2 | OMR | A | f() | Ruby | A | 0 | 0 |
| 3 | OMR | A | h() | Ruby | A | 0 | 0 |
| 4 | OMR | A | h(int) | Ruby | A | 0 | 0 |
| 5 | Ruby | A | h() | TR | A | 0 | 0 |
| 6 | Ruby | A | h(int) | TR | A | 0 | 0 |

For overloads:

Number | FunctionName | FunctionSignature | Type | Namespace | ClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | h | h(int) | firstOccurence | OMR | A | 0 | 0 |
| 3 | h | h() | Overload | OMR | A | 0 | 0 |
