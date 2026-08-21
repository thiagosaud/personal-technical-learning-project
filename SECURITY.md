# Security Policy

## 1. Security Scope

This repository is a personal technical-learning monorepo containing software
engineering, artificial intelligence, machine learning, automation,
infrastructure, and security experiments.

Although some projects are educational, the repository follows production-grade
security practices whenever reasonably applicable.

Security controls cover:

- Source code.
- Dependencies.
- Build and development tooling.
- CI/CD workflows.
- Secrets and credentials.
- Generated artifacts.
- Local development environments.
- Machine learning and data-processing pipelines.
- External tool integrations.
- Model and AI-related data boundaries.

---

## 2. Supported Versions

Security fixes are applied to actively maintained repository branches and
release lines.

| Version / Branch      | Supported |
| --------------------- | --------- |
| `main`                | Yes       |
| Latest stable release | Yes       |
| Older releases        | No        |

Because this is a continuously evolving technical-learning repository,
unsupported historical versions may not receive security remediation.

---

## 3. Reporting a Vulnerability

**Do not report security vulnerabilities through public GitHub Issues,
Pull Requests, Discussions, or other public channels.**

Public disclosure can expose users and maintainers before a remediation is
available.

### 3.1 Preferred Reporting Channel

If GitHub Private Vulnerability Reporting is enabled for this repository, use
the repository's private vulnerability reporting interface:

```text
GitHub repository
→ Security / Security and quality
→ Advisories
→ Report a vulnerability
```

GitHub allows public repositories with private vulnerability reporting enabled
to receive vulnerability reports directly and privately from security
researchers. [oai_citation:1‡GitHub Docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)

Private vulnerability reporting is a GitHub repository feature and is separate
from this `SECURITY.md` document. [oai_citation:2‡GitHub Docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)

If the private reporting option is unavailable, follow the repository
maintainer's designated private security contact mechanism.

**Do not create a public issue merely to disclose vulnerability details.**

---

## 4. What to Include

A useful vulnerability report should contain enough information to reproduce,
assess, and remediate the issue without exposing unnecessary sensitive data.

Where applicable, include:

- Vulnerability summary.
- Affected component, package, workflow, or directory.
- Affected version, branch, or commit.
- Security impact.
- Preconditions required for exploitation.
- Step-by-step reproduction instructions.
- Expected behavior.
- Actual behavior.
- Proof of Concept (PoC), when safe to provide.
- Relevant logs or stack traces.
- Dependency information.
- Suggested remediation, if known.

For dependency vulnerabilities, include the relevant package and version range.

For repository security advisories, GitHub recommends specifying the ecosystem,
package name, and affected versions using the standard advisory formats so
that the information can be used accurately by Dependabot and the GitHub
Advisory Database. [oai_citation:3‡GitHub Docs](https://docs.github.com/en/code-security/tutorials/fix-reported-vulnerabilities/write-security-advisories?utm_source=chatgpt.com)

### 4.1 Never Include

Do not include:

- Production credentials.
- API keys.
- Access tokens.
- Private encryption keys.
- Passwords.
- Session cookies.
- Customer or personal data.
- Private repository credentials.
- Unredacted `.env` contents.
- Cloud provider credentials.
- Authentication headers containing secrets.

If evidence requires sensitive material, redact the sensitive values before
submission.

---

## 5. Coordinated Disclosure

Security reports should follow a coordinated disclosure process.

The expected lifecycle is:

```text
Private report
      ↓
Initial triage
      ↓
Impact assessment
      ↓
Reproduction
      ↓
Remediation
      ↓
Validation
      ↓
Coordinated disclosure
```

Repository security advisories are designed to allow maintainers and security
researchers to privately discuss and fix vulnerabilities before publication.
[oai_citation:4‡GitHub Docs](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)

Do not publicly disclose technical exploitation details while remediation is
still being evaluated.

---

## 6. Security Response

Security reports should be evaluated according to:

1. Reproducibility.
2. Exploitability.
3. Affected scope.
4. Confidentiality impact.
5. Integrity impact.
6. Availability impact.
7. Dependency exposure.
8. Required privileges.
9. User interaction requirements.
10. Potential downstream impact.

When appropriate, the maintainer may request additional information before
accepting or rejecting the report.

GitHub provides maintainers with workflows for reviewing private vulnerability
reports, requesting additional information, accepting a report as a draft
security advisory, or closing a report that is determined not to represent a
security risk. [oai_citation:5‡GitHub Docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/manage-vulnerability-reports?utm_source=chatgpt.com)

---

## 7. Security Development Requirements

Security validation is part of the repository engineering workflow.

The repository currently provides multiple automated security gates.

### 7.1 Secret Detection — Gitleaks

Run:

```bash
pnpm test:sast:secrets
```

This detects credentials and other secret-like material according to the
repository's `.gitleaks.toml` configuration.

### 7.2 Static Application Security Testing — Semgrep

Run:

```bash
pnpm test:sast:semgrep
```

The repository executes:

```text
.semgrep.yaml
```

and the configured Semgrep security ruleset.

### 7.3 Python Security Analysis — Bandit

Run:

```bash
pnpm test:sast:py
```

Bandit analyzes Python code according to:

```text
.bandit.yaml
```

### 7.4 Complete Security Gate

Run:

```bash
pnpm test:sast:all
```

This combines the configured secret-detection and static-security checks.

---

## 8. Dependency Security

All third-party dependencies must be evaluated before introduction.

Evaluation should consider:

- Package provenance.
- Maintenance activity.
- Known vulnerabilities.
- License compatibility.
- Dependency size and complexity.
- Transitive dependency impact.
- Compatibility with the supported runtime.
- Security implications of build scripts.
- Whether the dependency is actually necessary.

The repository uses deterministic dependency resolution through:

```text
pnpm-lock.yaml
uv.lock
```

Do not bypass lockfile integrity to force an installation.

For CI and reproducible environments, frozen dependency installation should be
preferred whenever the workflow permits it.

---

## 9. Supply-Chain Security

The repository treats package installation and CI execution as supply-chain
boundaries.

Contributors must:

- Review new dependencies before introduction.
- Avoid unnecessary packages.
- Prefer established and maintained projects.
- Review dependency changes in lockfiles.
- Avoid arbitrary remote installation scripts.
- Avoid executing untrusted binaries.
- Keep package-manager versions aligned with repository configuration.
- Preserve automated dependency-update controls.

Security findings must not be hidden through broad scanner exclusions.

---

## 10. Secret Governance

Secrets must remain outside source control.

### 10.1 Forbidden Material

Never commit:

```text
.env
.env.*
```

when those files contain real credentials or secrets.

Never commit:

- Cloud access keys.
- API keys.
- OAuth client secrets.
- Private SSH keys.
- TLS private keys.
- Database passwords.
- Authentication tokens.
- Session secrets.
- Signing keys.
- Production credentials.
- Customer secrets.

### 10.2 Environment Documentation

When an environment variable is required, document its expected name and
purpose through an appropriate example configuration such as:

```text
.env.example
```

Example files must contain placeholders or non-sensitive dummy values only.

---

## 11. CI/CD Security

GitHub Actions workflows are security-sensitive execution environments.

The repository must preserve:

- Minimal workflow permissions.
- Explicit action versions.
- Deterministic dependency installation.
- Secret isolation.
- Protected release boundaries.
- Security scanning.
- Controlled release automation.

Changes to:

```text
.github/workflows/
```

must receive additional security review.

Contributors must consider whether workflow modifications could allow:

- Arbitrary code execution.
- Secret exfiltration.
- Privilege escalation.
- Untrusted pull-request code to access protected secrets.
- Dependency substitution.
- Unauthorized release creation.
- Unauthorized repository modification.

---

## 12. GitHub Actions and Untrusted Input

Workflow expressions, pull-request metadata, branch names, issue content, and
other external inputs must be treated as untrusted data.

Do not interpolate untrusted values directly into shell commands.

Prefer explicit environment variables and safe argument handling.

Avoid patterns that transform attacker-controlled strings into executable shell
code.

---

## 13. Local Workflow Execution

The repository uses Act to simulate GitHub Actions locally.

Examples:

```bash
pnpm infra:test:workflow:ci
```

and:

```bash
pnpm infra:test:workflow:security-schedule
```

Local workflow execution must not expose real production secrets.

Act environments should use isolated credentials and non-production resources.

---

## 14. AI and LLM Security

AI and machine-learning components are treated as security-sensitive trust
boundaries.

Where applicable, contributors must evaluate:

- Prompt injection.
- Indirect prompt injection.
- Insecure output handling.
- Data leakage.
- Sensitive-context exposure.
- Training-data contamination.
- Model artifact provenance.
- Untrusted model inputs.
- Untrusted model outputs.
- Third-party inference endpoints.
- Agent tool execution.
- Evaluation and telemetry leakage.

### 14.1 Prompt and Model Data

Do not place confidential system prompts, credentials, private datasets, or
sensitive business information into public examples, logs, tests, or telemetry.

Model responses must not be treated as trusted executable instructions without
appropriate validation.

---

## 15. Machine Learning and Data Security

Machine-learning projects must preserve data provenance and avoid accidental
disclosure of sensitive information.

Contributors should document:

- Dataset origin.
- Licensing constraints.
- Data transformations.
- Feature definitions.
- Target definitions.
- Data validation assumptions.
- Training/evaluation boundaries.
- Known data-quality limitations.

Do not commit private datasets or personally identifiable information.

Educational datasets must remain clearly separated from production or
confidential data.

---

## 16. Model Context Protocol (MCP) Security

MCP integrations are treated as external execution boundaries.

Before enabling an MCP server, evaluate:

- Authentication.
- Authorization.
- Tool capabilities.
- Filesystem access.
- Network access.
- Process execution.
- Credential handling.
- Supply-chain provenance.
- Input validation.
- Output validation.
- Error handling.
- Logging behavior.

MCP tools must operate with the **least privilege** required for their
intended function.

Connection tokens and credentials must remain externalized and must never be
committed to Git.

---

## 17. Static Analysis and Suppression Policy

Security-tool findings must be investigated before suppression.

Acceptable suppression must be:

- Narrowly scoped.
- Explicit.
- Justified.
- Reviewable.
- Consistent with the tool's supported mechanisms.

Avoid broad exclusions that disable entire security categories.

For example, a targeted exception is preferable to disabling an entire scanner
for a directory without documented justification.

---

## 18. Security Exceptions

Security exceptions require explicit justification.

An exception should document:

1. The affected rule.
2. The affected file or scope.
3. Why the finding is a false positive or accepted risk.
4. Why the exception cannot be avoided.
5. The mitigation in place.
6. Whether the exception should be revisited later.

Temporary exceptions should have a clear removal condition.

---

## 19. Vulnerability Classification

The repository may classify security findings using established vulnerability
taxonomies and risk frameworks.

When applicable, reports should provide:

- CWE classification.
- CVSS assessment.
- Affected dependency advisory.
- Exploitability considerations.
- Confidentiality impact.
- Integrity impact.
- Availability impact.

A formal CVSS score is useful but is not mandatory when insufficient
information exists to calculate it reliably.

---

## 20. Security Releases

Security fixes must be released according to the repository's versioning and
release governance.

When a security issue affects a versioned package:

- Identify the affected package.
- Determine the appropriate semantic version increment.
- Create the appropriate Changeset.
- Document the security impact without exposing exploit details prematurely.
- Validate the remediation.
- Run the applicable security gates.
- Coordinate disclosure appropriately.

Security-sensitive release information should remain private until disclosure
is safe.

---

## 21. Security Checklist

Before merging security-sensitive changes, verify:

- [ ] No secrets are present.
- [ ] Gitleaks passes.
- [ ] Semgrep passes.
- [ ] Bandit passes where applicable.
- [ ] Dependencies were reviewed.
- [ ] Lockfiles remain consistent.
- [ ] CI permissions were reviewed.
- [ ] External inputs are treated as untrusted.
- [ ] AI/LLM trust boundaries were evaluated where applicable.
- [ ] MCP permissions were evaluated where applicable.
- [ ] Security exceptions are narrow and documented.
- [ ] Relevant tests pass.
- [ ] Documentation reflects security-sensitive behavior.
- [ ] No private or personally identifiable data was introduced.

---

## 22. Security Contact

For security vulnerabilities, use GitHub's private vulnerability reporting
mechanism when it is enabled for the repository.

```text
GitHub repository
→ Security / Security and quality
→ Advisories
→ Report a vulnerability
```

If the private reporting mechanism is unavailable, use the repository
maintainer's designated private security contact channel.

**Do not disclose vulnerability details through public issues.**

---

## 23. References

The security process follows the capabilities and recommended workflows
provided by GitHub for repository security policies, private vulnerability
reporting, and repository security advisories. [oai_citation:6‡GitHub Docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)

Relevant GitHub documentation:

- [oai_citation:7‡docs.github.com](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)
- [oai_citation:8‡docs.github.com](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting?utm_source=chatgpt.com)
- [oai_citation:9‡docs.github.com](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories?learn=security_advisories&learnProduct=code-security&utm_source=chatgpt.com)
- [oai_citation:10‡docs.github.com](https://docs.github.com/en/code-security/tutorials/fix-reported-vulnerabilities/write-security-advisories?utm_source=chatgpt.com)
