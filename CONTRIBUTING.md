# Contributing to MIK-JARVIS

Thank you for your interest in contributing to **MIK-JARVIS** by **MIK Software**! This guide covers our standards and how to submit improvements or extensions.

---

## Why Contribute?

Contributing to MIK-JARVIS helps build a modern, robust, and local-first AI assistant ecosystem for developer and enterprise productivity.

### Recognition

All contributors are acknowledged in our project documentation and repository releases by MIK Software.

---

## Ways to Contribute

### Good First Contributions

These are great starting points for new contributors:

- Documentation improvements and typo fixes
- Bug reports with reproducible steps
- Tool and channel enhancements
- Test coverage improvements

Look for issues labeled [`good-first-issue`](https://github.com/open-jarvis/OpenJarvis/labels/good-first-issue).

### Ideal Contributions

- Bug fixes with tests
- Performance improvements
- New tools, engines, or agents following the [registry pattern](docs/development/contributing.md#registry-pattern)
- New channel integrations (Telegram, Discord, Slack, etc.)

### Harder to Review

These require more context and review time. **Please open an issue for discussion before starting a PR:**

- New primitives or major extensions to existing ones
- Large refactors
- Changes to core abstractions (`BaseAgent`, `InferenceEngine`, etc.)

### May Not Be Accepted

To avoid wasted effort, note that PRs in these categories are unlikely to be merged:

- Changes that break backwards compatibility in the public API
- Changes that add significant new dependencies without justification
- Changes that add friction to the user experience

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | Required |
| [uv](https://docs.astral.sh/uv/) | Latest | Package manager |
| Node.js | 22+ | Only needed for ClaudeCodeAgent and WhatsApp channel |

### Setup

```bash
git clone https://github.com/miksoftware/JARVIS.git
cd JARVIS
uv sync --extra dev
```

### Pre-commit Hooks

We use [pre-commit](https://pre-commit.com/) to run linting and formatting checks before each commit:

```bash
uv run pre-commit install
```

This installs Git hooks that automatically run [Ruff](https://docs.astral.sh/ruff/) on every commit. If the hooks fail, fix the issues and commit again.

For detailed development setup, code conventions, and project structure, see the [Development Guide](docs/development/contributing.md).

---

## Claiming Issues

1. Check if an issue exists or open one at [Issues](https://github.com/miksoftware/JARVIS/issues) describing what you'd like to work on.
2. Fork, branch, and start working.

---

## Proposing Changes

### Trivial Changes

For small fixes (typos, doc improvements, simple bug fixes), go ahead and open a PR directly.

### Non-trivial Changes

For larger changes — new features, refactors, new dependencies — open an issue first to discuss the approach with MIK Software maintainers.

---

## Pull Request Process

### Before Submitting

1. Run the full test suite:
   ```bash
   uv run pytest tests/ -v
   ```
2. Run the linter:
   ```bash
   uv run ruff check src/ tests/
   ```
3. Run the formatter:
   ```bash
   uv run ruff format --check src/ tests/
   ```
4. Add tests for new functionality
5. Follow the [registry pattern](docs/development/contributing.md#registry-pattern) for new components

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add FAISS memory backend
fix: handle empty tool responses in orchestrator
docs: update engine discovery documentation
test: add coverage for BM25 backend
refactor: simplify agent base class helpers
```

Keep the first line under 72 characters. Reference relevant issues (e.g., `fixes #42`).

### What Makes a Good PR

- **Focused** — one feature, fix, or refactor per PR
- **Tested** — includes unit tests covering new code paths
- **Documented** — updates docstrings and docs if adding public API
- **Backwards compatible** — avoids breaking existing interfaces without discussion

---

## Contribution Areas

MIK-JARVIS is built on five composable primitives. Here's where you can contribute:

| Area | What to Build | Guide |
|---|---|---|
| **Intelligence** | Model catalog entries, routing strategies | [Dev Guide](docs/development/contributing.md) |
| **Engines** | New inference backends (e.g., TensorRT, ONNX) | [Dev Guide](docs/development/contributing.md) |
| **Agents** | New agent types, agent improvements | [Dev Guide](docs/development/contributing.md) |
| **Tools** | New tools (browser, API clients, etc.) | [Dev Guide](docs/development/contributing.md) |
| **Learning** | Router policies, reward functions, training | [Dev Guide](docs/development/contributing.md) |
| **Evals** | New datasets, scorers, benchmark configs | [Dev Guide](docs/development/contributing.md) |
| **Channels** | Chat platform integrations | [Dev Guide](docs/development/contributing.md) |
| **Rust Port** | PyO3 bindings, crate parity with Python | See `rust/` directory |

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

## Questions?

- Open an issue or discussion on [GitHub](https://github.com/miksoftware/JARVIS)
- Contact MIK Software at [contacto@miksoftwarecol.com](mailto:contacto@miksoftwarecol.com)
