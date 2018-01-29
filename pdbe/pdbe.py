"""
pdbe functionality and implementation.
"""
import binascii
from os import fdopen, remove, getcwd, path, mkdir, walk, urandom, listdir
from os.path import isfile, join
from shutil import move
from tempfile import mkstemp
from typing import List, Optional, Tuple

IMPORT_PDB_LINE = 'import pdb; pdb.set_trace()\n'
LINE_FEED = '\n'


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


def get_import_pdb_line_begging_spaces(line: str) -> str:
    indents_space_count = get_function_indent(line)
    import_pdb_line_begging_spaces = get_import_pdb_line_st_spaces(indents_space_count)
    return import_pdb_line_begging_spaces


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
                    indents_space_count = get_function_indent(line)
                    import_pdb_line_begging_spaces = get_import_pdb_line_st_spaces(indents_space_count)
                    new_file.write(line + import_pdb_line_begging_spaces + IMPORT_PDB_LINE)
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


def get_commit_functions(file_path: str) -> list:

    commit_functions = []

    with open(file_path, 'r') as file:
        content = [line.strip() for line in file.readlines()]

        for index in range(len(content)):
            line = content[index]

            if does_line_contains_import_pdb(line):
                suggested_function = content[index-1]

                if is_function_sign_in_line(suggested_function):
                    function_open_bracket_index = suggested_function.index('(')
                    function_name = suggested_function[4:function_open_bracket_index]

                    commit_functions.append(function_name)

    return commit_functions


def get_project_call_cwd(call_commit_path: str, file_path: str) -> str:

    symbols_to_equal_paths = ' ' * (len(file_path) - len(call_commit_path))
    call_commit_path_with_static_length = call_commit_path + symbols_to_equal_paths

    project_call_cwd = ''

    for relative, static in zip(call_commit_path_with_static_length, file_path):
        if relative != static:
            project_call_cwd += static

    return project_call_cwd


def restore_import_pdb_from_commit(commit_content: List[str], call_commit_path: str):

    file_to_restore = ''

    for python_file in commit_content:

        if '.py' in python_file:
            file_to_restore = call_commit_path + python_file

        else:
            fh, abs_path = mkstemp()  # pylint:disable=invalid-name

            with fdopen(fh, 'w') as new_file:
                with open(file_to_restore) as old_file:
                    for line in old_file:
                        new_file.write(line)
                        
                        if 'def ' + python_file + '(' in line:
                            import_pdb_line_begging_spaces = get_import_pdb_line_begging_spaces(line)
                            new_file.write(import_pdb_line_begging_spaces + IMPORT_PDB_LINE)

            remove(file_to_restore)
            move(abs_path, file_to_restore)


def handle_commit_state(commit_message) -> None:

    commit_sha = binascii.hexlify(urandom(16)).decode("utf-8")

    call_commit_path = getcwd()
    pdbe_folder = call_commit_path + '/.pdbe'
    pdbe_commits_folder = pdbe_folder + '/commits'
    commit_file_path = pdbe_commits_folder + '/' + commit_sha

    if not path.exists(pdbe_folder):
        mkdir(pdbe_folder)
        mkdir(pdbe_commits_folder)

    python_files_in_directory = []

    for root, _, file_names in walk(call_commit_path):
        for file_name in file_names:
            if file_name.endswith('py'):
                file_path = root + '/' + file_name
                python_files_in_directory.append(file_path)

    with open(commit_file_path, 'w') as file:
        file.write(commit_sha + LINE_FEED)
        file.write(commit_message + LINE_FEED)

        for file_path in python_files_in_directory:
            commit_functions = get_commit_functions(file_path)

            if commit_functions:
                project_call_cwd = get_project_call_cwd(call_commit_path, file_path)
                file.write(project_call_cwd + LINE_FEED)

                for function_name in commit_functions:
                    file.write(function_name + LINE_FEED)


def handle_checkout(checkout_sha: int) -> None:

    call_commit_path = getcwd()
    pdbe_folder = call_commit_path + '/.pdbe'
    pdbe_commits_folder = pdbe_folder + '/commits/'

    try:
        for file in listdir(pdbe_commits_folder):
            file_path = join(pdbe_commits_folder, file)

            if checkout_sha in file_path:
                with open(file_path, 'r') as file:
                    content = [line.strip() for line in file.readlines()]
                    commit_content = content[2:]
                    restore_import_pdb_from_commit(commit_content, call_commit_path)

    except FileNotFoundError as error:
        print('{}: {}'.format(error.strerror, error.filename))

