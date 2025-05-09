#!/usr/bin/env python3
# Python Script to change the configuration of a CodeQL Default setup
# Steps below:
# Retrieve configurationID for the code security configuration from UI OR
#   - API Call: GET /orgs/{org}/code-security/configurations
# Get repositories associated with a code security configuration
#   - API Call: GET /rest/code-security/configurations/{configurationId}/repositories
# Update the above list of repos to use the extended query suite:
#   - API Call: PATCH /repos/{owner}/{repo}/code-scanning/default-setup { "query_suite": "extended" }

import json
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

# NOT NEEDED - Get security configurations for the organization
def get_security_configurations(org):
    url = f"{GITHUB_API_BASE_URL}/orgs/{org}/code-security/configurations"

    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error retrieving security configurations: {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    configurations = response.json()

def get_associated_repositories(org, config_id):
    # Get repositories associated with a code security configuration
    url = f"{GITHUB_API_BASE_URL}/orgs/{org}/code-security/configurations/{config_id}/repositories"
    params = {"status": "attached"}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error retrieving associated repositories: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    repositories = response.json()
    
    print(f"Found {len(repositories)} repositories associated with the configuration.")
    return repositories


def update_repositories(org, repo_name):
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

def main():
    # Main function to orchestrate the CodeQL configuration update.
    org = GITHUB_ORG
    if sys.argv[1]:
        config_id = sys.argv[1]
    else:
        print("Please provide the configuration ID as the command line argument.")
        sys.exit(1)
    
    #  Get associated repositories
    repositories = get_associated_repositories(org, config_id)

    # For each repo update security config to use extended query suite
    for repo in repositories:
        repo_name = repo["repository"]["name"]
        print(f"Processing repository: {repo_name}")
        update_status = update_repositories(org, repo_name)
        print(update_status)

    print("Process completed.")


if __name__ == "__main__":
    main()