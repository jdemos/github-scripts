# Python Script to enable Actions for a list of repositories
import os
import requests

# Define GitHub API base URL and authentication token
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("ACTIONS_PAT")  # Replace with your GitHub token
GITHUB_ORG = "johnd-testing"  # Replace with your GitHub organization

# Define list of repository names
def load_repositories(filename='repositories.txt'):
    try:
        with open(filename, 'r') as file:
            # Read repositories and strip whitespace
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Repository list file '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error loading repository list: {e}")
        return []


# Function to enable GitHub Actions for a repository
def enable_github_actions(owner, repo):
    url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/actions/permissions"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "enabled": True,
        "allowed_actions": "all"
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code != 204:
        print(f"Failed to enable GitHub Actions for repository {repo}. Status: {response.status_code}, Error: {response.text}")

# Main script logic
def main():
    owner = "johnd-testing"  # Replace with your GitHub owner/org
    org = "johnd-testing"  # Replace with your GitHub organization

    # Load repositories from file
    repositories = load_repositories()

    for repo in repositories:
        enable_github_actions(owner, repo)
        # Print success message
        print(f"Enabled GitHub Actions for {repo}")

if __name__ == "__main__":
    main()