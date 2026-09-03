# personal-technical-learning-project 📚

[![CI](https://github.com/thiagosaud/personal-technical-learning-project/actions/workflows/ci.yml/badge.svg)](https://github.com/thiagosaud/personal-technical-learning-project/actions/workflows/ci.yml)
[![Security](https://img.shields.io/badge/security-Gitleaks%20%7C%20Bandit%20%7C%20Semgrep-2ea44f)](SECURITY.md)
[![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Node.js](https://img.shields.io/badge/node.js-%3E%3D24.14.0-339933?logo=node.js&logoColor=white)](package.json)
[![pnpm](https://img.shields.io/badge/pnpm-11.22.0-F69220?logo=pnpm&logoColor=white)](package.json)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Personal repository for technical studies in software engineering, artificial
intelligence, machine learning, automation, security, and polyglot project governance.

The repository is structured as a private polyglot monorepo where the root layer
provides shared development standards, automation, quality gates, security
controls, CI/CD workflows, and release governance for independent technical
learning projects.

Made with curiosity, code, and many technical experiments 🧠

## 🎯 Goals

- Organize experiments and technical studies into independent projects.
- Apply modern software engineering and DevOps practices.
- Maintain consistent quality, security, and documentation standards.
- Centralize repository-wide development tooling and governance.
- Automate validation, testing, security analysis, versioning, and releases.
- Document practical implementations of machine learning and data engineering.
- Provide reproducible local and CI environments for polyglot development.

## 🏗️ Repository Role

The root package is intentionally configured as a **private workspace package**.
It is not intended to be published as an npm package.

Its primary responsibility is to provide the integration and governance layer
for the repository:

    Developer
       │
       ├── pnpm / uv
       │       └── Dependency management
       │
       ├── Lefthook
       │       └── Local Git quality gates
       │
       ├── ESLint / Prettier / Ruff / Markdownlint
       │       └── Code and documentation quality
       │
       ├── Gitleaks / Bandit / Semgrep
       │       └── Security and SAST
       │
       ├── Pytest
       │       └── Python test execution
       │
       ├── Act
       │       └── Local GitHub Actions validation
       │
       └── Changesets
               └── Versioning and release governance

## 🗂️ Structure

    personal-technical-learning-project/
    ├── CHANGELOG.md                                    # Repository-level change history and release records
    ├── CODE_OF_CONDUCT.md                              # Expected standards of behavior for project participants
    ├── CONTRIBUTING.md                                 # Contribution workflow, development standards, and repository governance
    ├── LICENSE                                         # MIT license terms governing the use and distribution of the repository
    ├── README.md                                       # Monorepo overview, architecture, development workflow, and operating guide
    ├── SECURITY.md                                     # Security policy and vulnerability reporting procedures
    │
    ├── .actrc                                          # Act configuration for running GitHub Actions workflows locally
    ├── .bandit.yaml                                    # Bandit configuration for Python security analysis
    ├── .editorconfig                                   # Editor-independent coding and formatting conventions
    ├── .gitignore                                      # Git exclusion rules for local, generated, and environment-specific files
    ├── .git-blame-ignore-revs                          # Git revisions excluded from blame history to reduce formatting-noise impact
    ├── .gitleaks.toml                                  # Gitleaks rules and configuration for secret detection
    ├── .markdownlint.json                              # Markdownlint rules enforcing repository documentation standards
    ├── .markdownlintignore                             # Markdown files and paths excluded from Markdownlint validation
    ├── .npmrc                                          # npm and pnpm client configuration and package-management behavior
    ├── .prettierignore                                 # Files and paths excluded from Prettier formatting
    ├── .prettierrc.mjs                                 # Prettier formatting rules for supported repository files
    ├── .semgrep.yaml                                   # Repository-specific Semgrep rules and static analysis configuration
    ├── eslint.config.mjs                               # Root ESLint flat configuration for JavaScript and TypeScript analysis
    ├── commitlint.config.mjs                           # Commit message conventions and Commitlint validation rules
    ├── lefthook.yml                                    # Local Git hook definitions for automated quality and governance checks
    ├── package.json                                    # Private root workspace metadata, package manager configuration, and development scripts
    ├── pnpm-lock.yaml                                  # Deterministic lockfile for resolved JavaScript and Node.js dependencies
    ├── pnpm-workspace.yaml                             # pnpm workspace membership and dependency supply-chain policies
    ├── pyproject.toml                                  # Root Python project metadata, tooling configuration, and test settings
    ├── sonar-project.properties                        # SonarQube project configuration and static analysis scope
    ├── uv.lock                                         # Deterministic lockfile for root Python development dependencies
    │
    ├── .pytest_cache/                                  # Pytest runtime cache generated during test execution
    ├── .ruff_cache/                                    # Ruff analysis cache generated during linting
    ├── .venv/                                          # Local Python virtual environment managed by uv
    ├── htmlcov/                                        # Locally generated HTML coverage report
    ├── node_modules/                                   # Locally installed Node.js dependencies generated by pnpm
    │
    ├── .vscode/                                        # Shared VS Code workspace configuration for consistent local development
    │   ├── extensions.json                             # Recommended VS Code extensions for repository development
    │   ├── launch.json                                 # Debugging and application launch configurations
    │   └── settings.json                               # Workspace-specific editor, language, and tooling settings
    │
    ├── .github/                                        # GitHub repository governance, automation, and collaboration configuration
    │   ├── ISSUE_TEMPLATE/                             # Standardized issue templates and structured issue forms
    │   ├── PULL_REQUEST_TEMPLATE.md                    # Pull request structure, review checklist, and contribution requirements
    │   ├── dependabot.yml                              # Automated dependency update and security maintenance configuration
    │   └── workflows/                                  # GitHub Actions workflows for CI, releases, and scheduled security validation
    │       ├── ci.yml                                  # Continuous integration quality gates for repository changes
    │       ├── release.yml                             # Changesets-based package versioning and release automation
    │
    ├── .changeset/                                     # Changesets release metadata and versioning state
    │   ├── README.md                                   # Changesets CLI-generated usage documentation for repository contributors
    │   └── config.json                                 # Changesets configuration for versioning, changelogs, branches, and package access
    │
    ├── scripts/                                        # Repository automation, validation, and development-support scripts
    │   ├── setup.sh                                    # Development environment bootstrap and workspace synchronization
    │   ├── validate-branch-name.sh                     # Git branch naming validation script
    │   ├── validate-commit-message.sh                  # Git Commit message validation script
    │
    └── projects/                                       # Independent technical learning projects and applied experiments
        └── ai-engineer/                                # AI engineering studies covering machine/deep learning and related disciplines
            ├── deep-learning/                          # Deep learning experiments, implementations, and case studies
            │   └── generate-text-with-transform/       # Transformer-based text-generation experiments
            │       └── case-shakespeare/               # Shakespeare corpus text-generation case study
            │
            ├── machine-learning/                       # Machine learning experiments, implementations, and case studies
                └── linear-and-logistical-regression/   # Regression-focused studies covering linear and logistic models
                    └── case-byd/                       # Applied BYD vehicle dataset, ML pipeline, and visualization case study

The tree describes the repository filesystem relevant to development and
governance.

Local environments and generated artifacts such as `.git/`, `node_modules/`,
`.venv/`, `.pytest_cache/`, `.ruff_cache/`, `htmlcov/`, `__pycache__/`, and
generated project artifacts are excluded from version control and recreated
as required.

## 🧰 Root Technology Stack

| Area                          | Technology             | Responsibility                                       |
| ----------------------------- | ---------------------- | ---------------------------------------------------- |
| Runtime                       | Node.js `>=24.14.0`    | JavaScript and TypeScript tooling                    |
| Package manager               | pnpm `11.22.0`         | Node.js dependency and workspace management          |
| Python environment            | uv                     | Python dependency and virtual environment management |
| Python                        | `>=3.12`               | Python tooling and project execution                 |
| Git hooks                     | Lefthook               | Local repository quality gates                       |
| JavaScript/TypeScript linting | ESLint                 | Static code analysis                                 |
| Python linting                | Ruff                   | Python linting                                       |
| Formatting                    | Prettier / Ruff Format | Consistent source formatting                         |
| Documentation linting         | Markdownlint           | Markdown quality validation                          |
| Commit validation             | Commitlint             | Conventional commit message enforcement              |
| Branch validation             | validate-branch-name   | Git branch naming enforcement                        |
| Testing                       | Pytest                 | Python unit testing                                  |
| Security                      | Gitleaks               | Secret detection                                     |
| Security                      | Bandit                 | Python security analysis                             |
| SAST                          | Semgrep                | Static application security testing                  |
| Code quality                  | SonarQube              | Static analysis and quality inspection               |
| CI/CD                         | GitHub Actions         | Automated repository workflows                       |
| Local CI                      | Act                    | Local execution of GitHub Actions workflows          |
| Release management            | Changesets             | Versioning and release metadata                      |

## 📦 Package Configuration

The root `package.json` defines the repository-wide JavaScript toolchain and
automation layer.

### Package identity

| Property     | Value                                 |
| ------------ | ------------------------------------- |
| Package name | `personal-technical-learning-project` |
| Visibility   | Private                               |
| License      | MIT                                   |

The package is marked as `"private": true`, therefore the root workspace is
not intended for npm publication.

### Branch naming policy

Branches must follow the repository-defined pattern:

    <type>/<short-description-in-kebab-case>

Allowed types:

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

Example:

    feat/linear-regression-byd

The validation rule is defined centrally in `package.json` and executed through
the repository branch validation tooling.

## 🚀 Setup

### Prerequisites

The root toolchain requires:

- Node.js `>=24.14.0`.
- pnpm `>=11.22.0`.
- Python `>=3.12`.
- uv.
- Git.
- Docker when required by individual workflows or projects.
- Act when executing GitHub Actions locally.

The authoritative Node.js and pnpm requirements are defined in
[`package.json`](package.json). Python project requirements are defined in
[`pyproject.toml`](pyproject.toml).

### Installation

Bootstrap the development environment from the repository root:

    pnpm infra:script:setup

The workspace dependency installation can also be executed explicitly:

    pnpm infra:install:global:workspace:dependencies

Python development dependencies can be synchronized with:

    pnpm infra:install:global:python:dependencies

## ✅ Quality Gates

All repository-wide quality gates must be executed from the **monorepo root**
so that the shared configuration and toolchain are applied consistently.

### Complete validation

    pnpm lint:check:all

The aggregate lint command validates:

1. Git branch naming.
2. ESLint.
3. Commit message conventions.
4. Markdown.
5. Prettier formatting.
6. Ruff linting.

### Automatic fixes

    pnpm lint:fix:all

This applies the configured automatic fixes for Markdown, Python linting,
ESLint, Prettier, and Python formatting.

### Python unit tests

    pnpm test:unit:py

Or through the aggregate test command:

    pnpm test:unit:all

### Security validation

Run all configured SAST and secret-detection checks:

    pnpm test:sast:all

Individual scanners can also be executed independently:

    pnpm test:sast:secrets
    pnpm test:sast:semgrep
    pnpm test:sast:py

## 🔐 Security

The repository applies multiple independent security controls:

- **Gitleaks** for secret detection.
- **Bandit** for Python security analysis.
- **Semgrep** for SAST.
- **SonarQube** for code-quality and static analysis.
- **Dependabot** for dependency update automation.
- **Lockfiles** for deterministic dependency resolution.
- **Scheduled GitHub Actions** for recurring security validation.

See the [security policy](SECURITY.md).

## 🪝 Git Hooks

Lefthook provides local Git hooks through:

    pnpm prepare

The `prepare` lifecycle script installs the repository Git hooks after
dependencies are installed.

These hooks enforce repository standards according to the definitions in
[`lefthook.yml`](lefthook.yml).

## 🧩 Projects

| Project                                                                                               | Description                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [case-byd](projects/ai-engineer/machine-learning/linear-and-logistical-regression/case-byd/README.md) | Educational ML pipeline with ETL, simple linear regression, multiple linear regression, logistic regression, and visualizations applied to BYD vehicle specifications |

Individual projects maintain their own README files, technical scope,
experiments, datasets, model descriptions, and project-specific instructions.

## 🤝 Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before contributing.

Contributions are expected to follow the repository's:

- branch naming conventions;
- conventional commit conventions;
- formatting rules;
- linting rules;
- Markdown standards;
- security checks;
- test requirements;
- Changesets release policy where applicable.

## 📦 Versioning

Versioning uses Changesets and follows Semantic Versioning.

Changesets records release intent separately from the actual versioning operation:
contributors create changesets first, and the release process later consumes
them to update package versions and changelogs.

### Versioning lifecycle

#### 1. Create a changeset

After implementing a releasable change:

    pnpm infra:release:changeset

The interactive CLI asks which workspace package changed and which SemVer
increment applies. It then creates a Markdown changeset inside `.changeset/`.

The selected increment should reflect the public impact of the change:

| Increment | Use when                                               |
| --------- | ------------------------------------------------------ |
| `patch`   | Bug fixes or backward-compatible internal improvements |
| `minor`   | New backward-compatible functionality                  |
| `major`   | Breaking changes to the package contract               |

Not every repository change requires a changeset. Changesets is primarily a
release and changelog mechanism.

#### 2. Inspect changesets relative to `main`

    pnpm infra:release:changeset:auto

This executes the configured Changesets command with `--since main`.

It is intended for reviewing release scope and does not publish a release.

#### 3. Enter prerelease mode

    pnpm infra:release:changeset:pre-enter

The repository is configured to use the `rc` prerelease tag.

#### 4. Exit prerelease mode

The current `package.json` exposes:

    pnpm infra:realease:changeset:pre-exit

> **Note:** `realease` is currently misspelled in the script name. The README
> documents the exact command currently defined in `package.json`. Consider
> renaming it to `infra:release:changeset:pre-exit` in a separate cleanup change.

#### 5. Version packages

The repository's versioning script is:

    pnpm infra:release:changeset:version:packages

It executes the equivalent of:

    changeset version
    pnpm install --no-frozen-lockfile

`changeset version` consumes pending changesets, updates package versions and
dependencies, and writes changelog entries.

The lockfile is then refreshed because package manifest versions may have
changed.

Review the resulting working-tree changes before committing them.

#### 6. GitHub release workflow

The release workflow is defined in
[`.github/workflows/release.yml`](.github/workflows/release.yml).

The workflow is responsible for automating the repository release process
using the Changesets configuration and repository release tooling.

The workflow itself remains the authoritative source for its exact CI
implementation.

## 🧪 Local GitHub Actions

GitHub Actions workflows can be executed locally through Act.

Run the CI workflow:

    pnpm infra:test:workflow:ci

The Act configuration is centralized in [`.actrc`](.actrc).

## 🛠️ Available Package Scripts

All scripts below are defined in [`package.json`](package.json).

Run them from the repository root using:

    pnpm <script>

### Installation and infrastructure

| Script                                        | Responsibility                                                       |
| --------------------------------------------- | -------------------------------------------------------------------- |
| `prepare`                                     | Installs Lefthook Git hooks through the package lifecycle            |
| `infra:install:global:workspace:dependencies` | Installs locked workspace dependencies with pnpm                     |
| `infra:install:global:python:dependencies`    | Synchronizes frozen Python dependencies across the workspace with uv |
| `infra:script:setup`                          | Bootstraps the local development environment                         |
| `infra:script:lint:check:branchname`          | Executes the repository branch-name validation script                |
| `infra:script:release:github`                 | Executes the GitHub release automation script                        |

### Changesets and releases

| Script                                     | Responsibility                                             |
| ------------------------------------------ | ---------------------------------------------------------- |
| `infra:release:changeset`                  | Opens the interactive Changesets CLI                       |
| `infra:release:changeset:auto`             | Runs Changesets relative to `main`                         |
| `infra:release:changeset:pre-enter`        | Enters `rc` prerelease mode                                |
| `infra:realease:changeset:pre-exit`        | Exits `rc` prerelease mode                                 |
| `infra:release:changeset:version:packages` | Applies pending changesets and refreshes the pnpm lockfile |

### Formatting

| Script           | Responsibility                                      |
| ---------------- | --------------------------------------------------- |
| `format:files`   | Formats repository files with Prettier              |
| `format:code:py` | Formats Python files with Ruff                      |
| `format:all`     | Runs JavaScript/configuration and Python formatting |

### Security and SAST

| Script              | Responsibility                                            |
| ------------------- | --------------------------------------------------------- |
| `test:sast:secrets` | Scans the repository for secrets with Gitleaks            |
| `test:sast:semgrep` | Runs Semgrep with repository and `p/security-audit` rules |
| `test:sast:py`      | Runs Bandit against Python source                         |
| `test:sast:all`     | Runs Gitleaks, Semgrep, and Bandit sequentially           |

### Testing

| Script          | Responsibility                                              |
| --------------- | ----------------------------------------------------------- |
| `test:unit:py`  | Runs the Python Pytest suite with the frozen uv environment |
| `test:unit:all` | Runs all configured unit-test suites                        |

### ESLint

| Script         | Responsibility                         |
| -------------- | -------------------------------------- |
| `eslint:check` | Runs ESLint with zero allowed warnings |
| `eslint:fix`   | Runs ESLint with automatic fixes       |

### Repository linting

| Script                  | Responsibility                                             |
| ----------------------- | ---------------------------------------------------------- |
| `lint:check:branchname` | Validates the current Git branch name                      |
| `lint:check:commit`     | Validates the current commit message with Commitlint       |
| `lint:check:markdown`   | Validates Markdown with Markdownlint                       |
| `lint:check:code:js`    | Checks repository formatting with Prettier                 |
| `lint:check:code:py`    | Runs Ruff linting                                          |
| `lint:fix:markdown`     | Applies Markdownlint automatic fixes                       |
| `lint:fix:code:py`      | Applies Ruff automatic fixes                               |
| `lint:check:all`        | Runs the complete repository linting gate                  |
| `lint:fix:all`          | Applies all configured automatic lint and formatting fixes |

## 📄 License

Distributed under the MIT license. See [LICENSE](LICENSE).
