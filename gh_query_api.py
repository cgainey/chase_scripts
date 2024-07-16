# I had a lot of trouble querying the github API and could not get a proper number of results. It was either stopping at 100 on the dot, ~150, or returning the total number of repos in the org (??) when I made changes to the `per_page` and such
# Turns out it was because of pagination. Pagination is annoying. I still don't really understand how to properly get even a known number of results. So this is the fix, just keep going if it is over your `per_page` size until it can't get more results.
# Anyway this handles it and returns a list of URLs that meet your query. Replace `html_url` with `name` or something if you want something else type of list

import requests

# Replace with your GitHub personal access token
token = 'TOKEN'

# Define the base URL for the GitHub API
base_url = 'https://api.github.com'

# Define the search query parameters
query_params = {
    'q': 'topic:EXAMPLE org:EXAMPLE archived:false',
    'per_page': 100
}

# Set the required headers and auth
headers = {
    'Authorization': 'token ' + token,
    'Accept': 'application/vnd.github.v3+json'
}

# Initialize an empty list to store all repository names
all_repo_names = []

# Make initial API request to search repositories
response = requests.get(base_url + '/search/repositories', params=query_params, headers=headers)

if response.status_code == 200:
    data = response.json()
    repo_names = [repo['html_url'] for repo in data['items']]
    all_repo_names.extend(repo_names)

    # Handle pagination if there are more than 100 results
    while 'next' in response.links:
        next_url = response.links['next']['url']
        response = requests.get(next_url, headers=headers)
        data = response.json()
        repo_names = [repo['html_url'] for repo in data['items']]
        all_repo_names.extend(repo_names)

    with open('repository_names.txt', 'w') as file:
        for name in all_repo_names:
            file.write(name + '\n')

    print("All repository names have been saved to repository_names1.txt")

else:
    print("Failed to fetch repositories. Status code:", response.status_code)
