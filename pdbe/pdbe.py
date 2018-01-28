"""
pdbe functionality and implementation.
"""
from os import fdopen, remove
from shutil import move
from tempfile import mkstemp

IMPORT_PDB_LINE = 'import pdb; pdb.set_trace()\n'


def is_function_sign_in_line(line: str) -> bool:
    """
    Check if line contains function declaration.
    """
    return 'def ' in line and '(' in line and '):' in line or ') ->' in line


def does_line_contains_import_pdb(line: str) -> bool:
    """
    Check if line contains import pdb statement.
    """
    return 'import pdb; pdb.set_trace()' in line


def get_function_indent(line: str) -> int:
    """
    Get function indents from begging of the file.
    """
    first_function_entrance = line.index('def')
    indents = line[:first_function_entrance]
    indents_space_count = len(indents)
    return indents_space_count


def get_import_pdb_line_st_spaces(indents_space_count: int) -> str:
    """
    Get string, that length is bigger than function declaration by 4.
    """
    next_statement_indents_count = 4
    return ' ' * (indents_space_count + next_statement_indents_count)


def formatted_to_pdb_statement_line(line: str) -> str:
    """
    Add string of import pdb statement below function with properly indents.
    """
    indents_space_count = get_function_indent(line)
    import_pdb_line_begging_spaces = get_import_pdb_line_st_spaces(indents_space_count)
    return line + import_pdb_line_begging_spaces + IMPORT_PDB_LINE


def put_import_pdb(file_path: str) -> None:
    """
    Put import pdb statement.

    It needs to be placed after function declaration.
    """
    fh, abs_path = mkstemp()  # pylint:disable=invalid-name

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if is_function_sign_in_line(line):
                    formatted_line = formatted_to_pdb_statement_line(line)
                    new_file.write(formatted_line)
                else:
                    new_file.write(line)

    remove(file_path)
    move(abs_path, file_path)


def remove_import_pdb(file_path: str) -> None:
    """
    Remove import pdb statement.
    """
    fh, abs_path = mkstemp()  # pylint:disable=invalid-name

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if not does_line_contains_import_pdb(line):
                    new_file.write(line)

    remove(file_path)
    move(abs_path, file_path)
