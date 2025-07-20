#!/usr/bin/env python3
"""
GitHub Org Client
"""
from typing import (
    List,
    Dict,
)

from utils import (
    get_json,
    access_nested_map,
    memoize,
)


class GithubOrgClient:
    """
    Client for interacting with the GitHub Organizations API.
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """
        Initializes a GithubOrgClient instance.

        Parameters:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """
        Returns the organization's information from the GitHub API, memoized.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """
        Returns the URL for the organization's public repositories.
        """
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """
        Returns the payload of public repositories from the GitHub API, memoized.
        """
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """
        Returns a list of public repository names for the organization,
        optionally filtered by license.

        Parameters:
            license (str, optional): The license key to filter repositories by.
                                     Defaults to None, returning all public repos.
        """
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """
        Checks if a given repository has a specific license.

        Parameters:
            repo (dict): A dictionary representing a repository.
            license_key (str): The license key to check for.
        """
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license
