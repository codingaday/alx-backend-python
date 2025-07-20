#!/usr/bin/env python3
"""
Unit tests for the access_nested_map, get_json, and memoize functions from
utils module.
"""
import unittest
from parameterized import parameterized
# Import patch and Mock for mocking, added for later tasks
from unittest.mock import patch, Mock
# Import all functions to be tested, modified for later tasks
from utils import access_nested_map, get_json, memoize


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

    # --- Start of Task 1: Exception testing for access_nested_map ---
    @parameterized.expand([
        # Test case 1: Empty map, trying to access 'a'
        ({}, ("a",), "a"),  # Expected key 'a' in error message
        # Test case 2: Map with 'a':1, trying to access 'b' via 'a'
        ({"a": 1}, ("a", "b"), "b"),  # Expected key 'b' in error message
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_exception_message):
        """
        Tests that access_nested_map raises a KeyError with the expected message
        for invalid access paths.

        Parameters:
            nested_map (dict): The nested dictionary to attempt access on.
            path (tuple): The invalid path (sequence of keys) to navigate.
            expected_exception_message (str): The key expected in the KeyError
                                              message.
        """
        # Use assertRaises as a context manager to check for exceptions
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # After the block, cm.exception holds the raised exception object
        self.assertEqual(str(cm.exception), f"'{expected_exception_message}'")
    # --- End of Task 1 ---


# --- Start of Task 2: Testing get_json ---
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
    @patch('requests.get')  # Decorator to patch requests.get before test runs
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
        # When .json() is called on that mock object, it should return
        # test_payload.
        mock_get.return_value.json.return_value = test_payload

        # Call the function under test
        actual_result = get_json(test_url)

        # Assertions:
        # 1. Test that the mocked requests.get was called exactly once with
        # test_url
        mock_get.assert_called_once_with(test_url)

        # 2. Test that the output of get_json is equal to test_payload
        self.assertEqual(actual_result, test_payload)
# --- End of Task 2 (get_json) ---


# --- Start of Task 2: Testing memoize ---
class TestMemoize(unittest.TestCase):
    """
    Tests the memoize decorator from utils module.
    """

    def test_memoize(self):
        """
        Tests that a method decorated with @memoize caches its result
        and the underlying method is called only once.
        """
        # Define the inner class for testing memoization
        class TestClass:
            """
            A simple class to test the memoize decorator.
            """
            def a_method(self):
                """
                A simple method that returns 42.
                """
                return 42

            @memoize
            def a_property(self):
                """
                A property that uses a_method and is memoized.
                """
                return self.a_method()

        # Use patch as a context manager to mock 'a_method' within 'TestClass'
        # We need to patch 'TestClass.a_method' directly.
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            # Instantiate TestClass
            test_instance = TestClass()

            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assertions:
            # 1. Test that a_method was called exactly once
            mock_a_method.assert_called_once()

            # 2. Test that the correct result is returned both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
