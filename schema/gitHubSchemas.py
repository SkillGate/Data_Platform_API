import os
import requests
from urllib.parse import urlparse  # Add this import statement
from dotenv import load_dotenv

def get_contributors(username, repo, access_token):
    contributors_url = f"https://api.github.com/repos/{username}/{repo}/contributors"
    headers = {'Authorization': f'token {access_token}'}
    try:
        response = requests.get(contributors_url, headers=headers)
        response.raise_for_status() 
        contributors = response.json()
        return contributors
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something went wrong",err)
    return []

def get_commit_details(username, repo, sha, access_token):
    commit_url = f"https://api.github.com/repos/{username}/{repo}/commits/{sha}"
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(commit_url, headers=headers)
    commit_details = response.json()
    return commit_details

def get_commits(username, repo, contributor_username, access_token):
    commits_url = f"https://api.github.com/repos/{username}/{repo}/commits"
    params = {'author': contributor_username}
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(commits_url, headers=headers, params=params)
    commits = response.json()
    return commits

def get_organization_repositories(organization, access_token):
    url = f"https://api.github.com/orgs/{organization}/repos"
    headers = {'Authorization': f'token {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        raise Exception(f"Failed to retrieve repositories. Status code: {response.status_code}, Response: {response.text}")

def extract_username_repo(github_url):
    url_parts = urlparse(github_url)
    path_parts = url_parts.path.strip('/').split('/')

    if len(path_parts) == 2:
        # Repository URL
        username, repo = path_parts
    elif len(path_parts) == 1 and path_parts[0] != '':
        # Organization URL
        username, repo = path_parts[0], ''
    else:
        raise ValueError("Invalid GitHub URL")

    return username, repo

def get_contributors_commits_count(repositories_data):
    return repositories_data

def extract_contributors_commits_count(github_url, access_token):
    username, repo = extract_username_repo(github_url)
    repositories_data = []

    # Check if the provided URL is an organization link
    if repo == '':
        repositories = get_organization_repositories(username, access_token)
    else:
        repositories = [repo]

    try:
        for repository in repositories:
            repository_contributors_stats = []

            # Extract contributors and commit counts for each repository
            contributors = get_contributors(username, repository, access_token)

            for contributor in contributors:
                if isinstance(contributor, dict) and 'login' in contributor:
                    contributor_username = contributor['login']
                    commit_count = len(get_commits(username, repository, contributor_username, access_token))

                    repository_contributors_stats.append({
                        'username': contributor_username,
                        'commit_count': commit_count
                    })
                else:
                    # Handle the case where 'login' key is not present or contributor is not a dictionary
                    print("Invalid contributor data:", contributor)

            repository_data = {
                'reponame': repository,
                'commit_description': repository_contributors_stats
            }
            repositories_data.append(repository_data)
            
    except Exception as e:
        print(f"Error during iteration: {e}")

    return get_contributors_commits_count(repositories_data)


def get_contributors_commits_details(contributors_stats):
    data = {"contributors_commits": []}

    for contributor_username, stats in contributors_stats.items():
        contributor_data = {"username": contributor_username, "commit_details": []}

        for commit_sha, commit_details in stats['commit_details'].items():
            commit_name = commit_details['commit']['message']
            stats = commit_details.get('stats', {})
            lines = stats.get('total', 0)

            commit_data = {"commit_name": commit_name, "lines_changed": lines}
            contributor_data["commit_details"].append(commit_data)

        data["contributors_commits"].append(contributor_data)

    return data

def extract_contributors_commits_details(github_url, access_token):
    username, repo = extract_username_repo(github_url)

    contributors_stats = {}

    # Check if the provided URL is an organization link
    if repo == '':
        repositories = get_organization_repositories(username, access_token)

        for repository in repositories:
            # Extract contributors and commit details for each repository
            contributors = get_contributors(username, repository, access_token)

            for contributor in contributors:
                contributor_username = contributor['login']
                commits = get_commits(username, repository, contributor_username, access_token)

                commit_details = {}

                for commit in commits:
                    commit_sha = commit['sha']
                    commit_details[commit_sha] = get_commit_details(username, repository, commit_sha, access_token)

                contributors_stats[contributor_username] = {
                    'repository': repository,
                    'commit_count': len(commits),
                    'commit_details': commit_details,
                }
    else:
        # Extract contributors and commit details for the specified repository
        contributors = get_contributors(username, repo, access_token)

        for contributor in contributors:
            contributor_username = contributor['login']
            commits = get_commits(username, repo, contributor_username, access_token)

            commit_details = {}

            for commit in commits:
                commit_sha = commit['sha']
                commit_details[commit_sha] = get_commit_details(username, repo, commit_sha, access_token)

            contributors_stats[contributor_username] = {
                'repository': repo,
                'commit_count': len(commits),
                'commit_details': commit_details,
            }
            
    return get_contributors_commits_details(contributors_stats)

def github_collaborators_commit_count(gitHubUrl):
    github_repo_url = gitHubUrl 
    github_access_token = os.getenv('GitHub_API_KEY')

    return extract_contributors_commits_count(github_repo_url, github_access_token)

def github_collaborators_commit_details(gitHubUrl):
    github_repo_url = gitHubUrl
    github_access_token = os.getenv('GitHub_API_KEY')

    return extract_contributors_commits_details(github_repo_url, github_access_token)
