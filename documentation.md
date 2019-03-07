Copyright (C) Codeplay Software Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

For your convenience, a copy of the License has been included in this
repository.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# Python Generator Tools (py_gen)

## Introduction

py_gen is a small library for generating code based on the python itertools
library. It provides an interface for generating strings and writing to files
using string template inputs. A set of custom objects are used to generate
groups of data and methods of iterating over them to insert them into templates.

## Interface

The interface is contained across two files in the root of py_gen.
* `interface.py`
* `iter_classes.py`


Using the interface provided by either of the methods `generate_source` or
`generate_file`, the generator tools can be invoked to create large amounts of
generated code. The generators run using the python itertools modules
[combinatoric generators](https://docs.python.org/2/library/itertools.html).

The interface provided requires the use of three classes, `Itermode`,
`Iterable`, and `IterGroup`, contained in `iter_classes.py`.

Both interfaces take an input to modify, either a file name to read from/write
to or a string to modify. They then take a list of `IterGroup` objects in the
parameter `iter_groups`.

An `IterGroup` is constructed with and contains `insertion_point`, `template`,
a list of `Iterable` objects, and a True/False flag denoting if the `Iterable`
is to be processed as a standard or combined `IterGroup`.

`insertion_point` is a string in the input which will be replaced by
generated code in the resulting output.

For example
```python
insertion_points = 'IP1'
```

`template` is a
[string Template](https://docs.python.org/2/library/string.html#template-strings)
with `${}` substitution keys to be filled with data from `Iterable`s.

For example
```python
template = Template('${key0} some text ${key1}')
```
`iterables` is a list of lists of `Iterable` objects which contain the key they
will replace, a list of values for input to a combinatoric generator, an
`Itermode` value to specify a combinatoric generator, and a modifier value.

For example
```python
iterables = [[Iterable(key='key0', vals=['a', 'b'],
                       itermode=Itermode.combinationsWR, iter_modifier=2),
              Iterable(key='key1', vals=['a'],
                      itermode=Itermode.product, iter_modifier=2)],
             [Iterable(key='key0', vals=['a', 'b', 'c'],
                       itermode=Itermode.combinations, itermodifier=3)]
```
Iterables can also be instructed to generate comma separated lists rather than
compacted ones.

For example
```python
non_comma_iter = Iterable(key='key0', vals=['a', 'b', 'c'],
                    itermode=Itermode.combinations, iter_modifier=2)
comma_iter = Iterable(key='key0', vals=['a', 'b', 'c'],
                    itermode=Itermode.combinations, iter_modifier=2,
                    comma_list=true)

# non_comma_iter   -> 'ab','ac','bc'
# comma_iter -> 'a, b', 'a, c', 'b, c'

```


These three structures map to each other as so
```python
[       'IP1',                                   'IP2']
          |                                        |
[     Template('${key0}...${key1}'),           Template('${key0}...')]
                 /             \                            |
[[Iterable(key='key0'...), Iterable(key='key1'...)], [Iterable(key='key0'...)]]
```


As an example, the following inputs
```python
source = 'Line one\n  @ip1@\n    @ip2@\nEnding line'
iter_groups = [IterGroup('@ip1@', Template('a ${key0}\n  ${key1}\nb'),
               [Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2),
                Iterable('key1', ['d', 'e'], Itermode.combinationsWR, 3)]),
               IterGroup('@ip2', Template('    1 ${key2}${key3}\n'),
                [Iterable('key2', ['1 2', '3'], Itermode.permutations, 2),
                 Iterable('key3', ['xyzw'], Itermode.product, 3)])]
```
will produce the output string
```
Line one
  a ab
    ddd
  ba ac
    ddd
  ba bc
    ddd
  ba ab
    dde
  ba ac
    dde
  ba bc
    dde
  ba ab
    dee
  ba ac
    dee
  ba bc
    dee
  ba ab
    eee
  ba ac
    eee
  ba bc
    eee
  b
        1 1 23xyzwxyzwxyzw
        1 31 2xyzwxyzwxyzw

Ending line
```

`IterGroup`s can be processed in two ways; combined, in which each `Iterable`
will be processed in parallel, and uncombined, in which each `Iterable` will be
fully exhausted before the next is processed.

When processed as a combined `IterGroup`, each `Iterable` in the group must
produce the same number of outputs. These outputs are inserted into the template
together. For example

```python
source = '@ip1@'
iter_groups = [IterGroup('@ip1@', Template('${key0}  ${key1}  |\n'),
               [Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2,
                         True),
                Iterable('key1', ['3', '2', '1'], Itermode.combinations, 2)],
               combine_iters = True)]
```
will produce the output string
```
a, b  32  |
a, c  31  |
b, c  21  |
```

A second type of `IterGroup` is provided for more specialized situations. The
`RemovalIterGroup` takes two lists of `Iterable`s. The `RemovalIterGroup` works
in the same manner as a normal `IterGroup` and can be used in combined and
standard output modes. The only difference is during generation, any output
created by the second list of `Iterable`s will not be included in the output
generated by the first list. In the case of combined output, if any output from
the first list in a combination is also present in the outputs of the second
list, the entire combination will be ignored.

To demonstrate

```python
source = '@ip1@'
iter_groups = [RemovalIterGroup('@ip1@', Template('${key0}  ${key1}  |\n'),
               [Iterable('key0', ['a', 'b', 'c'], Itermode.combinations, 2,
                         True),
                Iterable('key1', ['3', '2', '1'], Itermode.combinations, 2)],
               [Iterable('', ['a', 'b'], Itermode.combinations, 2)],
               combine_iters = True)]
```
will produce
```
a, c  31  |
b, c  21  |
```
Because 'a, b' was generated by the second list of iterables, the entire
output 'a, b  32  |\n' was ignored during generation.


The `generate_source` interface will take the source to modify as a string, and
return the generated result.

The `generate_file` interface takes two filenames and a list of `iter_group`s.
The first filename should be the input file with `insertion_points`, and the
second will be the file written by the generators. `generate_file` will also
return the written file as a string.

Each time `generate_file` is called the output will also be formatted if
`format_generated`  is set to True. The file will be formatted by calling the
script given by `format_script` with the output file as its argument.
Formatting is disabled by default for safety.

The template file will not be written to at any point, only read.

## Itermodes

### combinations

The `combinations` `Itermode` produces unique sequences of elements from the
input values. Elements are treated as unique based on their position in the
input, not on their value. The `iter_modifier` denotes the length, in values
from the `Iterable`, of each sequence. Individual elements from the input may
not be repeated in an output, and no output can match another in unsorted
contents.





#### Examples

```python
Iterable('key', ['a', 'b'], Itermode.combinations, 1)
-->
['a', 'b']

Iterable('key', ['a', 'b'], Itermode.combinations, 2)
-->
['ab']

Iterable('key', ['a', 'b', 'c'], Itermode.combinations, 2)
-->
['ab', 'ac', 'bc']
```


### combinationsWR

The `combinationsWR` `Itermode` produces unique sequences of elements from the
input values. Elements are treated as unique based on their position in the
input, not on their value. The `iter_modifier` denotes the length, in values
from the `Iterable`, of each subsequence. Individual elements from the input may
be repeated in an output, and no output can match another in unsorted contents.

#### Examples

```python
Iterable('key', ['a', 'b'], Itermode.combinationsWR, 1)
-->
['a', 'b']

Iterable('key', ['a', 'b'], Itermode.combinationsWR, 2)
-->
['aa', 'ab', 'bb']

Iterable('key', ['a', 'b', 'c'], Itermode.combinationsWR, 2)
-->
['aa', 'ab', 'ac', 'bb', 'bc', 'cc']
```


### permutations

The `permutations` `Itermode` produces unique sequences of elements from the
input values. Elements are treated as unique based on their position in the
input, not on their value. The `iter_modifier` denotes the length, in values
from the `Iterable`, of the sequence. Individual elements from the input may not
be repeated in an output, but an output can match another output in unsorted
contents.

#### Examples

```python
Iterable('key', ['a', 'b'], Itermode.permutations, 1)
-->
['a', 'b']

Iterable('key', ['a', 'b'], Itermode.permutations, 2)
-->
['ab', 'ba']

Iterable('key', ['a', 'b', 'c'], Itermode.permutations, 2)
-->
['ab', 'ac', 'ba', 'bc', 'ca', 'cb']
```


### product

The `product` `Itermode` produces the Cartesian product of the input, equivalent
to nested for-loops. The `iter_modifier` denotes the length, in values from the
`Iterable`, of each output.

#### Examples

```python
Iterable('key', ['a', 'b'], Itermode.product, 1)
-->
['a', 'b']

Iterable('key', ['a', 'b'], Itermode.product, 2)
-->
['aa', 'ab', 'ba', 'bb']

Iterable('key', ['a', 'b', 'c',], Itermode.product, 2)
-->
['aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']
```

## Backend

The interface links to a backend built in two parts. A combinatoric
dispatcher/generator and a set of utility methods for string manipulation and
file IO.

`internal/iters.py` contains the dispatcher and generator functions called by
it. These are responsible for checking an `Iterable`'s `Itermode` and calling
the appropriate combinatoric generator provided by the python library itertools.
The dispatcher will iterate through one `Iterables` list at a time, generating
strings each iteration with the string `Template`. Once finished, it will
return a new `Template` with the generated string.

The insertion methods will add spacing to each generated line to keep the
inserted string at equal indentation to the replaced insertion point. The output
file (`file_name`) won't be written to until all of the generation has taken
place. If generation fails part way through, no output will be produced.

## Testing

The py_gen module should be tested by importing the module and running the
testing methods. Testing has been run on both python 2.7 and 3.5+. An output
similar to the following should be seen when testing.

```
>>> import py_gen
>>> py_gen.run_all_tests()
......
----------------------------------------------------------------------
Ran 6 tests in 0.012s

OK
......
----------------------------------------------------------------------
Ran 6 tests in 0.006s

OK
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
.............
----------------------------------------------------------------------
Ran 13 tests in 0.001s

OK
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK

```

The test suite covers every `Itermode`, interface function, internal function,
and file reading/writing. If clang-format is not available with which to perform
formatting tests, some failures will be seen.
