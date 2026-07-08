import sys
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
def list_repo_files(repo_path):
    if not repo_path: # we check if it exists this  directory
        print(f"Помилка: Шлях '{repo_path}' не існує.")
        sys.exit(1)

    if "/" not in repo_path: # we check if it is git-repository(looking for  .git folder
        print(f"Помилка: Шлях '{repo_path}' не є Git-репозиторієм (відсутня папка .git).")
        sys.exit(1)
    
    print(f"--- Список файлів у репозиторії: {repo_path} ---")
    
    owner, repo_name = repo_path.split("/", 1)
    
    def fetch_contents(current_path=""):
        url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{current_path}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            sys.exit(1)
            
        items = response.json()
        if not isinstance(items, list):
            items = [items]
            
        for item in items:
            if item["type"] == "dir": # git folder skip  
                if item["name"] == ".git":
                    continue
                fetch_contents(item["path"])
            else:
                print(item["path"])

    fetch_contents()

if __name__ == "__main__":
    if len(sys.argv) < 2: # we checked if a user give arguments
        print("Використання: python3 cli.py <owner/repository>")
        sys.exit(1)

    target_path = sys.argv[1]
    list_repo_files(target_path)
