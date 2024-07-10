# Used to add a topic to a list of repos. 
# Usage is python3 gh_add_topic.py <list.csv> <github PAT> <topic to add>
# Originally I ran into an issue where only the new topic remained on the test repos while all previously existing topics were removed.
# This is why there is the block finding the existing topics 



import requests
import csv
import argparse
from urllib.parse import urlparse

def add_topic_to_repo(org_name, token, repo_name, topic):
    url = f"https://api.github.com/repos/{org_name}/{repo_name}/topics"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.mercy-preview+json"
    }

    # Get the existing topics on the repository
    existing_topics_url = f"https://api.github.com/repos/{org_name}/{repo_name}"
    existing_topics_response = requests.get(existing_topics_url, headers=headers)
    existing_topics = existing_topics_response.json().get("topics", [])

    # Add the new topic to the existing topics
    existing_topics.append(topic)
    
    payload = {
        "names": existing_topics
    }
    
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Topic '{topic}' added to repository {repo_name} successfully.")
    else:
        print(f"Failed to add topic '{topic}' to repository {repo_name}. Status code: {response.status_code}")
        print(response.json())
        with open("failed_add_topic.txt", "a") as log_file:
            log_file.write(f"Failed to add '{topic}' topic to repository: {repo_name} -- ")
            log_file.write(f"Status code: {response.status_code} -- ")
            log_file.write(f"Response: {response.json()}\n")

# Command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("repo_list_file", help="File containing list of repositories")
parser.add_argument("token", help="GitHub personal access token")
parser.add_argument("topic", help="Topic to be added to repositories")
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
        
        # Add the topic to the repository while keeping existing topics
        add_topic_to_repo(org_name, args.token, repo_name, args.topic)
       
    else:
        print(f"Invalid repository URL format: {repo_url}. Skipping...")
