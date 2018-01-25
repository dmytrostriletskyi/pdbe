"""
CLI manager.
"""
import argparse
import sys

from typing import List, Optional, Tuple


def handle_file_argument(set_value):
    pass


def handle_dir_argument(set_value):
    pass


def handle_everywhere_argument(set_value):
    pass


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
