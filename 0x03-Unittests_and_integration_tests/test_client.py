#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.

        Parameters:
            org_name (str): The name of the organization to test.
            mock_get_json (unittest.mock.Mock): The mock object for get_json.
        """
        # Configure the mock_get_json to return a specific payload.
        # This payload simulates the response from the GitHub API.
        mock_payload = {"login": org_name, "id": 12345, "public_repos": 100}
        mock_get_json.return_value = mock_payload

        # Instantiate GithubOrgClient with the parameterized org_name
        client = GithubOrgClient(org_name)

        # Call the .org property. This should trigger the call to get_json.
        result = client.org

        # Assertions:
        # 1. Test that get_json was called exactly once with the expected URL.
        # The expected URL is constructed based on the org_name.
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # 2. Test that the output of .org is equal to the mock_payload.
        # This verifies that the client correctly processes the mocked response.
        self.assertEqual(result, mock_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests that GithubOrgClient._public_repos_url returns the expected URL
        based on a mocked org payload.
        """
        # Define a mock payload for the .org property
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}

        # Patch the 'org' property of GithubOrgClient
        # We use patch.object with new_callable=PropertyMock to mock a property
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            # Configure the mock_org property to return our test_payload
            mock_org.return_value = test_payload

            # Instantiate GithubOrgClient (the org_name doesn't matter here
            # as .org is mocked)
            client = GithubOrgClient("test_org")

            # Access the _public_repos_url property
            result = client._public_repos_url

            # Assertions:
            # 1. Test that the 'org' property was accessed
            mock_org.assert_called_once()

            # 2. Test that the result of _public_repos_url is the expected one
            self.assertEqual(result, test_payload["repos_url"])

