#!/usr/bin/env python3
import os
import requests
import time

# Define GitHub API base URL and authentication token
GITHUB_API_URL = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def read_repo_list(filepath):
    """Read repository names from a text file."""
    with open(filepath, 'r') as file:
        repos = [line.strip() for line in file if line.strip()]
    return repos

def get_repository_id(owner, repo):
    """Get repository ID by name."""
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error getting repository {owner}/{repo}: {response.status_code}")
        print(response.json())
        return None

def enable_actions(repo_id):
    """Enable GitHub Actions for a repository."""
    url = f"{GITHUB_API_URL}/repositories/{repo_id}/actions/permissions"
    data = {"enabled": True}
    
    response = requests.put(url, headers=HEADERS, json=data)
    
    if response.status_code == 204:
        return True
    else:
        print(f"Error enabling actions for repository ID {repo_id}: {response.status_code}")
        print(response.json())
        return False

def main():
    # Get the repo list file path from user
    repo_file = input("Enter path to file containing repository names (format: owner/repo): ")
    
    # Read repository list
    try:
        repos = read_repo_list(repo_file)
    except Exception as e:
        print(f"Error reading repository list: {e}")
        return
    
    print(f"Found {len(repos)} repositories in the list")
    
    success_count = 0
    failure_count = 0
    
    for repo_path in repos:
        try:
            owner, repo = repo_path.split('/')
            print(f"Processing: {owner}/{repo}")
            
            # Get repository ID
            repo_id = get_repository_id(owner, repo)
            if not repo_id:
                print(f"Skipping {owner}/{repo} - could not get repository ID")
                failure_count += 1
                continue
            
            # Enable GitHub Actions
            if enable_actions(repo_id):
                print(f"✅ Successfully enabled Actions for {owner}/{repo}")
                success_count += 1
            else:
                print(f"❌ Failed to enable Actions for {owner}/{repo}")
                failure_count += 1
            
            # Avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing {repo_path}: {e}")
            failure_count += 1
    
    print(f"\nSummary: {success_count} succeeded, {failure_count} failed")

if __name__ == "__main__":
    main()