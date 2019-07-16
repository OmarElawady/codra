# Codra

Codra is a template engine written in python to render a string given its template and the data to fill this template
## Installation

`pip install codra`

## Example

```python
from codra import Template
template = r"""
Hello my name is {{ name }}. I am {{ age }} years old.
This is the activities I do:
{{ for i, activity in enumerate(activities) }}
  {{ i }}. {{ activity }}
{{ endfor}}
Those are the type of numbers less than 20
{{ for i in range(20) }}
  {{ if is_prime(i) }}
    {{i}} is prime.
  {{ endif }}
  {{ if not is_prime(i) }}
    {{i}} is not prime.
  {{ endif}}
{{ endfor}}
"""
def is_prime(n):
  if n < 2:
    return False
  elif n == 2:
    return False
  else:
    for i in range(2, n):
      if n % i == 0:
        return False
    return True

print(Template(template).render(name = "Alice", age = 20, activities = ["coding", "playing", "eating"], is_prime = is_prime, enumerate = enumerate))
```

## Format

The template consists mainly of data and executable sections which may be interleaved with each other. The executable sections is surrounded by double curly braces. `{{` can be escaped by preceding it with backslash. 

The executable sections (from now on called constructs) is divided into three types:

	1. Expressions.
	2. If conditions.
	3. For loops.

The constructs are eventually replaced by text after rendering. Since expressions might contain identifiers and function calls, they're supplied in kwargs to the render function with the names that appear iniside the template.

## Language constructs

In this section, the different language constructs is covered in more details.

### Expressions

Expressions in codra can be considered as a subset of the expressions in python. It's worth noting that the semantic analysis is based on that of python. The expressions is parsed and computed using the corresponding construct in python. That might explain a lot of the behaviour of the templare engine.

#### Literals

String literals are surrounded by either single quotation marks, or double quotation marks.

_Example_:

`'hello world'`

Numeric literals is any consecutive digits (only Integers is supported for now). Despite the fact that only integers is supported as literals, the result of any expression can be either integer of float.

`1984`

Boolean literals is planned to be added with the case sensitive keywords True and False.

#### Arithmetic operators

The operators `+`, `-`, `/`, `*` and `%` have the same semantic meaning as they do in python. Which means that `+` can be used also to concatanate strings.

_Example_:

`1 + 2 * 6 / 4 % 5` evaluates to 4

#### Comparison operators

You can use `==`, `!=` to check for equality and `<`, `<=`, `>` and '>=` to compare different expressions

`1 < 4` is True

#### Logical operators

`and`, `or and `not` can be used to combine the result of comparison expressions.

_Example_:

`1 == 2 or not 3 == 4` evaluates to `True`

#### Access operators

Access operators are used to fetch the value from an object or a dictionary. 

`.` is used to access class members of an object.

`[]` is used to get the value associated with a key in a dict.

_Example_:

`person.favorite_food['morning']`

#### Function calls

The built in functions `len` and `range` is supplied by default. To use another functions they must be supplied in the arguments of render. To call a function use its name along with a list of possibly empty parameters separated by `,` and enclosed in parentheses.

_Example_:

`Template("{{ is_odd(1) }}").render(is_odd = lambda x : x % 2 == 1)` evaluates to `"True"`

### If conditions

If conditions are used to print the enclosing data only if the expression evaluates to True:

The Syntax of if condition is:

```python
{{ if _condition_ }}
_body_
{{ endif }}
```
The body of the if can be any valid template (data, constructs or both). The if construct evaluates to its body if the condition is True, Otherwise, it's replaced by an empty string.

_Example_:

```python
Template("""
This is a condition to greet Alice only.
{{ if name == "Alice" }}
Hello {{ name }}.
{{ endif }}
""").render(name = "Alice")
```

this evaluates to:

```python
"""
This is condition to greet Alice only.

Hello Alice.

"""
```

### For loops

Loops can be used to iterate over any iterable python object (e.g. lists).

Loops can have one or more variables. It's translated by assigning the variable(s) to each item in the given iterable and evaluating the body of the loop. Then the result of each iteration is combined into a single unit.

_Examples_:

```python
Template("""
{{ for i in range(len(lst)) }}
{{i + 1}}. {{ lst[i] }}
{{ endfor }}
""").render(lst = ['a', 'b', 'c'])
```
which is equivalent to:

```python
Template("""
{{ for i, e in enumerate(lst) }}
{{i + 1}}. {{ e }}
{{ endfor }}
""").render(lst = ['a', 'b', 'c'], enumerate = enumerate)
```

evaluates to:

```python
"""

1. a

2. b

3. c

"""
```

