#!/usr/bin/env python3
"""
Unit tests for the access_nested_map and get_json functions from utils module.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock # Import patch and Mock for mocking
from utils import access_nested_map, get_json # Import both functions to be tested

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


class TestGetJson(unittest.TestCase):
    """
    Tests the get_json function from utils module.
    """

    @parameterized.expand([
        # Test case 1: Example.com with a simple payload
        ("http://example.com", {"payload": True}),
        # Test case 2: Holberton.io with a different payload
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get') # Decorator to patch requests.get before the test runs
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Tests that utils.get_json returns the expected result and
        that requests.get is called correctly.

        Parameters:
            test_url (str): The URL to pass to get_json.
            test_payload (dict): The expected JSON payload to be returned.
            mock_get (unittest.mock.Mock): The mock object for requests.get,
                                          injected by the @patch decorator.
        """
        # Configure the mock_get object:
        # When mock_get is called, it should return a mock object.
        # This returned mock object should have a .json() method.
        # When .json() is called on that mock object, it should return test_payload.
        mock_get.return_value.json.return_value = test_payload

        # Call the function under test
        actual_result = get_json(test_url)

        # Assertions:
        # 1. Test that the mocked requests.get was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # 2. Test that the output of get_json is equal to test_payload
        self.assertEqual(actual_result, test_payload)