import sys
from github_client import fetch_repo_context, fetch_pr_diff
from ai_analyzer import analyze_codebase, analyze_pull_request
from reporter import save_reports, save_pr_review

def print_usage():
    print("=" * 60)
    print("  AI Repository Analyzer & PR Reviewer")
    print("=" * 60)
    print("Mode 1: Full Repository Analysis (Standard Task)")
    print("  python3 cli.py <owner/repository> [branch_name]")
    print("\nMode 2: Automated PR Review Report (Bonus Task)")
    print("  python3 cli.py <owner/repository> --pr <pr_number>")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    target_path = sys.argv[1]
    if "/" not in target_path:
        print(f"[ERROR] '{target_path}' is not a valid repository format. Use 'owner/repo'.")
        sys.exit(1)
        
    owner, repo_name = target_path.split("/", 1)

    # Detect Bonus PR review mode
    if len(sys.argv) == 4 and sys.argv[2] == "--pr":
        pr_number = sys.argv[3]
        print(f"[*] [BONUS] Fetching Pull Request #{pr_number} diff for {target_path}...")
        diff_text = fetch_pr_diff(owner, repo_name, pr_number)
        
        print("[*] Sending PR diff to Gemini LLM for automated review...")
        review_data = analyze_pull_request(diff_text)
        
        print("[*] Saving automated PR review report...")
        save_pr_review(review_data)
        print("[SUCCESS] PR Review complete! Output saved to 'output/pr_review.md'.")
        
    else:
        # Full repository analysis mode
        target_branch = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"[*] Fetching repository context for {target_path}...")
        files, contents = fetch_repo_context(owner, repo_name, branch=target_branch)
        print(f"[+] Discovered {len(files)} files. Read contents for {len(contents)} source files.")

        print("[*] Analyzing codebase with Gemini LLM...")
        analysis = analyze_codebase(files, contents)

        print("[*] Saving final analysis reports...")
        save_reports(analysis)
        print("[SUCCESS] Full Analysis complete! Main report saved to 'output/report.md'.")

if __name__ == "__main__":
    main()
