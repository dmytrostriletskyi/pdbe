"""
Pdbe commits logic.
"""
import binascii
import keyword
from datetime import datetime
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

        suggested_function = ''

        # pylint:disable=consider-using-enumerate
        for line in content:

            if utils.is_one_line_function_declaration_line(line) and not utils.is_commended_function(line):
                function_open_bracket_index = line.index('(')
                suggested_function = line[4:function_open_bracket_index]

            elif 'def' in line and '(' in line and not utils.is_commended_function(line):
                function_open_bracket_index = line.index('(')
                suggested_function = line[4:function_open_bracket_index]

            if utils.does_line_contains_import_pdb(line):
                commit_functions.append(suggested_function)

    return commit_functions


# too-many-locals, too-many-branches, refactor
# pylint:disable=too-many-locals,too-many-branches
def restore_import_pdb_from_commit(commit_content: List[str], call_commit_path: str) -> None:
    """
    Restore import pdb statements from specified commit.
    """
    commit_content.append('.py')  # mock for algorithm below

    files_to_restore = []
    functions_to_restore = []
    temp_restore = []

    for content in commit_content:

        if '.py' not in content:
            temp_restore.append(content)

        if '.py' in content:
            if temp_restore:
                functions_to_restore.append(temp_restore)
                temp_restore = []

            file_to_restore = call_commit_path + content
            files_to_restore.append(file_to_restore)

    for file_to_restore, functions in zip(files_to_restore, functions_to_restore):

        fh, abs_path = mkstemp()  # pylint:disable=invalid-name

        with fdopen(fh, 'w') as new_file:
            with open(file_to_restore) as old_file:
                stored_import_pdb_line_begging_spaces = ''
                stored_function_name = ''

                for line in old_file:
                    keywords_in_line = list(set(keyword.kwlist).intersection(line.split()))
                    new_file.write(line)

                    if 'def ' in line and '(' in line and '):' in line and not utils.is_commended_function(line):

                        strip_line = line.strip()
                        function_open_bracket_index = strip_line.index('(')
                        function_name = strip_line[4:function_open_bracket_index]

                        if function_name in functions:
                            # pylint:disable=invalid-name
                            import_pdb_line_begging_spaces = utils.get_import_pdb_line_begging_spaces(line)
                            new_file.write(import_pdb_line_begging_spaces + utils.IMPORT_PDB_LINE)

                    elif 'def ' in line and '(' in line and '):' not in line:
                        function_name = line.split()[1][:-1]

                        if function_name in functions:
                            import_pdb_line_begging_spaces = utils.get_import_pdb_line_begging_spaces(line)
                            stored_import_pdb_line_begging_spaces = import_pdb_line_begging_spaces
                            stored_function_name = function_name
                        else:
                            stored_function_name = ''

                    elif 'def' not in line and '):' in line and not keywords_in_line:
                        if stored_function_name in functions:
                            new_file.write(stored_import_pdb_line_begging_spaces + utils.IMPORT_PDB_LINE)

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
