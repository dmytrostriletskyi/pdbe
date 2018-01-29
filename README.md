# pdbe

Your favorite debugger to everywhere!

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/acg.svg)](https://github.com/dmytrostriletskyi/acg/releases)
![Build](https://api.travis-ci.org/dmytrostriletskyi/pdbe.svg?branch=develop)
![Python3](https://img.shields.io/badge/Python-3.5-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

## Getting started

### What is pdbe

`pdbe` put import pdb statement `import pdb; pdb.set_trace()` in specified python's file, files in directory and
nested files in directory.

### Motivation

There could be a situations, when you need to debug project for knowing how it works, so put import pdb statement with
`pdbe` tools, run this project and handle any moves you do in.

### How to install

```
$ pip3 install pdbe
```

## Examples

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

Flag `--ew` instead of `--dir` allows you to put import pdb statement into all python files in all nested directories.

### Advanced

`pdbe` provides some commands, that seems like git's arsenal.

First of all, you can commit changes (in our case it is import pdb statements only) with following command:

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

Remember, all history of commits and it's data stored in hided folder called `.pdbe`, so
do not forget put to your `.girignore` following line `.pdbe/`.

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
