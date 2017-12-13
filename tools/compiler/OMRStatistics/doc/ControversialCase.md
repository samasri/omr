![Class Hierarchy](https://github.com/samasri/omr/blob/master/tools/compiler/OMRStatistics/doc/resources/ExampleUML2.png)

Number | Type | Base Namespace | Base ClassName | Base Signature | Overloaded/Overriden Namespace | Overloaded/Overriden ClassName | Overriding Signature |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | override | TR | A | f() | Ruby | A | f() |
| 2 | override | Ruby | A | f() | OMR | A | f() |
| 3 | overload | OMR | A | h() | OMR | A | h(int) |
| 4 | override | OMR | A | h() | Ruby | A | h() |
| 5 | ~~overload~~ | ~~OMR~~ | ~~A~~ | ~~h(int)~~ | ~~Ruby~~ | ~~A~~ | ~~h()~~ |
| 6 | override | OMR | A | h() | Ruby | A | h() |
| 7 | ~~overload~~ | ~~OMR~~ | ~~A~~ | ~~h(int)~~ | ~~Ruby~~ | ~~A~~ | ~~h()~~ |
| 8 | override | OMR | A | h(int) | Ruby | A | h(int) |
| 9 | ~~overload~~ | ~~OMR~~ | ~~A~~ | ~~h()~~ | ~~Ruby~~ | ~~A~~ | ~~h(int)~~ |

Our suggestion in this case to keep record #3 and remove records #5, 7, 9.

| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | override | TR | A | f() | Ruby | A | f() |
| 2 | override | Ruby | A | f() | OMR | A | f() |
| 3 | overload | OMR | A | h() | OMR | A | h(int) |
| 4 | override | Ruby | A | h() | OMR | A | h() |
| 5 | ~~overload~~ | ~~OMR~~ | ~~A~~ | ~~h(int)~~ | ~~Ruby~~ | ~~A~~ | ~~h()~~ |
| 6 | override | TR | A | h() | Ruby | A | h() |
| 7 | ~~overload~~ | ~~TR~~ | ~~A~~ | ~~h()~~ | ~~OMR~~ | ~~A~~ | ~~h(int)~~ |
| 8 | override | TR | A | h(int) | OMR | A | h(int) |
| 7 | ~~overload~~ | ~~TR~~ | ~~A~~ | ~~h(int)~~ | ~~Ruby~~ | ~~A~~ | ~~h()~~ |
| 9 | ~~overload~~ | ~~TR~~ | ~~A~~ | ~~h(int)~~ | ~~OMR~~ | ~~A~~ | ~~h()~~ |
