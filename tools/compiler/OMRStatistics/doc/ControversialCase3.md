![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case3.png)

For overrides:

Number | BaseNamespace | BaseClassName | Signature | OverridingNamespace | OverridingClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | OMR | A | f() | Ruby | A | 0 | 0 |
| 2 | OMR | A | h() | Ruby | A | 0 | 0 |
| 3 | OMR | A | h(int) | TR | A | 0 | 0 |
| 4 | Ruby | A | h() | TR | A | 0 | 0 |

For overloads:

Number | FunctionName | FunctionSignature | Type | Namespace | ClassName | isImplicit | isVirtual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A | 0 | 0 |
| 2 | f | f(int) | Overload | TR | A | 0 | 0 |
| 3 | h | h(int) | firstOccurence | OMR | A | 0 | 0 |
| 4 | h | h() | Overload | OMR | A | 0 | 0 |
