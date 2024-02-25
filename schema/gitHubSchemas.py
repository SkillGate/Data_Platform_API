import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
from constants.gitHubConstants import get_contributors
from constants.gitHubConstants import get_commit_details
from constants.gitHubConstants import get_commits
from constants.gitHubConstants import get_organization_repositories
from constants.gitHubConstants import get_repository_languages
from constants.gitHubConstants import get_github_user_profile_info

load_dotenv()
github_access_token = os.getenv('GitHub_API_KEY')

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
    result = {"repositories": []}

    for repo_name, contributors_data in repositories_data.items():
        repo_info = {"reponame": repo_name, "contributors": []}

        for contributor_name, commit_data in contributors_data.items():
            contributor_info = {"username": contributor_name, "commit_count": commit_data['commit_count']}
            repo_info["contributors"].append(contributor_info)

        result["repositories"].append(repo_info)

    return result

def extract_contributors_commits_count(github_url, access_token):
    username, repo = extract_username_repo(github_url)
    repositories_data = {}

    # Check if the provided URL is an organization link
    if repo == '':
        repositories = get_organization_repositories(username, access_token)
    else:
        repositories = [repo]

    try:
        for repository in repositories:
            repository_data = {}

            # Extract contributors and commit counts for each repository
            contributors = get_contributors(username, repository, access_token)

            for contributor in contributors:
                if isinstance(contributor, dict) and 'login' in contributor:
                    contributor_username = contributor['login']
                    commit_count = len(get_commits(username, repository, contributor_username, access_token))

                    repository_data[contributor_username]={
                        'commit_count': commit_count
                    }
                else:
                    # Handle the case where 'login' key is not present or contributor is not a dictionary
                    print("Invalid contributor data:", contributor)

            repositories_data[repository] = repository_data
           
            
    except Exception as e:
        print(f"Error during iteration: {e}")

    return get_contributors_commits_count(repositories_data)


def get_contributors_commits_details(repositories_data):
    data = {"repositories": []}

    for repository_name, contributors_data in repositories_data.items():
        repository_info = {"reponame": repository_name, "contributors": []}

        for contributor_username, stats in contributors_data.items():
            contributor_data = {
                "username": contributor_username,
                "commit_count": stats['commit_count'],
                "commit_details": []
            }

            for commit_sha, commit_details in stats['commit_details'].items():
                commit_name = commit_details['commit']['message']
                stats = commit_details.get('stats', {})
                lines_changed = stats.get('total', 0)

                commit_data = {
                    "commit_name": commit_name,
                    "lines_changed": lines_changed,
                    "commit_sha": commit_sha
                }
                contributor_data["commit_details"].append(commit_data)

            repository_info["contributors"].append(contributor_data)

        data["repositories"].append(repository_info)

    return data

def extract_contributors_commits_details(github_url, access_token):
    username, repo = extract_username_repo(github_url)

    repositories_data = {}

    # Check if the provided URL is an organization link
    if repo == '':
        repositories = get_organization_repositories(username, access_token)
    else:
        repositories = [repo]

    for repository in repositories:
        repository_data = {}

        # Extract contributors and commit details for each repository
        contributors = get_contributors(username, repository, access_token)

        for contributor in contributors:
            contributor_username = contributor['login']
            commits = get_commits(username, repository, contributor_username, access_token)

            commit_details = {}

            for commit in commits:
                commit_sha = commit['sha']
                commit_details[commit_sha] = get_commit_details(username, repository, commit_sha, access_token)

            repository_data[contributor_username] = {
                'commit_count': len(commits),
                'commit_details': commit_details,
            }
        
        repositories_data[repository] = repository_data
            
    return get_contributors_commits_details(repositories_data)

def extract_repository_languages(github_url, access_token):
    username, repo = extract_username_repo(github_url)

    repositories_data = {}

    # Check if the provided URL is an organization link
    if repo == '':
        repositories = get_organization_repositories(username, access_token)
    else:
        repositories = [repo]

    for repository in repositories:
        languages = get_repository_languages(username, repository, access_token)
        repositories_data[repository] = {
            'language': languages
        }

    return repositories_data

def extract_user_profile_info(github_url, access_token):
    username = github_url.rstrip('/').rsplit('/', 1)[-1]
    user_info_all = get_github_user_profile_info(username, access_token)
    if user_info_all == '':
        user_info = {}
    else:
        user_info = {
        "name": user_info_all.get("name", ""),
        "followers": user_info_all.get("followers", 0),
        "following": user_info_all.get("following", 0),
        "total_private_repos": user_info_all.get("total_private_repos", 0),
        "owned_private_repos": user_info_all.get("owned_private_repos", 0),
        "public_repos": user_info_all.get("public_repos", 0),
        "public_gists": user_info_all.get("public_gists", 0)
    }
    return user_info

def extract_github_project_details(repositories_data):
    data = {"repositories": []}

    for repository_name, repository_data in repositories_data.items():

        languages = repository_data.get('languages', [])
        contributors_data = repository_data.get('contributors', {})

        repository_info = {"reponame": repository_name, "languages": languages, "contributors": []}

        for contributor_username, stats in contributors_data.items():
            contributor_data = {
                "username": contributor_username,
                "commit_count": stats['commit_count'],
                "commit_details": []
            }

            for commit_sha, commit_details in stats['commit_details'].items():
                commit_name = commit_details['commit']['message']
                commit_data = commit_details['commit']['committer']['date']
                stats = commit_details.get('stats', {})
                total_lines_changed = stats.get('total', 0)
                additions_lines_changed = stats.get('additions', 0)
                deletions_lines_changed = stats.get('deletions',0)

                commit_data = {
                    "commit_name": commit_name,
                    "commit_data": commit_data,
                    "lines_changed": total_lines_changed,
                    "additions_lines_changed": additions_lines_changed,
                    "deletions_lines_changed": deletions_lines_changed,
                    "commit_sha": commit_sha
                }
                contributor_data["commit_details"].append(commit_data)

            repository_info["contributors"].append(contributor_data)

        data["repositories"].append(repository_info)

    return data

def get_github_project_details(gitHubUrl):
    username, repo = extract_username_repo(gitHubUrl)
    repositories_data = {}
    if repo == '':
        repositories = get_organization_repositories(username, github_access_token)
    else:
        repositories = [repo]

    for repository in repositories:
        repository_data = {}
        contributors_data = {}
        contributors = get_contributors(username, repository, github_access_token)

        for contributor in contributors:
            contributor_username = contributor['login']
            commits = get_commits(username, repository, contributor_username, github_access_token)

            commit_details = {}

            for commit in commits:
                commit_sha = commit['sha']
                commit_details[commit_sha] = get_commit_details(username, repository, commit_sha, github_access_token)

            contributors_data[contributor_username] = {
                'commit_count': len(commits),
                'commit_details': commit_details,
            }

        languages = get_repository_languages(username, repository, github_access_token)
        repository_data['languages'] = languages
        repository_data['contributors'] = contributors_data
        
        repositories_data[repository] = repository_data

    result = extract_github_project_details(repositories_data)  
    return result

def github_collaborators_commit_count(gitHubUrl):
    return extract_contributors_commits_count(gitHubUrl, github_access_token)

def github_collaborators_commit_details(gitHubUrl):
    return extract_contributors_commits_details(gitHubUrl, github_access_token)

def github_organization_languages(gitHubUrl): 
    return extract_repository_languages(gitHubUrl, github_access_token)

def github_user_profile_info(gitHubUrl):
    return extract_user_profile_info(gitHubUrl, github_access_token)
