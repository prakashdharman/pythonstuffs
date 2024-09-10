import requests
from datetime import datetime, timedelta

def get_bitbucket_commits_last_7_days(workspace, repo_slug, branch, username, app_password):
    """
    Fetches commit messages from the last 7 days from a specified branch in a Bitbucket repository.
    
    Parameters:
    - workspace (str): The Bitbucket workspace.
    - repo_slug (str): The repository slug or name.
    - branch (str): The branch to fetch commits from.
    - username (str): Your Bitbucket username.
    - app_password (str): Your Bitbucket app password.
    
    Returns:
    - list: A list of commit hashes and messages from the last 7 days.
    """
    # Calculate the date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Bitbucket API URL
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/commits/{branch}"
    params = {"q": f"date>{seven_days_ago}"}

    # Send the GET request to Bitbucket API with authentication
    response = requests.get(url, auth=(username, app_password), params=params)

    # Check if the request was successful
    if response.status_code == 200:
        commits = response.json()
        commit_list = []
        for commit in commits['values']:
            commit_info = {
                "hash": commit['hash'],
                "message": commit['message']
            }
            commit_list.append(commit_info)
        return commit_list
    else:
        print(f"Failed to retrieve commits: {response.status_code}, {response.text}")
        return []

# Example usage
if __name__ == "__main__":
    workspace = "your-workspace"
    repo_slug = "your-repo"
    branch = "development"
    username = "your-bitbucket-username"
    app_password = "your-bitbucket-app-password"

    commits = get_bitbucket_commits_last_7_days(workspace, repo_slug, branch, username, app_password)

    for commit in commits:
        print(f"Commit: {commit['hash']}")
        print(f"Message: {commit['message']}\n")
