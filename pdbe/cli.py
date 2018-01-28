"""
CLI manager.
"""
import argparse
import sys
from os import getcwd, listdir, walk
from os.path import isfile, join
from typing import List, Optional, Tuple

from pdbe import put_import_pdb, remove_import_pdb


def handle_file_argument(set_value: str, clear=False) -> None:
    """
    Handle import pdb statement under each function definition within file.
    """
    call_pdbe_path = getcwd()
    file_path = call_pdbe_path + '/' + set_value

    if clear:
        remove_import_pdb(file_path)

    else:
        put_import_pdb(file_path)


def handle_dir_argument(set_value: str, clear=False) -> None:
    """
    Handle import pdb statement under each function definition within all files in directory.
    """
    if set_value == '.':
        set_value = ''

    call_pdbe_path = getcwd()
    directory_path = call_pdbe_path + '/' + set_value

    python_files_in_directory = []

    try:
        for file in listdir(directory_path):
            file_path = join(directory_path, file)
            if isfile(file_path) and file.endswith('.py'):
                python_files_in_directory.append(file_path)

    except FileNotFoundError as error:
        print('{}: {}'.format(error.strerror, error.filename))

    for file_path in python_files_in_directory:
        if clear:
            remove_import_pdb(file_path)
        else:
            put_import_pdb(file_path)


def handle_everywhere_argument(set_value: str, clear=False) -> None:
    """
    Handle import pdb statement under each function definition within all nested files in directory.
    """
    if set_value.endswith('/'):
        print('\nEnter folder\'s name without slash at the and.\n')
        return

    call_pdbe_path = getcwd()
    directory_path = call_pdbe_path + '/' + set_value

    if set_value == '.':
        directory_path = directory_path[:-2]

    python_files_in_directory = []

    for root, _, file_names in walk(directory_path):
        for file_name in file_names:
            if file_name.endswith('py'):
                file_path = root + '/' + file_name
                python_files_in_directory.append(file_path)

    for file_path in python_files_in_directory:
        if clear:
            remove_import_pdb(file_path)
        else:
            put_import_pdb(file_path)


def parse_terminal_arguments(terminal_arguments: List[str]) -> argparse.Namespace:
    """
    Parse terminal arguments.
    """
    parser = argparse.ArgumentParser(description='pdbe arguments parser.')
    parser.add_argument(
        '-F',
        '--file',
        help='File to put import pdb under each function declaration in file.'
    )
    parser.add_argument(
        '-D',
        '--dir',
        help='Directory to put import pdb under each function declaration all specified dir\'s files .'
    )
    parser.add_argument(
        '-E',
        '--ew',
        help='Directory to put import pdb under each function declaration all dir\'s, included nested also, files',
    )
    parser.add_argument(
        '-C',
        '--clear',
        help='Clear import pdb statements in entered paths.',
        dest='clear',
        action='store_true'
    )
    return parser.parse_args(terminal_arguments)


# pylint:disable=inconsistent-return-statements
def get_used_terminal_pair(terminal_pairs_as_tuples: List[Tuple[str, Optional[str]]]) -> Optional[Tuple[str, str]]:
    """
    Find arguments pair, that used.
    """
    for pair in terminal_pairs_as_tuples:
        value = pair[1]
        if value is not None:
            return pair[0], value

    return


def handle_clear_argument(terminal_pairs_as_tuples) -> bool:
    """
    Return clear argument as bool value for existing and non-existing.

    Also remove it from terminal flag-value pairs because of dict-value handling.
    """
    clear = False

    for i, pair in enumerate(terminal_pairs_as_tuples):
        flag, value = pair[0], pair[1]

        if flag == 'clear':
            if value:
                clear = True

            del terminal_pairs_as_tuples[i]

    return clear


def pdbe() -> None:
    """
    Main function, handled CLI.
    """
    arguments = sys.argv[1:]

    if not arguments:
        print('Specify arguments for pdbe tool. Call --help (-H) command to know more about it.')
        return

    terminal_pairs = parse_terminal_arguments(arguments)
    terminal_pairs_as_tuples = terminal_pairs._get_kwargs()  # pylint:disable=protected-access

    clear = handle_clear_argument(terminal_pairs_as_tuples)
    set_flag, set_value = get_used_terminal_pair(terminal_pairs_as_tuples)

    possible_pairs = {
        'file': handle_file_argument,
        'dir': handle_dir_argument,
        'ew': handle_everywhere_argument,
    }

    possible_pairs[set_flag](set_value, clear)


if __name__ == '__main__':
    pdbe()
