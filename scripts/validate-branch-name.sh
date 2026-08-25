#!/usr/bin/env bash

# Fail fast on command errors and unset variables.
set -euo pipefail

echo "🔍 Validating workspace branch naming conventions..."

PACKAGE_JSON_PATH="package.json"

if [ ! -f "$PACKAGE_JSON_PATH" ]; then
  echo "❌ Error: package.json file could not be found at repository root." >&2
  exit 1
fi

# Prefer an explicitly supplied branch name.
# This is the expected execution path for CI environments such as GitHub Actions.
BRANCH_NAME="${BRANCH_NAME:-}"

# Fall back to the local Git working tree for developer-side execution.
if [ -z "$BRANCH_NAME" ]; then
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "❌ Error: BRANCH_NAME is not defined and the current directory is not a Git repository." >&2
    exit 1
  fi

  BRANCH_NAME="$(git branch --show-current)"
fi

if [ -z "$BRANCH_NAME" ]; then
  echo "❌ Error: Unable to determine the current branch name." >&2
  exit 1
fi

CONFIG_PATTERN="$(
  node -e "
    try {
      const pkg = require('./$PACKAGE_JSON_PATH');
      const cfg = pkg['validate-branch-name'];

      if (!cfg || !cfg.pattern) {
        process.exit(1);
      }

      process.stdout.write(cfg.pattern);
    } catch {
      process.exit(1);
    }
  " 2>/dev/null || true
)"

if [ -z "$CONFIG_PATTERN" ]; then
  echo "❌ Error: validate-branch-name configuration or pattern is missing from package.json." >&2
  exit 1
fi

if [[ ! "$BRANCH_NAME" =~ $CONFIG_PATTERN ]]; then
  echo "❌ Error: Branch verification failed!" >&2

  node -e "
    const pkg = require('./$PACKAGE_JSON_PATH');
    console.error(
      pkg['validate-branch-name'].errorMsg ||
      'Invalid branch name standard.'
    );
  " 2>/dev/null || true

  echo "📍 Received branch: $BRANCH_NAME" >&2

  exit 1
fi

echo "✅ Branch name validation passed: $BRANCH_NAME"
