# For archiving github repos from a list. csv or txt work.
# Enter the repo with the full URL
# Make sure your PAT is authorized for any org the repos may live
# usage: python3 gh_archive_v2.py <repo_list> <token> 
# Any unsuccessful archives will be added to a txt file called failed_archiving.txt
# Updated from the original to add the "archived" topic

import requests
import csv
import argparse
from urllib.parse import urlparse

# Function to add the "archived" topic to a repository
def add_topic_to_repo(org_name, token, repo_name):
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/topics"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.mercy-preview+json"
    }
    payload = {
        "names": ["archived"]
    }
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Topic 'archived' added to repository {repo_name} successfully.")
    else:
        print(f"Failed to add topic 'archived' to repository {repo_name}. Status code: {response.status_code}")
        print(response.json())
        with open("failed_add_topic.txt", "a") as log_file:
            log_file.write(f"Failed to add 'archived' topic to repository: {repo_name} -- ")
            log_file.write(f"Status code: {response.status_code} -- ")
            log_file.write(f"Response: {response.json()}\n")

# Function to archive a repository
def archive_repo(org_name, token, repo_name):
    url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    headers = {
        "Authorization": f"token {token}"
    }
    payload = {
        "archived": True
    }
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Repository {repo_name} archived successfully.")
    else:
        print(f"Failed to archive repository {repo_name}. Status code: {response.status_code}")
        print(response.json())
        with open("failed_archiving.txt", "a") as log_file:
            log_file.write(f"Failed to archive repository: {repo_name} -- ")
            log_file.write(f"Status code: {response.status_code} -- ")
            log_file.write(f"Response: {response.json()}\n")

# Command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("repo_list_file", help="File containing list of repositories")
parser.add_argument("token", help="GitHub personal access token")
args = parser.parse_args()

# Read the repository list from the specified file
with open(args.repo_list_file, "r") as file:
    lines = file.readlines()

for line in lines:
    repo_url = line.strip()
    url_parts = urlparse(repo_url)
    path_parts = url_parts.path.split('/')
    if len(path_parts) >= 3:  # Check if the URL format is correct
        org_name = path_parts[1]
        repo_name = path_parts[2]
        
        # Add the "archived" topic to the repository
        add_topic_to_repo(org_name, args.token, repo_name)
        
        # Archive the repository
        archive_repo(org_name, args.token, repo_name)
    else:
        print(f"Invalid repository URL format: {repo_url}. Skipping...")
