import requests

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
    try:
        response = requests.get(commit_url, headers=headers)
        commit_details = response.json()
        return commit_details
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something went wrong",err)
    return []

def get_commits(username, repo, contributor_username, access_token):
    commits_url = f"https://api.github.com/repos/{username}/{repo}/commits"
    params = {'author': contributor_username}
    headers = {'Authorization': f'token {access_token}'}
    try:
        response = requests.get(commits_url, headers=headers, params=params)
        commits = response.json()
        return commits
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something went wrong",err)
    return []

def get_organization_repositories(organization, access_token):
    url = f"https://api.github.com/orgs/{organization}/repos"
    headers = {'Authorization': f'token {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        raise Exception(f"Failed to retrieve repositories. Status code: {response.status_code}, Response: {response.text}")

def get_repository_languages(owner, repo, access_token):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {access_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something went wrong", err)
    return []

def get_github_user_profile_info(username, access_token):
    url = f"https://api.github.com/users/{username}"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {access_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something went wrong", err)
    return []
