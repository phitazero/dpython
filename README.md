# dpython

A shell for the Python interpreter for easier JSON/dict object logging

## Usage:

Replace PYTHON_EXECUTABLE in the code with the path to your Python binary, or just the executable name, if it's in PATH

Then either use `python <path to dpython.py> <path to code>` or build `dpython.py` into an executable and use `./dpython <path to code>`

You can use special #-prefixed expressions in your code.
These will be interpreted as comments by regular Python, but as directives by dpython.

### Directives:

**Note: only one directive capturing stdout can be used at a time**

`# $ =>`  
All print()'ed dicts and lists will be serialized to JSON and printed  
**Blocks all other directives, printing to stdout!**

`# $ => [file]`  
All print()'ed dicts and lists will be serialized to JSON and written into \[file].json, overwriting it, or creating it, if doesn't exist

`# $ =>> [file]`  
All print()'ed dicts and lists will be serialized to JSON and appended to \[file].json, raising an exception if it doesn't exist

`# [var] =>`  
\[var] will be serialized to JSON and printed

`# [var] => [file]`  
\[var] will be serialized to JSON and written into \[file].json, overwriting it, or creating it, if doesn't exist

`# [var] =>> [file]`  
\[var] will be serialized to JSON and appended to \[file].json, raising an exception if it doesn't exist

`# => [file]`  
\[file].json will be cleared or created, if doesn't exist