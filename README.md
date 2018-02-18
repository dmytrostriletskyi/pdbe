# pdbe

Your favorite debugger to everywhere!

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/pdbe.svg)](https://github.com/dmytrostriletskyi/pdbe/releases)
![Build](https://api.travis-ci.org/dmytrostriletskyi/pdbe.svg?branch=develop)
![Python3](https://img.shields.io/badge/Python-3.5-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

[![Medium](https://img.shields.io/badge/Post-Medium-brightgreen.svg)](https://medium.com/@dmytrostriletskyi/https-medium-com-dmytrostriletskyi-pdbe-a-feature-for-internal-python-debugger-7081f589bcbb)
[![Habrahabr](https://img.shields.io/badge/Post-Habrahabr-brightgreen.svg)](https://habrahabr.ru/post/348376/)

## Getting started

### What is pdbe

`pdbe` puts import pdb statement `import pdb; pdb.set_trace()` in specified python's file, files in directory and
nested files in directory (files in directory, that located in another directory with files also).

### Motivation

There could be a situations, when you need to debug project (i.e. super old framework with millions of code lines) for knowing how it works. So put import pdb statement with `pdbe` tools, run this project and handle any bunch of code.

### How to install

```
$ pip3 install pdbe
```

## Usage

### Common usage

Import pdb statements into particular file:

```
$ pdbe --file path/to/file.py
```

As result you will see:

```python
def first_function():
    import pdb; pdb.set_trace()
    ...

def second_function():
    import pdb; pdb.set_trace()
    ...

    def third_function():
        import pdb; pdb.set_trace()
        ...
```

Remove pdb statement from that file with:

```
$ pdbe --file path/to/file.py --clear
```

The same works with files in directories:

```
$ pdbe --dir path/to/dir-with-python-files
```

And clear:

```
$ pdbe --dir path/to/dir-with-python-files --clear
```

Flag `--ew` instead of `--dir` allows you to put import pdb statement into all python files in all directories (nested from specified).

### Advanced usage

`pdbe` provides some commands, that seems like git's arsenal.

First of all, you can commit (save to ususing in future) state of import pdb statements:

```
$ pdbe --commit 'Commit message'
```

Then you are able to see logs (all logs of commits you did in your dev-history):

```
$ pdbe --log
```

The result will be something like that:

```
commit  | add336b6a204bb7b3abe76c296b67f92
date    | 23:17:00 29-01-2018
message | Commit message
```

And the final point is a `checkout` command, that can restore changes, that were bind to your commit:

```
$ pdbe --checkout add336b6a204bb7b3abe76c296b67f92
```

You are able to write not less 5 symbols of commit number (SHA).

### Advanced flow example

To clearify how it works, imagine that you wrote `pdbe --file path/to/file.py`:

```python
def first_function():
    import pdb; pdb.set_trace()
    ...

def second_function():
    import pdb; pdb.set_trace()
    ...

    def third_function():
        import pdb; pdb.set_trace()
        ...
```

That commited state of imports with:

```
$ pdbe --commit 'Commit message'
```

Next step is a clearing imports:

```
$ pdbe --file path/to/file.py --clear
```

```python
def first_function():
    ...

def second_function():
    ...

    def third_function():
        ...
```

And now you do not need remember which file you did debug (you could go to the lunch) and put imports again.

Take a look at logs:

```
commit  | add336b6a204bb7b3abe76c296b67f92
date    | 23:17:00 29-01-2018
message | Commit message
```

And restore it with `checkout` command:

```
$ pdbe --checkout add336b6a204bb7b3abe76c296b67f92
```

Remember, all history of commits and it's data stored in hided folder called `.pdbe`, so
do not forget put following line `.pdbe/` to your `.gitignore`.

## Configuration file

`Pdbe` supports a configurations. Configurations have the following view.

```
debugger=ipdb
ignore=migrations,fixtures,setup.py
#ignore=contributions,test_view.py
```

To use the configuration file, create a file called `.pdberc` within home directory (`cd ~`).
And for now there are two points are supported:

1. `debugger` to set `ipdb` (only `ipdb` is supported for now).
2. `ignore` to set directories (files in this directory will never be handled by pdbe) and files. Use `,` symbol to separate content of this setting.

Also you are able to comment configuration line with `#` symbol.

## Development

Install packages, that needed for testing:

```
$ pip3 install requirements-dev.txt
```

Run tests before development to be sure pdbe works properly:

```
$ python -m unittest discover tests
```

Follow codestyle with linters:

```
$ flake8 pdbe && pycodestyle pdbe && pylint pdbe
```
