"""
Pdbe functionality and implementation.
"""
from os import fdopen
from tempfile import mkstemp

# pylint:disable=no-name-in-module
from utils import (
    change_files_data,
    does_line_contains_import_pdb,
    get_import_pdb_line_st_spaces,
    get_function_indent,
    is_commended_function,
    is_function_sign_in_line,
    IMPORT_PDB_LINE,
)


def put_import_pdb(file_path: str) -> None:
    """
    Put import pdb statement.

    It needs to be placed after function declaration.
    """
    fh, abs_path = mkstemp()  # pylint:disable=invalid-name

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if is_function_sign_in_line(line) and not is_commended_function(line):
                    indents_space_count = get_function_indent(line)
                    import_pdb_line_begging_spaces = get_import_pdb_line_st_spaces(indents_space_count)
                    new_file.write(line + import_pdb_line_begging_spaces + IMPORT_PDB_LINE)
                else:
                    new_file.write(line)

    change_files_data(file_path, abs_path)


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

    change_files_data(file_path, abs_path)
