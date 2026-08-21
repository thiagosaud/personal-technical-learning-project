#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

# Ensure the BRANCH_NAME environment variable is present and not empty
# This handles the 'BRANCH_NAME is required' logical condition safely
if [ -z "${BRANCH_NAME:-}" ]; then
  echo "❌ Error: BRANCH_NAME environment variable is required." >&2
  exit 1
fi

# Locate the root package.json file safely relative to the script execution context
PACKAGE_JSON_PATH="package.json"

if [ ! -f "$PACKAGE_JSON_PATH" ]; then
  echo "❌ Error: package.json file could not be found at root." >&2
  exit 1
fi

# Safely extract the configuration blocks from package.json using native inline Node evaluation
# This avoids installing heavy JSON parsing tools like 'jq' inside the CI agent
CONFIG_PATTERN=$(node -e "
  const pkg = require('./$PACKAGE_JSON_PATH');
  const cfg = pkg['validate-branch-name'];
  if (!cfg || !cfg.pattern) process.exit(1);
  console.log(cfg.pattern);
" 2>/dev/null || echo "MISSING_CONFIG")

CONFIG_ERROR_MSG=$(node -e "
  const pkg = require('./$PACKAGE_JSON_PATH');
  const cfg = pkg['validate-branch-name'];
  if (!cfg || !cfg.errorMsg) process.exit(1);
  console.log(cfg.errorMsg);
" 2>/dev/null || echo "Branch name validation failed.")

if [ "$CONFIG_PATTERN" = "MISSING_CONFIG" ]; then
  echo "❌ Error: validate-branch-name configuration or pattern is missing from package.json." >&2
  exit 1
fi

# Execute strict structural evaluation of the branch string against the regex pattern
# This matches the behavior of RegExp.prototype.test() without ReDoS vulnerabilities
if [[ ! "$BRANCH_NAME" =~ $CONFIG_PATTERN ]]; then
  echo "❌ Error: $CONFIG_ERROR_MSG" >&2
  exit 1
fi

echo "✅ Branch name validation passed: $BRANCH_NAME"
