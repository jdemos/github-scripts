# Python Script to change the configuration of a CodeQL Default setup
# Steps below:
# Pass code security configuration ID as cli argument
# Get repositories associated with a code security configuration
#   - API Call: GET /rest/code-security/configurations/{configurationId}/repositories
#   - Parameters: status=attached,enforced
# Update the above list of repos to use the extended query suite:
#   - API Call: PATCH /repos/{owner}/{repo}/code-scanning/default-setup { "query_suite": "extended" }

import sys
import os
import requests

# Define GitHub API base URL and authentication token
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("CODE_SCANNING_PAT")  # Replace with your GitHub token environment variable
GITHUB_ORG = "octodemo"  # Replace with your GitHub organization environment variable

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_associated_repos(org, config_id):
    # Get repos associated with a code security configuration
    url = f"{GITHUB_API_BASE_URL}/orgs/{org}/code-security/configurations/{config_id}/repositories"
    params = {"status": "attached,enforced"}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error retrieving associated repositories: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    repos = response.json()
    
    print(f"Found {len(repos)} repositories associated with the configuration.")
    return repos


def update_repos(org, repo_name):
    # Update repo to use the extended query suite
    url = f"{GITHUB_API_BASE_URL}/repos/{org}/{repo_name}/code-scanning/default-setup"
    payload = {"query_suite": "extended"}
    
    response = requests.patch(url, headers=HEADERS, json=payload)
    
    if response.status_code in [202, 200]:
        print(f"  ✓ Successfully updated {repo_name} to use extended query suite")
    else:
        print(f"✗ Failed to update {repo_name}: {response.status_code}")
        print(f"Error: {response.text}")

    return response.text

# Main function to orchestrate the CodeQL configuration update.
def main():
    # Assign value to org variable from constant
    org = GITHUB_ORG
    # Check if config_id was provided as a command line argument
    if sys.argv[1]:
        config_id = sys.argv[1]
    else:
        print("Please provide the configuration ID as the command line argument.")
        sys.exit(1)
    #  Get associated repos
    repos = get_associated_repos(org, config_id)

    # For each repo update security config to use extended query suite
    for repo in repos:
        repo_name = repo["repository"]["name"]
        print(f"Processing repository: {repo_name}")
        update_status = update_repos(org, repo_name)
        print(update_status)

    print("Process completed.")


if __name__ == "__main__":
    main()