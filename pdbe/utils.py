"""
Pdbe utils.
"""
from os import remove
from os.path import expanduser, exists
from shutil import move


def read_confs():
    """
    Read configuration file called `.pdberc`.
    """
    debugger = 'import pdb; pdb.set_trace()\n'
    ignore = []

    home = expanduser('~')
    pdberc = home + '/.pdberc'

    confs = {}

    if not exists(pdberc):
        return {
            'debugger': debugger,
            'ignore': ignore,
        }

    with open(pdberc, 'r') as file:
        content = [line.strip() for line in file.readlines()]

    for line in content:
        if '=' in line and line.strip()[0] != '#':
            key, value = line.split('=')
            confs[key] = value

    if 'debugger' in confs:
        if confs['debugger'] == 'ipdb':
            debugger = 'import ipdb; ipdb.set_trace()\n'

    if 'ignore' in confs:
        ignore = confs['ignore'].split(',')

    result = {
        'debugger': debugger,
        'ignore': ignore,
    }

    return result


IMPORT_PDB_LINE = read_confs()['debugger']
INGORED_PATHS = read_confs()['ignore']
LINE_FEED = '\n'


def is_one_line_function_declaration_line(line: str) -> bool:  # pylint:disable=invalid-name
    """
    Check if line contains function declaration.
    """
    return 'def ' in line and '(' in line and '):' in line or ') ->' in line


def does_line_contains_import_pdb(line: str) -> bool:
    """
    Check if line contains import pdb statement.
    """
    return IMPORT_PDB_LINE.strip().split() == line.split()


def is_commended_function(line: str) -> bool:
    """
    Check if function is commended.
    """
    return line.strip()[0] == '#'


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


# pylint:disable=invalid-name
def get_import_pdb_line_begging_spaces(line: str) -> str:
    """
    Return string, that length equals to function indents plus 4.
    """
    indents_space_count = get_function_indent(line)
    import_pdb_line_begging_spaces = get_import_pdb_line_st_spaces(indents_space_count)
    return import_pdb_line_begging_spaces


def get_project_call_cwd(call_commit_path: str, file_path: str) -> str:
    """
    Get static project path.
    """
    symbols_to_equal_paths = ' ' * (len(file_path) - len(call_commit_path))

    # pylint:disable=invalid-name
    call_commit_path_with_static_length = call_commit_path + symbols_to_equal_paths

    project_call_cwd = ''

    for relative, static in zip(call_commit_path_with_static_length, file_path):
        if relative != static:
            project_call_cwd += static

    return project_call_cwd


def change_files_data(file_path: str, abs_path: str) -> None:
    """
    Change files data.
    """
    remove(file_path)
    move(abs_path, file_path)


def check_if_file_is_ignored(file_path):
    """
    Check if file path is ignored.
    """
    path_parts = file_path.split('/')

    for part in path_parts:
        if part in INGORED_PATHS:
            return True
