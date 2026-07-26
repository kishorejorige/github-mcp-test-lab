# GitHub MCP Test Lab

[![CI](https://github.com/kishorejorige/github-mcp-test-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/kishorejorige/github-mcp-test-lab/actions/workflows/ci.yml)

This repo is a small lab for practicing AI + GitHub + DevOps workflows.

It demonstrates a professional development flow:

```text
Issue → Branch → Code → Ruff → Pytest → Pull Request → CI → Merge
```

## Features

* Simple Python math functions
* Pytest test suite
* Ruff linting
* GitHub Actions CI
* CI status badge
* GitHub CLI workflow practice
* Local workflow automation agent

## Run Locally

Run the app:

```bash
uv run python app.py
```

Run Ruff:

```bash
uv run ruff check
```

Run tests:

```bash
uv run pytest -q
```

## GitHub Workflow Agent

The local workflow agent helps automate a safe GitHub development workflow.

The agent has two commands:

```text
start  → creates a GitHub issue and a feature branch
finish → runs Ruff, runs Pytest, commits, pushes, and creates a PR
```

It does **not** auto-merge pull requests. A human should review CI results before merging.

## Start a New Task

Example:

```bash
uv run python scripts/workflow_agent.py start \
  --title "Add divide function" \
  --body "Add divide function and tests using the workflow agent." \
  --branch "issue-add-divide-function" \
  --commit-message "feat: add divide function"
```

The agent will:

* Check that Git is clean
* Create a GitHub issue
* Create a new branch
* Print the next command to run after editing files

## Finish a Task

After editing files, run:

```bash
uv run python scripts/workflow_agent.py finish \
  --commit-message "feat: add divide function" \
  --pr-title "Add divide function" \
  --pr-body "Closes #ISSUE_NUMBER. Adds divide function and tests."
```

The agent will:

* Confirm you are not on `main`
* Confirm file changes exist
* Run Ruff
* Run Pytest
* Commit changes
* Push the feature branch
* Create a pull request

## Manual Merge Step

After the PR is created, check CI:

```bash
gh pr checks
```

If checks pass, merge:

```bash
gh pr merge PR_NUMBER --merge --delete-branch
```

Then sync local main:

```bash
git checkout main
git pull origin main
git status
```

## What This Lab Proves

This project shows practical DevOps and GitHub workflow skills:

* Clean branching workflow
* Pull request workflow
* Automated linting and testing
* GitHub Actions CI
* GitHub CLI usage
* Safe local automation agent

## Next Improvements

* Add branch protection rules
* Add CodeQL security scanning
* Add automatic PR templates
* Add MCP-based GitHub agent integration
* Add more automation commands
