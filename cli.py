import sys
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_contents(owner, repo_name, current_path="", branch=None):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{current_path}"
    if branch:
        url += f"?ref={branch}"
    
    headers = {
        "Accept": "application/vnd.github+json"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"\n[DEBUG] API Error! Status code: {response.status_code}")
        print(f"[DEBUG] Server response: {response.text}")
        sys.exit(1)
        
    items = response.json()
    if not isinstance(items, list):
        items = [items]
        
    for item in items:
        if item["type"] == "dir":
            if item["name"] == ".git":
                continue
            # Recursive traversal for nested subdirectories
            fetch_contents(owner, repo_name, item["path"], branch)
        else:
            print(item["path"])

def list_repo_files(repo_path, branch=None):
    if not repo_path:
        print(f"Error: Path '{repo_path}' does not exist.")
        sys.exit(1)

    if "/" not in repo_path:
        print(f"Error: '{repo_path}' is not a valid target format (owner/repo).")
        sys.exit(1)
    
    if branch:
        print(f"--- Repository files: {repo_path} (branch: {branch}) ---")
    else:
        print(f"--- Repository files: {repo_path} (default branch) ---")
    
    owner, repo_name = repo_path.split("/", 1)
    fetch_contents(owner, repo_name, branch=branch)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cli.py <owner/repository> [branch_name]")
        sys.exit(1)

    target_path = sys.argv[1]
    target_branch = sys.argv[2] if len(sys.argv) > 2 else None
    
    list_repo_files(target_path, branch=target_branch)
