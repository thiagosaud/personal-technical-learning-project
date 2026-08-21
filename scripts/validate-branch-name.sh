#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

echo "🔍 Validating workspace branch naming conventions..."

# THE IDEMPOTENT FALLBACK FIX: If BRANCH_NAME is empty or missing,
# queries the local Git tree directly to extract the active branch name.
BRANCH_NAME="${BRANCH_NAME:-$(git branch --show-current)}"

# Ensure the BRANCH_NAME variable is present and not empty after fallback checks
if [ -z "${BRANCH_NAME}" ]; then
  echo "❌ Error: BRANCH_NAME environment variable is required and Git context is missing." >&2
  exit 1
fi

PACKAGE_JSON_PATH="package.json"

if [ ! -f "$PACKAGE_JSON_PATH" ]; then
  echo "❌ Error: package.json file could not be found at root." >&2
  exit 1
fi

# (O restante do script se mantém exatamente igual ao que blindamos anteriormente)
CONFIG_PATTERN=$(node -e "
  try {
    const pkg = require('./$PACKAGE_JSON_PATH');
    const cfg = pkg['validate-branch-name'];
    if (!cfg || !cfg.pattern) throw new Error();
    console.log(cfg.pattern);
  } catch {
    console.log('MISSING_CONFIG');
  }
" 2>/dev/null || echo "MISSING_CONFIG")

if [ "$CONFIG_PATTERN" = "MISSING_CONFIG" ]; then
  echo "❌ Error: validate-branch-name configuration or pattern is missing from package.json." >&2
  exit 1
fi

if [[ ! "$BRANCH_NAME" =~ $CONFIG_PATTERN ]]; then
  echo "❌ Error: Branch verification failed!" >&2
  node -e "
    const pkg = require('./$PACKAGE_JSON_PATH');
    console.error(pkg['validate-branch-name'].errorMsg || 'Invalid branch name standard.');
  " 2>/dev/null
  exit 1
fi

echo "✅ Branch name validation passed: $BRANCH_NAME"
