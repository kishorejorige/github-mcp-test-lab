import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], check: bool = True, capture: bool = False):
    print(f"\n$ {' '.join(command)}")
    result = subprocess.run(
        command,
        text=True,
        check=False,
        capture_output=capture,
    )
    if check and result.returncode != 0:
        print(f"\n❌ Command failed: {' '.join(command)}")
        if capture:
            print(result.stdout)
            print(result.stderr)
        sys.exit(result.returncode)
    return result


def ensure_repo_root():
    if not Path(".git").exists():
        print("❌ Run this script from the repository root.")
        sys.exit(1)


def ensure_clean_git():
    result = run(["git", "status", "--porcelain"], capture=True)
    if result.stdout.strip():
        print("❌ Git working tree is not clean. Commit or restore changes first.")
        print(result.stdout)
        sys.exit(1)


def ensure_changes_exist():
    result = run(["git", "status", "--porcelain"], capture=True)
    if not result.stdout.strip():
        print("❌ No file changes found. Edit files first, then run finish.")
        sys.exit(1)


def current_branch() -> str:
    result = run(["git", "branch", "--show-current"], capture=True)
    return result.stdout.strip()


def start(args):
    print("🤖 Workflow Agent: start")
    ensure_repo_root()
    ensure_clean_git()

    issue = run(
        ["gh", "issue", "create", "--title", args.title, "--body", args.body],
        capture=True,
    )
    issue_url = issue.stdout.strip()
    issue_number = issue_url.rstrip("/").split("/")[-1]

    print(f"✅ Issue created: {issue_url}")
    run(["git", "checkout", "-b", args.branch])

    print("\n✅ Branch is ready.")
    print("Now manually edit files, then run:")
    print(
        f'uv run python scripts/workflow_agent.py finish '
        f'--commit-message "{args.commit_message}" '
        f'--pr-title "{args.title}" '
        f'--pr-body "Closes #{issue_number}. {args.body}"'
    )


def finish(args):
    print("🤖 Workflow Agent: finish")
    ensure_repo_root()

    branch = current_branch()
    if branch == "main":
        print("❌ You are on main. Create/use a feature branch first.")
        sys.exit(1)

    ensure_changes_exist()

    run(["uv", "run", "ruff", "check"])
    run(["uv", "run", "pytest", "-q"])

    run(["git", "add", "."])
    run(["git", "commit", "-m", args.commit_message])
    run(["git", "push", "-u", "origin", branch])

    pr = run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            args.pr_title,
            "--body",
            args.pr_body,
            "--base",
            "main",
            "--head",
            branch,
        ],
        capture=True,
    )

    print(f"✅ Pull request created: {pr.stdout.strip()}")
    print("\nNext check CI:")
    print("gh pr checks")


def main():
    parser = argparse.ArgumentParser(description="Local GitHub workflow agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Create issue and branch")
    start_parser.add_argument("--title", required=True)
    start_parser.add_argument("--body", required=True)
    start_parser.add_argument("--branch", required=True)
    start_parser.add_argument("--commit-message", required=True)

    finish_parser = subparsers.add_parser("finish", help="Run checks, commit, push, PR")
    finish_parser.add_argument("--commit-message", required=True)
    finish_parser.add_argument("--pr-title", required=True)
    finish_parser.add_argument("--pr-body", required=True)

    args = parser.parse_args()

    if args.command == "start":
        start(args)
    elif args.command == "finish":
        finish(args)


if __name__ == "__main__":
    main()
