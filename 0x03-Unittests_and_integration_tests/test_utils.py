#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function from utils module.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map # Import the function to be tested

class TestAccessNestedMap(unittest.TestCase):
    """
    Tests the access_nested_map function for various valid inputs
    and exception cases.
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

    @parameterized.expand([
        # Test case 1: Empty map, trying to access 'a'
        ({}, ("a",), "a"), # Expected key 'a' to be in the error message
        # Test case 2: Map with 'a':1, trying to access 'b' via 'a'
        ({"a": 1}, ("a", "b"), "b"), # Expected key 'b' to be in the error message
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception_message):
        """
        Tests that access_nested_map raises a KeyError with the expected message
        for invalid access paths.

        Parameters:
            nested_map (dict): The nested dictionary to attempt access on.
            path (tuple): The invalid path (sequence of keys) to navigate.
            expected_exception_message (str): The key expected in the KeyError message.
        """
        # Use assertRaises as a context manager to check for exceptions
        # This block will pass if a KeyError is raised inside it
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # After the block, cm.exception holds the raised exception object
        # We then check if the message of that exception matches the expected key
        self.assertEqual(str(cm.exception), f"'{expected_exception_message}'")