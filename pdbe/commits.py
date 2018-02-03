"""
Pdbe commits logic.
"""
from datetime import datetime
import binascii
from os import fdopen, getcwd, path, mkdir, walk, urandom, listdir
from os.path import join
from tempfile import mkstemp
from typing import List

try:
    import utils
# pylint:disable=bare-except
except:  # Python 3.5 does not contain `ModuleNotFoundError`
    from pdbe import utils


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

            if utils.does_line_contains_import_pdb(line):
                suggested_function = content[index - 1]

                if utils.is_function_sign_in_line(suggested_function):
                    function_open_bracket_index = suggested_function.index('(')
                    function_name = suggested_function[4:function_open_bracket_index]

                    commit_functions.append(function_name)

    return commit_functions


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
                            import_pdb_line_begging_spaces = utils.get_import_pdb_line_begging_spaces(line)
                            new_file.write(import_pdb_line_begging_spaces + utils.IMPORT_PDB_LINE)

            utils.change_files_data(file_to_restore, abs_path)


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

    sorted_commits_by_datetime = sorted(
        logs, key=lambda x: datetime.strptime(x[0], '%H:%M:%S %d-%m-%Y'), reverse=True
    )

    for log in sorted_commits_by_datetime:

        commit_created_datetime, commit_sha, commit_message = log

        commit = '\033[94m' + 'commit  | {}'.format(commit_sha) + '\033[0m\n'
        date = 'date    | {}\n'.format(commit_created_datetime)
        message = 'message | {}\n'.format(commit_message)

        print(commit + date + message)


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

        datetime_now = datetime.now().strftime('%H:%M:%S %d-%m-%Y')

        file.write(datetime_now + utils.LINE_FEED)
        file.write(commit_sha + utils.LINE_FEED)
        file.write(commit_message + utils.LINE_FEED)

        for file_path in python_files_in_directory:
            commit_functions = get_commit_functions(file_path)

            if commit_functions:
                project_call_cwd = utils.get_project_call_cwd(call_commit_path, file_path)
                file.write(project_call_cwd + utils.LINE_FEED)

                for function_name in commit_functions:
                    file.write(function_name + utils.LINE_FEED)
