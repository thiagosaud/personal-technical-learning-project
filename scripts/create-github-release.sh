#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

echo "🔍 Evaluating package version states..."

# Validate presence of necessary system tools before execution
if ! command -v gh &> /dev/null; then
  echo "❌ Error: GitHub CLI ('gh') is not installed or available in PATH." >&2
  exit 1
fi

# Read current package version from package.json utilizing native Node evaluation
CURRENT_VERSION=$(node -e "console.log(require('./package.json').version);")

# Safely query the package version from the parent commit (HEAD^)
# Capturing the raw string inside an export context safeguards command execution
if ! PREVIOUS_VERSION=$(git show HEAD^:package.json 2>/dev/null | node -e "
  const fs = require('fs');
  try {
    const input = fs.readFileSync(0, 'utf-8');
    if (!input) process.exit(1);
    console.log(JSON.parse(input).version);
  } catch {
    process.exit(1);
  }
"); then
  echo "⚠️ No parent package.json found (shallow history or first commit); skipping release creation."
  exit 0
fi

if [ "$CURRENT_VERSION" = "$PREVIOUS_VERSION" ]; then
  echo "Package version did not change ($CURRENT_VERSION); skipping release creation."
  exit 0
fi

# Linear SemVer syntax check split simulation to prevent processing errors
BASE_VERSION="${CURRENT_VERSION%%-*}"
if [[ ! "$BASE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ Invalid package version syntax: $CURRENT_VERSION" >&2
  exit 1
fi

TAG="v${CURRENT_VERSION}"

# THE DEFINTIVE GH SERVICE FIX: Explicitly evaluate exit status codes
# to decouple 'set -e' constraints from the network discovery validation probe.
INITIAL_EXIT_CODE=0
gh release view "$TAG" >/dev/null 2>&1 || INITIAL_EXIT_CODE=$?

if [ "$INITIAL_EXIT_CODE" -eq 0 ]; then
  echo "ℹ️ Release ${TAG} already exists; skipping deployment."
  exit 0
elif [ "$INITIAL_EXIT_CODE" -ne 1 ]; then
  # Exit code 1 means 'Release not found' (expected). Any other code (like 4, 127)
  # implies authentication failure or networking infrastructure crashes.
  echo "❌ Error: GitHub CLI failed with unexpected exit code: $INITIAL_EXIT_CODE. Verify GH_TOKEN configurations." >&2
  exit "$INITIAL_EXIT_CODE"
fi

echo "🚀 Preparing deployment parameters for GitHub Release ${TAG}..."

# Determine if this run targets a prerelease version string
RELEASE_TARGET="${GITHUB_SHA:-HEAD}"
RELEASE_ARGS=("release" "create" "$TAG" "--target" "$RELEASE_TARGET" "--title" "$TAG" "--generate-notes")

if [[ "$CURRENT_VERSION" == *"-"* ]]; then
  RELEASE_ARGS+=("--prerelease")
fi

# Execute the final release deployment pipeline
gh "${RELEASE_ARGS[@]}"

echo "✅ GitHub Release ${TAG} created successfully!"
