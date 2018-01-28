"""
Test pdbe cases.
"""
import unittest

from ddt import data, ddt, unpack

from pdbe.pdbe import (
    get_import_pdb_line_st_spaces,
    get_function_indent,
    is_function_sign_in_line,
)


@ddt
class TestPDBE(unittest.TestCase):
    """
    Test pdbe functionality.
    """

    @data(
        ('import sys', False),
        ('def fake_function(', False),
        ('def function(*args, **kwargs):', True),
    )
    @unpack
    def test_is_function_sign_in_line(self, line, expected):
        """
        Case: needs to detect function declaration.
        Expected: only line, that contains `def`, `(` and `):` substring confirmed.
        """
        result = is_function_sign_in_line(line)
        self.assertEqual(expected, result)

    @data(
        ('def function(*args, **kwargs):', 0),
        ('    def function(*args, **kwargs):', 4),
        ('        def function(*args, **kwargs):', 8),
    )
    @unpack
    def test_get_function_indent(self, line, expected):
        """
        Test function indents count.

        Import pdb statement need to be by 4 more.
        """
        result = get_function_indent(line)
        self.assertEqual(expected, result)

    @data(
        (0, '    '),
        (4, '        '),
        (8, '            '),
    )
    @unpack
    def test_get_import_pdb_line_start_spaces(self, indents_space_count, expected):
        """
        Test string, that needs to be before import pdb statement.
        """
        result = get_import_pdb_line_st_spaces(indents_space_count)
        self.assertEqual(expected, result)
