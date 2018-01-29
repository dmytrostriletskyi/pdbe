"""
pdbe functionality and implementation.
"""
import datetime
import binascii
from os import fdopen, remove, getcwd, path, mkdir, walk, urandom, listdir
from os.path import join
from shutil import move
from tempfile import mkstemp
from typing import List

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


# pylint:disable=invalid-name
def get_import_pdb_line_begging_spaces(line: str) -> str:
    """
    Return string, that length equals to function indents plus 4.
    """
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
    """
    Return list of functions, that need to be commited.
    """
    commit_functions = []

    with open(file_path, 'r') as file:
        content = [line.strip() for line in file.readlines()]

        # pylint:disable=consider-using-enumerate
        for index in range(len(content)):
            line = content[index]

            if does_line_contains_import_pdb(line):
                suggested_function = content[index - 1]

                if is_function_sign_in_line(suggested_function):
                    function_open_bracket_index = suggested_function.index('(')
                    function_name = suggested_function[4:function_open_bracket_index]

                    commit_functions.append(function_name)

    return commit_functions


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


def restore_import_pdb_from_commit(commit_content: List[str], call_commit_path: str) -> None:
    """
    Restore import pdb statements from specified commit.
    """
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

                            # pylint:disable=invalid-name
                            import_pdb_line_begging_spaces = get_import_pdb_line_begging_spaces(line)
                            new_file.write(import_pdb_line_begging_spaces + IMPORT_PDB_LINE)

            remove(file_to_restore)
            move(abs_path, file_to_restore)


# pylint:disable=too-many-locals
def handle_commit_state(commit_message) -> None:
    """
    Handle commit state.
    """
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

        datetime_now = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        file.write(datetime_now + LINE_FEED)
        file.write(commit_sha + LINE_FEED)
        file.write(commit_message + LINE_FEED)

        for file_path in python_files_in_directory:
            commit_functions = get_commit_functions(file_path)

            if commit_functions:
                project_call_cwd = get_project_call_cwd(call_commit_path, file_path)
                file.write(project_call_cwd + LINE_FEED)

                for function_name in commit_functions:
                    file.write(function_name + LINE_FEED)


def handle_checkout(checkout_sha: str) -> None:
    """
    Handle checkout.
    """
    call_commit_path = getcwd()
    pdbe_folder = call_commit_path + '/.pdbe'
    pdbe_commits_folder = pdbe_folder + '/commits/'

    try:
        for file in listdir(pdbe_commits_folder):
            file_path = join(pdbe_commits_folder, file)

            if checkout_sha in file_path:
                with open(file_path, 'r') as file:
                    content = [line.strip() for line in file.readlines()]
                    commit_content = content[3:]
                    restore_import_pdb_from_commit(commit_content, call_commit_path)

    except FileNotFoundError as error:
        print('{}: {}'.format(error.strerror, error.filename))


def handle_commits_log() -> None:
    """
    Handle commits log.
    """
    call_commit_path = getcwd()
    pdbe_folder = call_commit_path + '/.pdbe'
    pdbe_commits_folder = pdbe_folder + '/commits/'

    logs = []

    for file in listdir(pdbe_commits_folder):
        file_path = join(pdbe_commits_folder, file)

        with open(file_path, 'r') as file:
            content = [line.strip() for line in file.readlines()]

            commit_created_datetime, commit_sha, commit_message = content[0], content[1], content[2]
            log = (commit_created_datetime, commit_sha, commit_message)

            logs.append(log)

    for log in logs:
        commit_created_datetime, commit_sha, commit_message = log[0], log[1], log[2]

        commit = '\033[94m' + 'commit  | {}'.format(commit_sha) + '\033[0m\n'
        date = 'date    | {}\n'.format(commit_created_datetime)
        message = 'message | {}\n'.format(commit_message)

        print(commit + date + message)
