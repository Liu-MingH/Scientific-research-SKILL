# Science Vibe Coding

> Structured AI-assisted scientific code generation. 6 safety guards, 11 prompt templates, grounded in Nature (2026).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)]()

Works with **Cursor**, **Claude Code**, **Windsurf**, **Copilot**, **ChatGPT**, and any AI coding assistant.

## Quick Start

```bash
# One-line install — auto-detects your AI tool
curl -sL https://raw.githubusercontent.com/Liu-MingH/Scientific-research-SKILL/main/install.sh | bash
```

Or manually:

```bash
cp SKILL.md .cursorrules     # Cursor
cp SKILL.md CLAUDE.md        # Claude Code
cp SKILL.md .windsurfrules   # Windsurf
```

Then tell your AI assistant:

```
Clean my proteomics dataset (data.csv):
- Delete rows with missing protein IDs
- Impute intensity values using KNN (k=5)
- Flag outliers using IQR method
```

The framework will: output an analysis plan for your confirmation → generate code with safety guards → run verification → produce a reproducibility blueprint.

## File Structure

```
├── SKILL.md                     # Core: workflow, 6 guards, 8 principles
├── prompt-templates.md          # 11 scenario templates + prompt guide
├── risk-checklist.md            # Verification checklist
├── vibe-blueprint-template.md   # Reproducibility template
├── install.sh                   # Universal installer
├── examples/                    # End-to-end example
└── LICENSE                      # MIT
```

## Why This Exists

AI coding tools accelerate research by up to 75%, but introduce subtle, dangerous errors:

- **Method substitution** — AI runs a z-test, labels it as a t-test (Morey, Nature 2026)
- **Silent data modification** — AI imputes missing values without telling you
- **Self-testing theater** — AI writes tests that "always pass" (Meyer, 2026)
- **Code inflation** — 400 lines balloon to 3,000, unreadable by anyone (Pimenova, 2025)

This framework prevents these failure modes through structured prompts, mandatory guards, and verification protocols.

## Safety System

Six mandatory guards applied to every generated code:

1. **Explicit Method Declaration** — prints the exact function being called (dynamic, not hardcoded)
2. **No Silent Defaults** — unspecified parameters raise errors instead of using library defaults
3. **Input Validation** — data shape, type, and completeness checks before any analysis
4. **No AI Self-Testing** — tests only generated under explicit adversarial scenarios
5. **Comprehensive Comments** — every function documents what, why, and assumptions
6. **Change Audit** — AI must report all modifications, deletions, and overwrites

## Evidence Base

| Source | Key Finding |
|--------|------------|
| [Nature 653:348-350](https://doi.org/10.1038/d41586-026-01477-w) | 90%+ developers use AI coding; AI accuracy on benchmarks ~71% |
| [Meyer, J. Proteome Res. 2026](https://doi.org/10.1021/acs.jproteome.5c00984) | 4 prompts, 10 min, $1.96 → 1,400 lines of verified code |
| [Ziemann et al., Genome Biol. 2016](https://doi.org/10.1186/s13059-016-1044-7) | 20% of genomics papers had Excel gene-name errors |
| [Pimenova et al., arXiv 2025](https://doi.org/10.48550/arXiv.2509.12491) | 190K words analyzed; 13 pain points, 28 best practices |

## Contributing

Contributions welcome: new scenario templates, failure case studies, language adaptations (R, MATLAB, Julia), journal-specific checklists.

## License

MIT. See [LICENSE](LICENSE).

## Citation

```bibtex
@misc{science-vibecoding-2026,
  title  = {Science Vibe Coding: A Structured Framework for AI-Assisted Scientific Code Generation},
  author = {Liu-MingH},
  year   = {2026},
  url    = {https://github.com/Liu-MingH/Scientific-research-SKILL}
}
```
