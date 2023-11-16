# USAGE NOTES
#
#  Ensure it is executable 'chmod +x add_team_to_repo_list.sh'
#  
#  To run: ./add_team_to_repo_list.sh <github-organization> <github-team-name> <permission-level> <repo-list-file>
#
#  Replace YOUR_GITHUB_TOKEN with your personal access token you generated from github
#
#  Permission level options: pull, triage, push, maintain, admin. Default = push
#
#  The repo list file works with a txt file. Possibly other file formats but I did not test


#!/bin/bash

# Check for the required arguments
if [ $# -ne 4 ]; then
  echo "Usage: $0 <github-organization> <github-team-name> <permission-level> <repo-list-file>"
  exit 1
fi

# Set the variables
ORG_NAME=$1
TEAM_NAME=$2
PERMISSION_LEVEL=$3
REPO_LIST_FILE=$4

# Loop through the list of repositories in the file and add the team with the specified permission level
while read repo; do
  echo "Adding team $TEAM_NAME with permission $PERMISSION_LEVEL to repository $repo"
  curl -X PUT -H "Authorization: token YOUR_GITHUB_TOKEN" -H "Content-Type: application/json" \
  -d "{\"permission\":\"$PERMISSION_LEVEL\"}" \
  "https://api.github.com/orgs/$ORG_NAME/teams/$TEAM_NAME/repos/$ORG_NAME/$repo"
done < $REPO_LIST_FILE
