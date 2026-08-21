#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enforce strict variable lookups
set -u

echo "--------------------------------------------"
echo "⚓ Initializing Automated Monorepo Setup"
echo "--------------------------------------------"

# ==========================================
# 1. PREREQUISITE VALIDATION (Node, PNPM & UV)
# ==========================================
if ! command -v node &> /dev/null; then
    echo "❌ Error: 'node' runtime is not installed."
    exit 1
fi

if ! command -v pnpm &> /dev/null; then
    echo "❌ Error: 'pnpm' package manager is not installed."
    echo "💡 Install it globally by running: npm install -g pnpm"
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "❌ Error: 'uv' package manager is not installed."
    echo "💡 Install it by running: curl -LsSf https://astral.sh | sh"
    exit 1
fi

echo "✓ Core runtimes detected: Node.js, pnpm, and uv."

# ==========================================
# 2. SAFETY CLEANUP
# ==========================================
echo "🧹 Cleaning up legacy caches and environment residues..."

if [ -d ".venv" ]; then
    RANDOM_ID=$((RANDOM))
    mv .venv ".venv_stale_${RANDOM_ID}" || true
    rm -rf ".venv_stale_${RANDOM_ID}" || true
fi

rm -rf .uv || true

if [ -d "projects" ]; then
    find projects -type d -name "node_modules" -prune -o -type d -name ".venv" -exec rm -rf {} + || true
fi

# ==========================================
# 3. NODE WORKSPACE INSTALLATION
# ==========================================
echo "📦 Installing Node.js workspace dependencies via pnpm..."
pnpm install --frozen-lockfile

# ==========================================
# 4. PYTHON WORKSPACE RESOLUTION & SYNC
# ==========================================
echo "📦 Generating unified Python environment lockfile (uv.lock)..."
uv lock

echo "🚀 Installing Python dependencies and linking workspace subprojects..."
uv sync --all-packages

# ==========================================
# 5. MONOREPO QUALITY MATRIX VERIFICATION
# ==========================================
echo "🛡️ Executing unifed quality verification pipeline (lint:all:check)..."

# Running sequential validations ensures strict error propagation across commands
pnpm run lint:commit \
  && pnpm run lint:branch \
  && pnpm run lint:markdown \
  && pnpm run lint:code:js \
  && pnpm run lint:code:py \
  && pnpm run lint:security:py \
  && pnpm run lint:security:semgrep \
  && pnpm run eslint \
  && pnpm run security:secrets

echo "--------------------------------------------"
echo "✅ Monorepo environment configured and validated successfully!"
echo "💡 All security checks and linters passed perfectly."
echo "--------------------------------------------"
