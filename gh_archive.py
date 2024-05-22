import requests #this is for getting errors back
import csv      #this is in case I want to use a csv over .txt
import argparse #because I want command line arguments 
from urllib.parse import urlparse #because i want to grab org and repo from link

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
        archive_repo(org_name, args.token, repo_name)
    else:
        print(f"Invalid repository URL format: {repo_url}. Skipping...")