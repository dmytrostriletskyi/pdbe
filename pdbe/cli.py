"""
CLI manager.
"""
import argparse
import sys
from os import getcwd, listdir, walk
from os.path import isfile, join
from typing import List, Optional, Tuple

from pdbe import put_import_pdb


def handle_file_argument(set_value: str) -> None:
    """
    Handle put import pdb statement under each function definition within file.
    """
    call_pdbe_path = getcwd()
    file_path = call_pdbe_path + '/' + set_value
    put_import_pdb(file_path)


def handle_dir_argument(set_value):
    """
    Handle put import pdb statement under each function definition within all files in directory.
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
        put_import_pdb(file_path)


def handle_everywhere_argument(set_value):

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
        put_import_pdb(file_path)


def parse_terminal_arguments(terminal_arguments: List[str]) -> argparse.Namespace:
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
        help='Directory to put import pdb under each function declaration all dir\'s, included nested also, files'
    )

    return parser.parse_args(terminal_arguments)


def get_used_terminal_pair(terminal_pairs_as_tuples: List[Tuple[str, Optional[str]]]) -> Optional[Tuple[str, str]]:
    """
    Find arguments pair, that used.
    """
    for pair in terminal_pairs_as_tuples:
        value = pair[1]
        if value is not None:
            return pair[0], value

    return


def main() -> None:
    """
    Main function, handled CLI.
    """
    arguments = sys.argv[1:]

    if not arguments:
        print('Specify arguments for pdbe tool. Call --help (-H) command to know more about it.')
        return

    terminal_pairs = parse_terminal_arguments(arguments)
    terminal_pairs_as_tuples = terminal_pairs._get_kwargs()

    set_flag, set_value = get_used_terminal_pair(terminal_pairs_as_tuples)

    possible_pairs = {
        'file': handle_file_argument,
        'dir': handle_dir_argument,
        'ew': handle_everywhere_argument,
    }

    possible_pairs[set_flag](set_value)


if __name__ == '__main__':
    main()