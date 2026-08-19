# Contributing and Engineering Governance Guidelines

## Versioning & Release Architecture

This polyglot monorepo enforces an independent, decoupled versioning strategy managed automatically via the Changesets engine. Version increments strictly adhere to the **Semantic Versioning (MAJOR.MINOR.PATCH)** protocol under two strict operational constraints:

### Rule 1: Root Infrastructure Scoped Modifications

When modifications target global root configurations, base development toolchains, or core platform security invariants:

- The version bump is restricted exclusively to the workspace root `package.json`.
- Changes are compiled directly into the global `CHANGELOG.md` under the root scope.
- Subproject member versions remain completely frozen and unaffected.

### Rule 2: Subproject Analytical Scoped Modifications

When modifications target specific standalone project directory structures (e.g., `projects/ai-engineer/.../case-byd`):

- The version bump is restricted exclusively to that specific target subproject package manifest layer.
- Resulting release descriptions are automatically prepended to the global `CHANGELOG.md` specifying the project package scope boundary (e.g., `### Added - @projects/case-byd`).
- The global monorepo root package version remains completely frozen and unaffected.

---

## Changelog & Documentation Guidelines

- All active modifications must be staged under the `[Unreleased]` block using the localized `pnpm run changeset` execution loop during branch development tasks.
- Do not utilize the changelog as a dumping ground for raw Git commit message histories.
- Avoid technical syntax references like "fixed variable X" or "updated line Y". Always capture high-level resulting behaviors or core systemic engineering impacts.

### Categories Directory

- `Added`: For clean innovative capabilities or raw analytical modules introduced.
- `Changed`: For changes in existing system features or model implementations.
- `Deprecated`: For soon-to-be removed operational endpoints or functions.
- `Removed`: For deprecated capabilities permanently severed from production.
- `Fixed`: For localized error mitigations or structural bug resolution sweeps.
- `Security`: In case of targeted package vulnerability patches or secret isolation blocks.
