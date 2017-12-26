![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case2.png)

For overrides:
Number | BaseNamespace | BaseClassName | BaseSignature | OverridenNamespace | OverridenClassName | Overriding Signature |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | override | TR | A | f() | Ruby | A | f() |
| 2 | override | Ruby | A | f() | OMR | A | f() |
| 3 | override | Ruby | A | h() | OMR | A | h() |
| 4 | override | TR | A | h() | Ruby | A | h() |
| 5 | override | TR | A | h(int) | Ruby | A | h(int) |

For overloads:
Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | h | h() | Overload | OMR | A |
| 3 | h | h(int) | firstOccurence | Ruby | A |