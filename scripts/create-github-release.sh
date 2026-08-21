#!/usr/bin/env bash

set -euo pipefail

echo "🚀 Creating repository release..."

if ! command -v gh >/dev/null 2>&1; then
  echo "❌ GitHub CLI ('gh') is required." >&2
  exit 1
fi

if [ -z "${GH_TOKEN:-}" ]; then
  echo "❌ GH_TOKEN is required." >&2
  exit 1
fi

if [ ! -f ".release-version" ]; then
  echo "❌ .release-version not found." >&2
  exit 1
fi

REPOSITORY="${GITHUB_REPOSITORY}"
TARGET_SHA="${GITHUB_SHA}"

REPOSITORY_VERSION="$(tr -d '[:space:]' < .release-version)"

if [[ ! "$REPOSITORY_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ Invalid repository version: ${REPOSITORY_VERSION}" >&2
  exit 1
fi

TAG="v${REPOSITORY_VERSION}"

echo "Repository: ${REPOSITORY}"
echo "Version:    ${REPOSITORY_VERSION}"
echo "Tag:        ${TAG}"
echo "Commit:     ${TARGET_SHA}"

if gh release view "$TAG" \
  --repo "$REPOSITORY" \
  >/dev/null 2>&1; then

  echo "ℹ️ Release ${TAG} already exists."
  exit 0
fi

gh release create "$TAG" \
  --repo "$REPOSITORY" \
  --target "$TARGET_SHA" \
  --title "$TAG" \
  --generate-notes

echo "✅ Repository release ${TAG} created."
