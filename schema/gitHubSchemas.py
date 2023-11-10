import requests
from urllib.parse import urlparse  # Add this import statement

def get_contributors(username, repo, access_token):
    contributors_url = f"https://api.github.com/repos/{username}/{repo}/contributors"
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(contributors_url, headers=headers)
    contributors = response.json()
    return contributors

def count_commits(username, repo, contributor_username, access_token):
    commits_url = f"https://api.github.com/repos/{username}/{repo}/commits"
    params = {'author': contributor_username}
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(commits_url, headers=headers, params=params)
    commits = response.json()
    return len(commits)

def save_contributors_commits(contributors_stats):
    data = {"contributors_commits": []}

    for contributor_username, commit_count in contributors_stats.items():
        contributor_data = {"username": contributor_username, "commit_count": commit_count}
        data["contributors_commits"].append(contributor_data)

    return data

def extract_contributor_commits(github_url, access_token):
    # Parse GitHub URL to extract username and repo
    url_parts = urlparse(github_url)
    path_parts = url_parts.path.strip('/').split('/')
    username, repo = path_parts[:2]

    contributors_stats = {}

    contributors = get_contributors(username, repo, access_token)

    for contributor in contributors:
        contributor_username = contributor['login']
        commit_count = count_commits(username, repo, contributor_username, access_token)
        contributors_stats[contributor_username] = commit_count

    return save_contributors_commits(contributors_stats)


def gitHubOutsideCollaborators(gitHubUrl):
    github_repo_url = gitHubUrl
    github_access_token = "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"  # Replace with your GitHub access token

    return extract_contributor_commits(github_repo_url, github_access_token)