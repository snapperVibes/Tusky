# Tusky
###### Real-time quiz application

<!-- 😅 <a href="http://vanilla-js.com/"><img alt="Vanilla JS" src=http://vanilla-js.com/assets/button.png></a> -->
## Style
### Core Table
  - Primary key is identity (`id = ID()`)
  - The class name is singular PascalCase*.
  - The \_\_tablename__ is plural snake_case*.
  - Each column has the equal-sign lined up a single space after the longest column name.
  - Columns and `__tablename__` only line up coincidentally.

### Lookup Table
TODO: Naming schema
  - Primary key is foreign key to core table

### Linking Tables
Style|Class Name|\_\_tablename__
---|---|---
One to Many|`LinkThingToThings`|`"link_thing_to_things"`

### Vertical-Line Breaks
Variables may have 0 or 1 line breaks.
Multi-line functions and classes are required to have line breaks, except if they are part of a class, in which case they have 1 line break.
Single-line functions may lumped as a block with Go FMT style spacing.
