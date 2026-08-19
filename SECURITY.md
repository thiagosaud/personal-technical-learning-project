# Security Policy

## Supported Versions

Security fixes are applied exclusively to actively maintained branches and validated release tags.

| Version               | Supported |
| --------------------- | --------- |
| `main`                | Yes       |
| Latest stable release | Yes       |
| Older releases        | No        |

---

## Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub issues, pull requests, or public discussions.**

### Preferred Channel

Use GitHub's private vulnerability reporting mechanism directly through the repository dashboard:

```text
GitHub → Security → Advisories → Report a vulnerability
```

If private vulnerability reporting is unavailable, contact the repository maintainers through the secure private channels established under the project organization. Do not disclose vulnerability details publicly before the maintainers have investigated and provided a verified remediation patch.

---

## What to Include

A useful security report must contain:

- Vulnerability summary and high-level architectural impact.
- Affected microservice component or folder topology.
- Affected version, commit hash, or package lock reference.
- Detailed step-by-step reproduction instructions.
- Expected behavior vs. actual behavior observed.
- Common Vulnerability Scoring System (CVSS) matrix or security impact analysis.
- Proof of Concept (PoC) code streams when fully safe to execute.
- Suggested cryptographic mitigation or configuration patch when available.

**Never include real production credentials, raw API keys, environment secret tokens, or private customer data.**

---

## Security Development Requirements

The monorepo enforces automated multi-layered security gates at the local hook layer and remote CI automation workers.

### Local Secret Detection (Gitleaks Engine)

```bash
pnpm run security:secrets
```

### Static Application Security Testing — SAST (Semgrep Infrastructure)

```bash
pnpm run lint:security:semgrep
```

### Python Core Security & Supply-Chain Auditing (Bandit Infrastructure)

```bash
pnpm run lint:security:py
```

### Full Local Continuous Integration Gate Simulation (Act Engine)

```bash
pnpm run ci:local:all
```

---

## Secret Governance

Never commit cryptographic material, environment files, or live production configurations to the source tree.

### Forbidden Material

- Active cloud infrastructure access tokens or API keys.
- Private encryption keys, certificates, or asymmetric pairs.
- Unencrypted passwords, database strings, or session secrets.
- Active or local configurations representing `.env` or `.env.*` targets.

Always maintain a decoupled `.env.example` deployment reference containing dummy parameter properties for environment variable documentation layout maps.

---

## AI & LLM Operational Security

AI data pipelines, model artifacts, and telemetry stacks are treated as high-risk trust boundaries under strict OWASP Top 10 for LLM guidelines.

### Data Protection Matrix

- Prevent leakage of architectural system prompts, proprietary data ingestion pipelines, or model weights through evaluation logs or system telemetry.
- Block unintended data exposure from third-party model inference endpoints or agent tooling logs.
- Guard against **Prompt Injection** and **Indirect Prompt Injection** vectors targeting multi-source vehicle spec extractors.
- Strictly validate down-stream data parsing to avoid **Insecure Output Handling** anomalies originating from uncontrolled model completions.

---

## Model Context Protocol (MCP) Safety

MCP integrations represent external execution boundaries and must operate under zero-trust authorization layers.

### Evaluation Requirements

Before activating any local or remote MCP server infrastructure, you must thoroughly evaluate:

- Authentication layers and scoped operational capability restrictions.
- Network boundary isolation parameters and directory system access bounds.
- Up-stream supply-chain tracking provenance for imported server binaries.
- Error handling behavior to prevent data dumps upon runtime communication failures.

All active MCP configuration parameters containing connection tokens must remain externalized and must never be staged into Git version control. Tools must execute exclusively with the lowest privilege access footprint required.

---

## Dependency & Pipeline Quality Gates

- **Supply-Chain Verification**: Every introduced third-party package must pass evaluation regarding active community maintenance, verified provenance tracking, licensing compliance, and known vulnerability records.
- **Lockfile Enforcement**: Deterministic tracking via frozen lockfiles (`pnpm-lock.yaml` and `uv.lock`) is mandatory. Builds violating lock consistency will fail compilation gates instantly.
- **Suppression Invariants**: False positives must be handled exclusively through narrowly scoped, documented exception parameters (e.g., `# nosec` annotations or targeted inline ignore targets) rather than broad global rule suppressions.
