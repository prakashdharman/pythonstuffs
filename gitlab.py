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


import subprocess
import csv
import os

def generate_git_log_csv(repo_path, output_csv):
    # Change to the specified directory
    os.chdir(repo_path)
    
    # Run the git log command
    result = subprocess.run(
        ["git", "log", "--since='7 days ago'", "--pretty=format:%ad,%s", "--date=iso"],
        capture_output=True,
        text=True
    )
    
    # Split the output into lines
    log_lines = result.stdout.strip().split('\n')
    
    # Write the log lines to a CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Commit Message"])
        for line in log_lines:
            writer.writerow(line.split(',', 1))

# Example usage
repo_path = "/path/to/your/repo"
output_csv = "commits_last_7_days.csv"
generate_git_log_csv(repo_path, output_csv)



import subprocess
import csv
import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_crq_reference(commit_message):
    # Regular expression to match CRQ references like CRQ123456:
    match = re.search(r'CRQ\d{6,}:', commit_message)
    return match.group(0) if match else ''

def generate_git_log_csv(repo_path, output_csv_path):
    # Check if the repository path exists
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    
    # Check if the output directory exists
    output_dir = os.path.dirname(output_csv_path)
    if not os.path.isdir(output_dir) and output_dir:
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

    logging.info(f"Processing repository: {repo_path}")
    
    try:
        # Change to the specified directory
        os.chdir(repo_path)
        
        # Run the git log command
        result = subprocess.run(
            ["git", "log", "--since=7 days ago", "--pretty=format:%ad,%s", "--date=iso"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        
        # Decode the output
        log_output = result.stdout.decode('utf-8')
        
        # Split the output into lines
        log_lines = log_output.strip().split('\n')
        
        # Write the log lines to a CSV file
        with open(output_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Commit Message", "CRQ Reference"])
            for line in log_lines:
                date_msg = line.split(',', 1)
                if len(date_msg) > 1:
                    date = date_msg[0]
                    commit_msg = date_msg[1]
                    crq_reference = extract_crq_reference(commit_msg)
                    writer.writerow([date, commit_msg, crq_reference])
        
        logging.info(f"CSV file created: {output_csv_path}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e.stderr.decode('utf-8')}")
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
    except PermissionError as e:
        logging.error(f"Permission error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def generate_reports(repos, output_dir):
    for repo_path, output_file_name in repos:
        output_csv_path = os.path.join(output_dir, output_file_name)
        generate_git_log_csv(repo_path, output_csv_path)

# Example usage
output_directory = "/path/to/your/output/directory"
repos = [
    ("/path/to/your/first/repo", "commits_first_repo_last_7_days.csv"),
    ("/path/to/your/second/repo", "commits_second_repo_last_7_days.csv")
]

generate_reports(repos, output_directory)


