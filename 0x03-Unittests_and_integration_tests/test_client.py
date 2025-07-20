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
        """
        mock_payload = {
            "login": org_name,
            "id": 12345,
            "public_repos": 100
        }
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = ("https://api.github.com/orgs/{}".format(org_name))
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, mock_payload)

    def test_public_repos_url(self) -> None:
        """
        Tests that GithubOrgClient._public_repos_url returns the expected URL.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.public_repos returns the expected list
        of repositories and that mocks are called correctly.
        """
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"},  # No license
            {"name": "repo4", "license": {"key": "mit"}},
        ]

        mock_get_json.return_value = mock_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://dummy.url/repos"
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()
            expected_repos = ["repo1", "repo2", "repo3", "repo4"]
            self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str,
                         expected: bool) -> None:
        """
        Tests that GithubOrgClient.has_license returns the correct boolean.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# Fixture data for TestIntegrationGithubOrgClient
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
    Integration tests for GithubOrgClient.public_repos.
    Uses parameterized_class to load fixtures and mocks external HTTP requests.
    """
    @classmethod
    def setUpClass(cls):
        """
        Sets up class-level mocks for integration tests.
        Mocks requests.get to return predefined payloads.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect_func(url):
            if url == cls.org_payload["repos_url"].replace("/repos", ""):
                return Mock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return Mock(json=lambda: cls.repos_payload)
            else:
                raise ValueError(f"Unexpected URL: {url}")

        cls.mock_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls):
        """
        Stops the patcher after all integration tests in this class have run.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Tests that GithubOrgClient.public_repos returns expected repositories.
        """
        client = GithubOrgClient(self.org_payload["login"])
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Tests GithubOrgClient.public_repos with license filter.
        """
        client = GithubOrgClient(self.org_payload["login"])
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
