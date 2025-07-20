#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
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
        mock_payload = {
            "login": org_name,
            "id": 12345,
            "public_repos": 100
        }
        mock_get_json.return_value = mock_payload

        # Instantiate GithubOrgClient with the parameterized org_name
        client = GithubOrgClient(org_name)

        # Call the .org property. This should trigger the call to get_json.
        result = client.org

        # Assertions:
        # 1. Test that get_json was called exactly once with the expected URL.
        # The expected URL is constructed based on the org_name.
        expected_url = ("https://api.github.com/orgs/{}".format(org_name))
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
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.public_repos returns the expected list of
        repositories and that the relevant mocks are called correctly.
        """
        # Define a mock payload for repos_payload
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"},  # No license
            {"name": "repo4", "license": {"key": "mit"}},
        ]

        # Configure the mock_get_json to return our mock_repos_payload
        mock_get_json.return_value = mock_repos_payload

        # Patch the _public_repos_url property as a context manager
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            # Configure the mocked _public_repos_url to return a dummy URL
            # The actual value doesn't matter here as get_json is mocked
            mock_public_repos_url.return_value = "http://dummy.url/repos"

            # Instantiate GithubOrgClient
            client = GithubOrgClient("test_org")

            # Call the public_repos method
            # This should trigger calls to _public_repos_url (memoized)
            # and then get_json (also memoized via repos_payload)
            result = client.public_repos()

            # Assertions:
            # 1. Test that _public_repos_url was accessed
            mock_public_repos_url.assert_called_once()

            # 2. Test that get_json was called exactly once
            # (It's called by repos_payload, which is memoized)
            mock_get_json.assert_called_once()

            # 3. Test that the list of repos is what we expect
            expected_repos = ["repo1", "repo2", "repo3", "repo4"]
            self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),  # Added case: license is None
        ({}, "my_license", False),  # Added case: no license key
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """
        Tests that GithubOrgClient.has_license returns the correct boolean value.

        Parameters:
            repo (dict): A dictionary representing a repository.
            license_key (str): The license key to check for.
            expected (bool): The expected boolean result.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# Fixture data for TestIntegrationGithubOrgClient
# These would typically come from a fixtures.py file or similar
# For this task, they are defined directly for clarity.
google_org_payload = {
    "login": "google",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/google/repos"
}
google_repos_payload = [
    {"name": "google-cloud-sdk", "license": {"key": "apache-2.0"}},
    {"name": "kubernetes", "license": {"key": "apache-2.0"}},
    {"name": "tensorflow", "license": {"key": "apache-2.0"}},
    {"name": "go-cloud", "license": {"key": "bsd-3-clause"}},
    {"name": "flutter", "license": {"key": "bsd-3-clause"}},
]
google_expected_repos = [
    "google-cloud-sdk", "kubernetes", "tensorflow", "go-cloud", "flutter"
]
google_apache2_repos = [
    "google-cloud-sdk", "kubernetes", "tensorflow"
]

abc_org_payload = {
    "login": "abc",
    "id": 2,
    "repos_url": "https://api.github.com/orgs/abc/repos"
}
abc_repos_payload = [
    {"name": "abc-repo1", "license": {"key": "mit"}},
    {"name": "abc-repo2", "license": {"key": "gpl-3.0"}}
]
abc_expected_repos = ["abc-repo1", "abc-repo2"]
abc_apache2_repos = []


@parameterized_class([
    {
        "org_payload": google_org_payload,
        "repos_payload": google_repos_payload,
        "expected_repos": google_expected_repos,
        "apache2_repos": google_apache2_repos,
    },
    {
        "org_payload": abc_org_payload,
        "repos_payload": abc_repos_payload,
        "expected_repos": abc_expected_repos,
        "apache2_repos": abc_apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient.public_repos method.
    This class uses parameterized_class to load fixtures and mocks
    external HTTP requests.
    """
    @classmethod
    def setUpClass(cls):
        """
        Sets up the class-level mocks for integration tests.
        Mocks requests.get to return predefined payloads based on URL.
        
        """
