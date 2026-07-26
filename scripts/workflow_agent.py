import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(command, text=True, check=False)
    if check and result.returncode != 0:
        print(f"\n❌ Command failed: {' '.join(command)}")
        sys.exit(result.returncode)
    return result


def ensure_clean_git():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout.strip():
        print("❌ Git working tree is not clean. Commit or restore changes first.")
        print(result.stdout)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub issue, branch, run checks, commit, push, and open a PR."
    )
    parser.add_argument("--title", required=True, help="Issue and PR title")
    parser.add_argument("--body", required=True, help="Issue and PR body")
    parser.add_argument("--branch", required=True, help="New branch name")
    parser.add_argument("--commit-message", required=True, help="Commit message")
    parser.add_argument(
        "--skip-issue",
        action="store_true",
        help="Skip creating a GitHub issue",
    )

    args = parser.parse_args()

    if not Path(".git").exists():
        print("❌ Run this script from the repository root.")
        sys.exit(1)

    print("🤖 GitHub Workflow Agent - Phase 1")
    ensure_clean_git()

    issue_url = None
    if not args.skip_issue:
        issue = subprocess.run(
            ["gh", "issue", "create", "--title", args.title, "--body", args.body],
            capture_output=True,
            text=True,
            check=True,
        )
        issue_url = issue.stdout.strip()
        print(f"✅ Issue created: {issue_url}")

    run(["git", "checkout", "-b", args.branch])

    print("\n⚠️  Now make your code changes manually.")
    print("After editing files, run this script again with --skip-issue? No.")
    print("For Phase 1, this agent pauses here so you can safely edit files.")
    print("\nNext manual commands after editing:")
    print("  uv run ruff check")
    print("  uv run pytest -q")
    print("  git add .")
    print(f"  git commit -m \"{args.commit_message}\"")
    print(f"  git push -u origin {args.branch}")
    print("  gh pr create --title \"...\" --body \"...\" --base main --head BRANCH")
    print("\n✅ Branch is ready.")
    if issue_url:
        print(f"Link your PR body to the issue: Closes {issue_url.split('/')[-1]}")


if __name__ == "__main__":
    main()
