# Scientific Research SKILL — Science Vibe Coding

A structured QoderWork skill for generating rigorous, publication-ready scientific code through AI-assisted natural language prompts. Covers the full research lifecycle: data cleaning, statistical testing, visualization, ML/DL modeling, CS benchmarking, and code review.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)]()
[![Templates](https://img.shields.io/badge/templates-11-green.svg)]()

## What Is This?

"Vibe coding" — a term coined by OpenAI co-founder Andrej Karpathy — describes a programming paradigm where users interact with AI through natural language, letting the AI handle code generation while focusing on outcomes.

This skill brings structure and rigor to vibe coding for **scientific research**. It encodes best practices from a [Nature article](https://doi.org/10.1038/d41586-026-01477-w) (Jones, 2026) and validated case studies across proteomics, climate science, molecular biology, and statistics.

**Core principle**: AI-generated scientific code is an *untrusted draft* — it must be verified, not just executed.

## Why It Exists

A [Nature investigation](https://doi.org/10.1038/d41586-026-01477-w) found that while AI coding tools dramatically accelerate research (up to 75% productivity increase), they introduce subtle, dangerous errors:

- **Method substitution**: AI runs a z-test when you asked for a t-test, but labels the output as a t-test
- **Silent data modification**: AI "helpfully" imputes missing values or smooths curves without telling you
- **Self-testing theater**: AI writes tests for its own code that "always pass"
- **Code inflation**: 400-line scripts balloon to 3000 lines, becoming unreadable by both human and AI

This framework prevents these failure modes through structured prompts, mandatory safety guards, and verification protocols.

## What's Inside

```
science-vibecoding/
├── SKILL.md                     # Core workflow & safety principles
├── prompt-templates.md          # 11 battle-tested prompt templates
├── risk-checklist.md            # Pre/post-execution verification
├── vibe-blueprint-template.md   # Reproducibility documentation
├── examples/                    # End-to-end example with all safety guards
├── README.md                    # This file
└── LICENSE                      # MIT License
```

### Prompt Templates (11 Scientific Scenarios)

| # | Scenario | Primary Risk Guard |
|---|----------|-------------------|
| 1 | Data Cleaning & Preprocessing | Prevents unauthorized imputation methods |
| 2 | Statistical Hypothesis Testing | Prevents silent method substitution (the "Morey Test") |
| 3 | Publication-Quality Visualization | Enforces colorblind-safe palettes & journal DPI |
| 4 | Cross-Software Format Conversion | Detects Excel gene-name conversion artifacts |
| 5 | ML Model Training | Mandates k-fold CV, prevents data leakage |
| 6 | Anti-Lazy Unit Testing | Forces adversarial edge cases (60%+ edge coverage) |
| 7 | Mathematical Modeling & Simulation | Requires named parameters with units, stability checks |
| 8 | Text Mining & Extraction | Handles encoding fallbacks, reconciliation logging |
| 9 | Code Review for Publication | Zero-logic-change constraint during refactoring |
| 10 | Deep Learning Training | Full GPU reproducibility suite, train/eval mode guards, gradient integrity checks |
| 11 | CS Algorithm Benchmarking | Multi-scale timing, correctness verification, scaling behavior analysis |

### Safety System

Every generated code includes five mandatory safety guards:

1. **Explicit Method Declaration** — runtime print of the exact function being called
2. **No Silent Defaults** — unspecified parameters raise errors instead of using library defaults
3. **Input Validation Block** — data shape, type, and completeness checks before any analysis
4. **No AI Self-Testing** — tests only generated under explicit `UNIT_TESTING` scenario with adversarial cases
5. **Comprehensive Comments** — every function documents what, why, and assumptions

### Vibe Blueprint

Based on Meyer's (2026) reproducibility framework, every session generates a `VIBE_BLUEPRINT.md` documenting: exact prompts used, AI model version, all parameters, verification results, cost/time analysis, and known limitations.

## Installation

### As a QoderWork Skill

Copy the `science-vibecoding` directory to your skills folder:

```bash
# QoderWork / QoderWork CN — install via .skill file
# Download Scientific-research-SKILL.skill from Releases, then drag-and-drop into QoderWork

# Or manual install:
# macOS / Linux
cp -r science-vibecoding ~/.qoderwork/skills/

# Windows (QoderWork CN)
xcopy science-vibecoding %USERPROFILE%\.qoderworkcn\skills\science-vibecoding /E /I
```

The skill will be automatically discovered when you ask for scientific code generation, data analysis, statistical testing, or research code preparation.

### Standalone Use

You can also use the prompt templates directly with any AI coding assistant (ChatGPT, Claude, Copilot, Cursor, etc.). Just copy the relevant template from `prompt-templates.md`, fill in the `[bracketed placeholders]`, and paste it as your prompt.

## Quick Start

Tell your AI assistant:

```
Clean my proteomics dataset (data.csv):
- Delete rows with missing protein IDs
- Impute intensity values using KNN (k=5)
- Flag outliers using IQR method
- Log every action
```

The skill will automatically:
1. Select the `DATA_CLEANING` template
2. Add safety guards (no silent defaults, input validation, action logging)
3. Generate verified, commented, publication-ready code
4. Prompt you to create a Vibe Blueprint for reproducibility

## Evidence Base

This framework is grounded in peer-reviewed research and documented failure cases:

| Source | Key Finding |
|--------|------------|
| [Nature 653:348-350](https://doi.org/10.1038/d41586-026-01477-w) | 90%+ developers use AI coding; AI accuracy on benchmarks is ~71% |
| [Meyer, J. Proteome Res. 2026](https://doi.org/10.1021/acs.jproteome.5c00984) | 4 prompts, 10 min, $1.96 → 1400 lines of verified proteomics code |
| [Ziemann et al., Genome Biol. 2016](https://doi.org/10.1186/s13059-016-1044-7) | 20% of genomics papers had Excel gene-name errors |
| [Pimenova et al., arXiv 2025](https://doi.org/10.48550/arXiv.2509.12491) | 190K words analyzed; identified 13 pain points and 28 best practices |

## Who Should Use This

- **Researchers** who use AI to generate analysis code but worry about correctness
- **Lab PIs** who want standardized, reviewable code from their team's AI-assisted workflows
- **Bioinformaticians** building data pipelines with AI assistance
- **Statisticians** who want guardrails against AI method substitution
- **Graduate students** learning to combine AI tools with rigorous scientific practice

## Who Should NOT Rely on This Alone

- Researchers who cannot explain what the generated code does (see Principle 1)
- Clinical or regulatory submissions without independent validation
- Production systems without professional software engineering review

## Contributing

Contributions are welcome! Areas where we'd love input:

- **New scenario templates** for fields not yet covered (e.g., genomics pipelines, geospatial analysis, neuroscience signal processing)
- **Failure case studies** with documented AI errors and how they were caught
- **Language-specific adaptations** (R, MATLAB, Julia templates)
- **Journal-specific compliance checklists** for code supplementary materials

Please open an issue or pull request.

## License

MIT License. See [LICENSE](LICENSE).

## Citation

If you use this framework in your research, please cite:

```bibtex
@misc{science-vibecoding-2026,
  title  = {Science Vibe Coding: A Structured Framework for AI-Assisted Scientific Code Generation},
  author = {Liu-MingH},
  year   = {2026},
  url    = {https://github.com/Liu-MingH/Scientific-research-SKILL},
  note   = {Based on best practices from Nature 653:348-350 (2026)}
}
```

## Acknowledgments

This framework synthesizes insights from:
- Nicola Jones's reporting in Nature (2026)
- Jesse Meyer's proteomics vibe coding study (J. Proteome Res., 2026)
- Veronica Pimenova et al.'s qualitative study of vibe coding practices (arXiv, 2025)
- Mark Ziemann et al.'s gene name error research (Genome Biol., 2016)
- The scientists who shared their experiences: Zeke Hausfather, Rosemarie Wilton, Tim Hobbs, Manuel Corpas, and Richard Morey
