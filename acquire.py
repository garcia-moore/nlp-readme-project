import os
import json
import time
import pandas as pd
from typing import List, Dict, Union
import requests
from bs4 import BeautifulSoup

from env import github_token, github_username

def scrape_github_data():
    headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}
    if headers["Authorization"] == "token " or headers["User-Agent"] == "":
        raise Exception(
            "You need to replace 'your_github_token' and 'your_github_username' with your actual GitHub token and username"
        )

    def github_api_request(url: str) -> Union[List, Dict]:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if response.status_code != 200:
            raise Exception(
                f"Error response from github api! status code: {response.status_code}, "
                f"response: {json.dumps(response_data)}"
            )
        return response_data

    def get_repo_language(repo: str) -> str:
        url = f"https://api.github.com/repos/{repo}"
        repo_info = github_api_request(url)
        if isinstance(repo_info, dict):
            return repo_info.get("language", "")
        raise Exception(
            f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
        )

    def get_readme_contents(repo: str) -> str:
        url = f"https://api.github.com/repos/{repo}/readme"
        response = requests.get(url, headers=headers)
        if response.status_code == 404:  # handle not found error
            return ""  # return empty string or whatever default value you prefer
        readme_info = response.json()
        if isinstance(readme_info, dict):
            readme_text = requests.get(readme_info.get('download_url', '')).text
            return readme_text
        return ""

    def get_top_100_repos(language: str) -> List[str]:
        repos = []
        for page in range(1, 4):  # GitHub uses 1-indexed pages
            url = f"https://github.com/search?spoken_language_code=en&o=desc&q=stars%3A%3E1+language%3A{language}&s=forks&type=Repositories&l={language}&p={page}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            repos += [repo.get('href')[1:] for repo in soup.select('.v-align-middle') if repo.get('href')]
            if len(repos) >= 100:
                break
            time.sleep(3)  # sleep between requests to respect rate limits
        return repos[:100]

    def process_repo(repo: str) -> Dict[str, str]:
        """
        Takes a repo name like "gocodeup/codeup-setup-script" and returns a
        dictionary with the language of the repo and the readme contents.
        """
        return {
            "repo": repo,
            "language": get_repo_language(repo),
            "readme_contents": get_readme_contents(repo),
        }

    languages = ['JavaScript', 'Python', 'Java', 'C']
    data = []
    for language in languages:
        repos = get_top_100_repos(language)
        for repo in repos:
            data.append(process_repo(repo))

    df = pd.DataFrame(data)
    df.to_csv("github_data.csv", index=False)
    return df
