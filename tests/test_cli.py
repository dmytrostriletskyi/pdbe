"""
Test CLI cases.
"""
import unittest

from ddt import data, ddt, unpack

from pdbe.cli import get_used_terminal_pair


@ddt
class TestCLIUtils(unittest.TestCase):
    """
    Test CLI helpers.
    """

    @data(
        (
            [('file', 'sometestforpdb.py'), ('dir', None), ('ew', None)], ('file', 'sometestforpdb.py')
        ),
        (
            [('file', None), ('dir', None), ('ew', None)], None
        )
    )
    @unpack
    def test_get_used_terminal_pair(self, enter, expected):
        """
        Case: find pair, that flag's value is not None to work with.
        Expected: return flag and it's value else None.
        """
        result = get_used_terminal_pair(enter)
        self.assertEqual(expected, result)
