"""
Pdbe functionality and implementation.
"""
from os import fdopen
from tempfile import mkstemp

try:
    import utils
# pylint:disable=bare-except
except:  # Python 3.5 does not contain `ModuleNotFoundError`
    from pdbe import utils


def put_import_pdb(file_path: str) -> None:
    """
    Put import pdb statement.

    It needs to be placed after function declaration.
    """
    fh, abs_path = mkstemp()  # pylint:disable=invalid-name

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            if utils.check_if_file_is_ignored(old_file.name):
                return

            # for multiple function declaration
            import_pdb_statement_to_write = ''
            multiple_function_declaration_begging_spaces = ''

            for line in old_file:
                if multiple_function_declaration_begging_spaces:
                    if 'def' not in line and '):' in line:
                        import_pdb_line_begging_spaces = multiple_function_declaration_begging_spaces
                        import_pdb_statement_to_write = import_pdb_line_begging_spaces + utils.IMPORT_PDB_LINE
                        multiple_function_declaration_begging_spaces = ''

                if utils.is_one_line_function_declaration_line(line) and not utils.is_commended_function(line):
                    indents_space_count = utils.get_function_indent(line)
                    import_pdb_line_begging_spaces = utils.get_import_pdb_line_st_spaces(indents_space_count)
                    new_file.write(line + import_pdb_line_begging_spaces + utils.IMPORT_PDB_LINE)

                else:
                    if 'def' in line and not utils.is_commended_function(line):
                        indents_space_count = utils.get_function_indent(line)
                        multiple_function_declaration_begging_spaces = utils.get_import_pdb_line_st_spaces(
                            indents_space_count
                        )

                    new_file.write(line)

                if import_pdb_statement_to_write:
                    new_file.write(import_pdb_statement_to_write)
                    import_pdb_statement_to_write = ''

    utils.change_files_data(file_path, abs_path)


def remove_import_pdb(file_path: str) -> None:
    """
    Remove import pdb statement.
    """
    fh, abs_path = mkstemp()  # pylint:disable=invalid-name

    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if not utils.does_line_contains_import_pdb(line):
                    new_file.write(line)

    utils.change_files_data(file_path, abs_path)
