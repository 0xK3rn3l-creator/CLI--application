import os
import sys
import requests
import base64

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def _get_headers(accept_header="application/vnd.github+json"):
    headers = {"Accept": accept_header}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_repo_context(owner, repo_name, current_path="", branch=None):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{current_path}"
    if branch:
        url += f"?ref={branch}"
    
    headers = _get_headers()
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"\n[DEBUG] GitHub API Error! Status code: {response.status_code}")
        print(f"[DEBUG] Server response: {response.text}")
        sys.exit(1)
        
    items = response.json()
    if not isinstance(items, list):
        items = [items]
        
    file_list = []
    file_contents = {}
    
    ignored_names = {".git", "node_modules", "__pycache__", "venv", ".vs", "obj", "bin", ".idea"}
    allowed_extensions = ('.py', '.md', '.json', '.txt', '.js', '.cs', '.ts', '.html', '.css', '.go', '.rs', '.cpp', '.h')

    for item in items:
        if item["type"] == "dir":
            if item["name"] in ignored_names:
                continue
            sub_files, sub_contents = fetch_repo_context(owner, repo_name, item["path"], branch)
            file_list.extend(sub_files)
            file_contents.update(sub_contents)
        else:
            file_list.append(item["path"])
            filename = item["name"].lower()
            
            if filename.endswith(allowed_extensions) and item["size"] < 100000:
                file_resp = requests.get(item["url"], headers=headers)
                if file_resp.status_code == 200:
                    file_data = file_resp.json()
                    if file_data.get("encoding") == "base64":
                        try:
                            decoded = base64.b64decode(file_data["content"]).decode('utf-8', errors='ignore')
                            file_contents[item["path"]] = decoded
                        except Exception:
                            pass

    return file_list, file_contents

def fetch_pr_diff(owner, repo_name, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}"
    headers = _get_headers(accept_header="application/vnd.github.v3.diff")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"\n[DEBUG] GitHub API Error fetching PR diff! Status code: {response.status_code}")
        print(f"[DEBUG] Server response: {response.text}")
        sys.exit(1)
        
    return response.text
