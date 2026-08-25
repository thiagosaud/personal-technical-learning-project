#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

echo "--------------------------------------------------------"
echo "🔍 Validating codebase commit message semantics..."
echo "--------------------------------------------------------"

# THE ENTERPRISE HISTORY GATE: Bypasses static files during CI/CD execution points.
# Leverages official commitlint range parameters over active Git references.
if [ "${CI:-false}" = "true" ]; then
  echo "📦 CI Environment detected. Auditing incoming commit streams natively..."

  # If running over a Pull Request, check the entire incoming branch history range
  if [ -n "${COMMIT_FROM_SHA:-}" ] && [ -n "${COMMIT_TO_SHA:-}" ]; then
    echo "📊 Linting commit history range: ${COMMIT_FROM_SHA} -> ${COMMIT_TO_SHA}"
    echo "--------------------------------------------------------"
    echo "📝 Commits included in this range:"
    git log --pretty=format:"🔹 %h - %s (%an)" "${COMMIT_FROM_SHA}..${COMMIT_TO_SHA}"
    echo -e "\n--------------------------------------------------------"

    pnpm exec commitlint --from "$COMMIT_FROM_SHA" --to "$COMMIT_TO_SHA"
  else
    # Fallback for individual direct push pipelines in cloud environments
    echo "🎯 Linting last single historical commit point..."
    echo "--------------------------------------------------------"
    echo "📝 Target Commit Content:"
    git log -1 --pretty=format:"🔹 %h - %s (%an)%n%n%b" HEAD
    echo -e "\n--------------------------------------------------------"

    pnpm exec commitlint --from "HEAD~1" --to "HEAD"
  fi
else
  echo "💻 Local Environment detected. Reading message structure from active Git hook metadata..."
  echo "--------------------------------------------------------"
  echo "📝 Staged Commit Content:"

  # Read the staged message file provided by Git hooks or fallback to local log simulation
  if [ -f "./.git/COMMIT_EDITMSG" ]; then
    cat "./.git/COMMIT_EDITMSG"
  else
    git log -1 --pretty=format:"🔹 %h - %s (%an)%n%n%b" HEAD
  fi
  echo -e "\n--------------------------------------------------------"

  pnpm exec commitlint --edit
fi

echo "✅ Commit message validation passed successfully!"
echo "--------------------------------------------------------"
