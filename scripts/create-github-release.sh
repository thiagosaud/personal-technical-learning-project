#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

echo "🔍 Evaluating package version states..."

# Read current package version from package.json utilizing native Node evaluation
CURRENT_VERSION=$(node -e "console.log(require('./package.json').version);")

# Safely query the package version from the parent commit (HEAD^)
# Overriding the pipe failure pattern ensures the script handles shallow checkouts gracefully
if ! PREVIOUS_PACKAGE_JSON=$(git show HEAD^:package.json 2>/dev/null); then
  echo "⚠️ No parent package.json found (shallow history or first commit); skipping release creation."
  exit 0
fi

# Extract the previous version from the captured json string
PREVIOUS_VERSION=$(node -e "console.log(($PREVIOUS_PACKAGE_JSON).version);")

if [ "$CURRENT_VERSION" = "$PREVIOUS_VERSION" ]; then
  echo "Package version did not change ($CURRENT_VERSION); skipping release creation."
  exit 0
fi

# Linear SemVer syntax check split simulation to prevent processing errors
BASE_VERSION="${CURRENT_VERSION%%-*}"
if [[ ! "$BASE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ Invalid package version syntax: $CURRENT_VERSION"
  exit 1
fi

TAG="v${CURRENT_VERSION}"

# THE CRITICAL FIX: Changing "|| false" to "|| true" safeguards the execution context.
# If the release does not exist, gh returns exit 1, "|| true" forces success,
# and the "if" condition safely evaluates to false, letting the script proceed.
if gh release view "$TAG" >/dev/null 2>&1 || true; then
  # We must explicitly check if the command ACTUALLY succeeded to know if the release exists
  if gh release view "$TAG" >/dev/null 2>&1; then
    echo "ℹ️ Release ${TAG} already exists; skipping deployment."
    exit 0
  fi
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
