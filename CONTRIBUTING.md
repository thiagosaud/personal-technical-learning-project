# Contributing and Engineering Governance Guidelines

Thank you for contributing to `personal-technical-learning-project`.

This repository is a polyglot technical-learning monorepo with shared
engineering governance, automated quality gates, security controls, and
independently versioned learning projects.

Contributions must preserve the repository's architectural boundaries,
reproducibility, security posture, and documentation standards.

---

## 1. Repository Governance

The repository is governed as a monorepo with two primary scopes:

1. **Root infrastructure**
   - Global development tooling.
   - CI/CD workflows.
   - Security controls.
   - Repository-wide linting and formatting.
   - Git hooks.
   - Release automation.
   - Shared Python and JavaScript/TypeScript tooling.

2. **Independent learning projects**
   - Self-contained technical studies.
   - Machine learning experiments.
   - Data engineering experiments.
   - AI engineering implementations.
   - Project-specific tests and documentation.

Changes should remain within the smallest appropriate scope.

---

## 2. Contribution Scope

### 2.1 Root Infrastructure

Changes to the repository root include, but are not limited to:

- `package.json`
- `pnpm-workspace.yaml`
- `pnpm-lock.yaml`
- `pyproject.toml`
- `uv.lock`
- `eslint.config.mjs`
- `.prettierrc.mjs`
- `.markdownlint.json`
- `.gitleaks.toml`
- `.semgrep.yaml`
- `.bandit.yaml`
- `lefthook.yml`
- `commitlint.config.mjs`
- `.github/workflows/`
- `scripts/`
- `.vscode/`
- repository-level documentation and governance files.

Root-level changes affect the shared development platform and therefore must
be evaluated for their impact on all workspace projects.

### 2.2 Independent Learning Projects

Independent projects are located below:

```text
projects/
└── <domain>/
    └── <technology-or-discipline>/
        └── <study-or-topic>/
            └── <project>/
```

For example:

```text
projects/
└── ai-engineer/
    └── machine-learning/
        └── linear-and-logistical-regression/
            └── case-byd/
```

Each project should maintain clear ownership of its:

- Source code.
- Tests.
- Documentation.
- Dataset definitions.
- Model implementations.
- Visualization logic.
- Project-specific dependencies.
- Project-specific release metadata.

A project must not introduce duplicated root-level governance tooling unless
there is a documented architectural reason.

Shared repository tooling should remain centralized whenever practical.

### 2.3 Scope Boundary

Before modifying a file, determine whether the change belongs to:

- the **repository governance layer**; or
- an **independent learning project**.

Avoid mixing unrelated root infrastructure changes with project-specific
functional changes in the same contribution unless the dependency between
them is explicit and necessary.

---

## 3. Development Environment

### 3.1 Required Toolchain

The canonical toolchain is defined by the repository configuration.

The required Node.js and pnpm versions are declared in `package.json`.

The repository currently requires:

```text
Node.js >= 24.14.0
pnpm >= 11.22.0
Python >= 3.12
```

The package manager is pinned through:

```json
"packageManager": "pnpm@11.22.0"
```

Python dependencies and development tools are managed through `uv`.

Do not manually modify lockfiles to bypass dependency resolution.

### 3.2 Installation

From the repository root:

```bash
pnpm infra:script:setup
```

The setup script is responsible for preparing the development environment
according to the repository's bootstrap conventions.

When dependency synchronization is required explicitly:

```bash
pnpm infra:install:global:workspace:dependencies
pnpm infra:install:global:python:dependencies
```

### 3.3 Local Git Hooks

Lefthook manages repository Git hooks.

The lifecycle command:

```bash
pnpm prepare
```

installs the configured hooks.

Contributors must not bypass repository hooks merely to make a change pass
locally.

If a hook fails, resolve the underlying issue before continuing whenever
possible.

---

## 4. Branching Strategy

Branch names must follow the repository's configured branch convention:

```text
<type>/<short-description-in-kebab-case>
```

Allowed types are:

```text
feat
fix
docs
style
refactor
perf
test
chore
ci
revert
release
```

Examples:

```text
feat/linear-regression-byd
fix/eslint-flat-config
docs/security-policy
test/byd-model-training
ci/act-workflow-validation
```

Validate the current branch with:

```bash
pnpm infra:script:lint:check:branchname
```

The repository also exposes:

```bash
pnpm lint:check:branchname
```

Do not use uppercase characters, spaces, underscores, or arbitrary branch
prefixes.

---

## 5. Commit Convention

Commit messages are validated with Commitlint and the conventional commit
configuration.

Validate a commit message with:

```bash
pnpm lint:check:commit
```

Use Conventional Commits, for example:

```text
feat: add logistic regression experiment
fix: correct BYD dataset validation
docs: update repository structure
refactor: isolate model training layer
test: add ETL validation coverage
ci: update workflow runtime
chore: update development tooling
```

The commit message should describe the intent and impact of the change rather
than implementation noise.

---

## 6. Code Quality

All repository quality gates should be executed from the repository root.

### 6.1 JavaScript / TypeScript

ESLint is the repository's JavaScript and TypeScript static analysis layer.

Run:

```bash
pnpm eslint:check
```

Automatic fixes:

```bash
pnpm eslint:fix
```

Prettier validation:

```bash
pnpm lint:check:code:js
```

Formatting:

```bash
pnpm format:files
```

### 6.2 Python

Ruff provides Python linting and formatting.

Run:

```bash
pnpm lint:check:code:py
```

Automatic lint fixes:

```bash
pnpm lint:fix:code:py
```

Python formatting:

```bash
pnpm format:code:py
```

### 6.3 Markdown

Markdown documentation is validated through Markdownlint.

Run:

```bash
pnpm lint:check:markdown
```

Automatic fixes:

```bash
pnpm lint:fix:markdown
```

### 6.4 Complete Lint Gate

Run the complete repository lint gate with:

```bash
pnpm lint:check:all
```

This validates the configured branch, ESLint, commit message, Markdown,
Prettier, and Ruff gates.

Automatic fixes are available through:

```bash
pnpm lint:fix:all
```

---

## 7. Testing

Python unit tests are executed with Pytest.

Run:

```bash
pnpm test:unit:py
```

Run all currently configured unit-test suites:

```bash
pnpm test:unit:all
```

Tests must be deterministic and must not depend on undeclared local state.

Generated test artifacts such as:

```text
.pytest_cache/
htmlcov/
__pycache__/
```

must not be committed.

---

## 8. Security Validation

Security checks are mandatory for repository changes.

### 8.1 Secret Detection

Run:

```bash
pnpm test:sast:secrets
```

Gitleaks must not report active credentials, tokens, private keys, or other
sensitive material.

### 8.2 Semgrep

Run:

```bash
pnpm test:sast:semgrep
```

The repository executes both its local rules and the configured
`p/security-audit` ruleset.

### 8.3 Bandit

Run:

```bash
pnpm test:sast:py
```

Bandit analyzes Python code according to `.bandit.yaml`.

### 8.4 Complete Security Gate

Run:

```bash
pnpm test:sast:all
```

Security findings must be addressed rather than suppressed broadly.

When an exception is technically justified, use the narrowest supported
suppression mechanism and document the reason.

Never commit:

- API keys.
- Access tokens.
- Passwords.
- Private keys.
- Production credentials.
- Customer data.
- `.env` files containing secrets.
- Authentication cookies or session secrets.

---

## 9. CI Validation

The repository uses GitHub Actions for remote validation.

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

The repository also supports local workflow execution through Act.

Run the local CI workflow with:

```bash
pnpm infra:test:workflow:ci
```

Local Act execution should be treated as a validation environment, not as a
replacement for GitHub Actions.

The final authority for repository integration remains the configured GitHub
Actions workflow.

---

## 10. Documentation Standards

Documentation must describe observable behavior, architectural intent, and
operational requirements.

Avoid documentation that merely reproduces implementation details.

### 10.1 README Files

Project-level README files should normally document:

- Purpose.
- Scope.
- Architecture.
- Structure.
- Requirements.
- Installation.
- Usage.
- Tests.
- Outputs or artifacts.
- Known limitations.

### 10.2 Structural Documentation

Directory trees should explain the responsibility of important files and
directories.

Prefer:

```text
scripts/
├── setup.sh                     # Development environment bootstrap
├── validate-branch-name.sh      # Branch naming validation
├── validate-commit-message.sh   # Git Commit message validation
```

over unexplained file listings.

### 10.3 Markdown Compliance

Markdown must pass the repository's Markdownlint configuration.

Do not introduce arbitrary HTML or formatting constructs when standard
Markdown provides an equivalent solution.

---

## 11. Dependency Management

Dependencies must be managed through the repository's declared package
managers.

JavaScript and Node.js dependencies:

```bash
pnpm
```

Python dependencies:

```bash
uv
```

Do not introduce another package manager without an explicit architectural
decision.

Lockfiles are part of the repository's reproducibility boundary:

```text
pnpm-lock.yaml
uv.lock
```

Dependency changes must be reviewed for:

- Security.
- Licensing.
- Maintenance status.
- Compatibility.
- Transitive dependency impact.
- Lockfile consistency.

---

## 12. Changesets and Versioning

The repository uses Changesets for release metadata and follows
[Semantic Versioning](https://semver.org).

Create a changeset with:

```bash
pnpm infra:release:changeset
```

The Changesets CLI records the intended release impact in a Markdown file
inside `.changeset/`.

### 12.1 Version Categories

| Increment | Use                                                 |
| --------- | --------------------------------------------------- |
| `patch`   | Backward-compatible fixes and internal improvements |
| `minor`   | Backward-compatible functionality                   |
| `major`   | Breaking changes to the public package contract     |

### 12.2 Preview Pending Changes

```bash
pnpm infra:release:changeset:auto
```

This evaluates changesets relative to `main`.

It does not publish a release.

### 12.3 Prerelease Mode

Enter prerelease mode:

```bash
pnpm infra:release:changeset:pre-enter
```

Exit prerelease mode:

```bash
pnpm infra:realease:changeset:pre-exit
```

The second command intentionally follows the currently configured repository
script name.

### 12.4 Version Packages

The repository release workflow uses:

```bash
pnpm infra:release:changeset:version:packages
```

This consumes pending changesets, updates package versions and changelogs, and
refreshes the pnpm lockfile.

Review the resulting working-tree changes before committing them.

---

## 13. Release Architecture

Root infrastructure and independent learning projects are versioned
independently.

### 13.1 Root Infrastructure Changes

When a change affects global infrastructure:

- The root package is the affected versioning scope.
- The root `package.json` version may be incremented.
- The root changelog records the release impact.
- Independent project package versions remain unchanged unless they are also
  explicitly affected.

Examples include:

- CI/CD architecture.
- Security tooling.
- Root package management.
- Shared linting.
- Repository-wide hooks.
- Release automation.

### 13.2 Independent Learning Project Changes

When a change is isolated to a learning project:

- Only the affected project package should receive the corresponding version
  increment.
- Unrelated root infrastructure remains unchanged.
- The release metadata must identify the affected project scope.

Examples include:

- New machine learning experiments.
- Changes to project-specific ETL.
- Project-specific model implementations.
- Project-specific visualizations.
- Project-specific tests.

---

## 14. Changelog Policy

Release documentation must communicate the resulting behavior or engineering
impact.

Use the following semantic categories:

- **Added** — New functionality or capability.
- **Changed** — Modification of existing behavior.
- **Deprecated** — Functionality scheduled for removal.
- **Removed** — Functionality permanently removed.
- **Fixed** — Corrective changes.
- **Security** — Security-related remediation.

Do not use the changelog as a raw Git commit history.

Avoid entries such as:

```text
Fixed variable X.
Changed line 42.
Updated function Y.
```

Prefer:

```text
Fixed validation failure when processing incomplete vehicle specifications.
```

---

## 15. Pull Requests

Pull requests should be focused and reviewable.

A pull request should clearly communicate:

1. What changed.
2. Why it changed.
3. Which scope is affected.
4. How the change was validated.
5. Whether release metadata is required.
6. Whether documentation was updated.
7. Whether security implications were evaluated.

Before opening a pull request, run the applicable gates.

For a broad repository change, the recommended final validation is:

```bash
pnpm lint:check:all
pnpm test:unit:all
pnpm test:sast:all
```

If applicable, also execute the relevant local GitHub Actions workflow with
Act.

---

## 16. Generated Files

Generated artifacts must not be committed unless explicitly required by the
project.

Examples include:

```text
node_modules/
.venv/
.pytest_cache/
.ruff_cache/
htmlcov/
__pycache__/
```

Machine-generated visualization artifacts should also remain outside version
control unless the project explicitly defines them as distributable assets.

---

## 17. Security-Sensitive Contributions

Security vulnerabilities must not be disclosed through public issues.

Follow the repository's [`SECURITY.md`](SECURITY.md) policy.

Contributors must immediately stop public discussion of a suspected
vulnerability and use the designated private reporting mechanism.

Do not include real credentials, secrets, or private customer information in:

- Issues.
- Pull requests.
- Commit messages.
- Test fixtures.
- Logs.
- Screenshots.
- Documentation.

---

## 18. AI, ML, and Data Contributions

Machine learning and AI contributions require additional attention to data
provenance, reproducibility, and evaluation methodology.

Contributors should document, where applicable:

- Dataset source.
- Data assumptions.
- Feature definitions.
- Target definitions.
- Training methodology.
- Evaluation methodology.
- Model limitations.
- Known data leakage risks.
- Reproducibility requirements.

Metrics generated from training data must not be represented as generalized
model performance.

For educational experiments, explicitly distinguish:

```text
training evaluation
```

from:

```text
unseen-data evaluation
```

when both are relevant.

---

## 19. Review Checklist

Before submitting a contribution, verify:

- [ ] The change is in the correct repository scope.
- [ ] Branch name follows the repository convention.
- [ ] Commit messages follow Conventional Commits.
- [ ] Code follows the configured formatter and linter rules.
- [ ] Relevant tests pass.
- [ ] Security scans pass.
- [ ] Documentation reflects the resulting behavior.
- [ ] No secrets or private data are included.
- [ ] Lockfiles are consistent.
- [ ] Generated artifacts are excluded.
- [ ] A Changeset was added when the change affects a versioned package.
- [ ] The Changeset uses the correct semantic version increment.
- [ ] The pull request clearly describes validation performed.

---

## 20. Final Quality Gate

Before requesting review, execute:

```bash
pnpm lint:check:all
pnpm test:unit:all
pnpm test:sast:all
```

If all gates pass, inspect the final Git diff:

```bash
git status
git diff --check
git diff
```

The contribution is ready for review only after the resulting diff has been
verified for correctness, scope, security, and documentation completeness.

---

## 21. Engineering Principle

The repository favors:

> Small changes, explicit boundaries, deterministic environments, automated
> validation, reproducible experiments, and documented engineering decisions.

When in doubt, prefer the smallest change that preserves the repository's
existing architectural and governance contracts.
