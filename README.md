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

[Errors are values](https://go-proverbs.github.io/), and exceptions should be exceptional.
Sadly, Python was written before this mantra took to the mainstream.
However, I fully believe that Python wouldn't have catchable exceptions if it were written today.
After all, [explicit is better than implicit](https://www.python.org/dev/peps/pep-0020/#id2).
