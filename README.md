# Tusky
###### Real-time quiz application

## Code Style
### Tools
Tusky is auto-formatted using [Black](https://github.com/psf/black).

[comment]: <> (Todo: Add Flake8 to tools)

### Snapper's Style
Definitions for `__all__` should be at the top of a module, not the bottom.
This way module exports are able to be found easily without searching.

"Tall" modules are preferred over "wide" packages.
Although a verbose file structure becomes a necessity for larger projects,
I (as the developer) just prefer less files.
