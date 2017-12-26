![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/Case1.png)

For overrides:

Number | BaseNamespace | BaseClassName | BaseSignature | OverridenNamespace | OverridenClassName | Overriding Signature |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | TR | A | f() | Ruby | A | f() |
| 2 | Ruby | A | f() | OMR | A | f() |
| 3 | Ruby | A | h() | OMR | A | h() |
| 4 | Ruby | A | h(int) | OMR | A | h(int) |
| 5 | TR | A | h() | Ruby | A | h() |
| 6 | TR | A | h(int) | Ruby | A | h(int) |

For overloads:

Number | FunctionName | FunctionSignature | Type | BaseNamespace | BaseClassName |
| --- | --- | --- | --- | --- | --- |
| 1 | f | f() | firstOccurence | OMR | A |
| 2 | h | h(int) | firstOccurence | OMR | A |
| 3 | h | h() | Overload | OMR | A |