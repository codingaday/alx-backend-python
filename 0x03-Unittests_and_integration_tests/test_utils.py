
#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function from utils module.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map # Import the function to be tested

class TestAccessNestedMap(unittest.TestCase):
    """
    Tests the access_nested_map function for various valid inputs.
    """

    @parameterized.expand([
        # Test case 1: Simple nested map, single key path
        ({"a": 1}, ("a",), 1),
        # Test case 2: Deeper nested map, single key path
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        # Test case 3: Deeper nested map, two-key path
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Tests that access_nested_map returns the expected result for valid inputs.

        Parameters:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path (sequence of keys) to navigate.
            expected_result (any): The expected value at the given path.
        """
        # Call the function with the provided test inputs
        actual_result = access_nested_map(nested_map, path)
        # Assert that the actual result matches the expected result
        self.assertEqual(actual_result, expected_result)