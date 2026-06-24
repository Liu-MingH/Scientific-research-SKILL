# End-to-End Example: Clinical Trial Analysis

This example demonstrates the complete Science Vibe Coding workflow applied to a realistic research scenario: comparing blood glucose reduction between a new treatment and a control group.

## What This Example Demonstrates

The `end_to_end_example.py` script implements the **Standard Analysis Pipeline** (DATA_CLEANING → STAT_TESTING → VISUALIZATION) with all six mandatory safety guards:

| Guard | What It Protects Against | Where to Look |
|-------|-------------------------|---------------|
| **Guard 1: Explicit Method Declaration** | AI silently substituting a requested test with a different one (e.g., t-test → z-test, per Morey's case) | `run_hypothesis_test()` — method selected dynamically AFTER Shapiro-Wilk and Levene checks, then printed immediately before execution |
| **Guard 2: No Silent Defaults** | Library defaults that are scientifically inappropriate for your data | All parameters are named constants at the top of the script with explicit rationale comments |
| **Guard 3: Input Validation** | Running analysis on corrupted or unexpected data | Every function entry point begins with an input validation block checking shape, types, and missing values |
| **Guard 4: No AI Self-Testing** | Self-generated tests that "always pass" (Meyer, 2026) | The script contains no pytest functions or auto-generated test suites — only human-verifiable sanity checks |
| **Guard 5: Comprehensive Comments** | Code that runs but cannot be explained to a reviewer | Every function has Google-style docstrings; every non-trivial block has comments explaining what, why, and assumptions |
| **Guard 6: Change Audit** | AI secretly modifying or deleting code (Pimenova, 2025) | All modifications are reported; no silent changes to existing code |

The example also demonstrates the **FILE handoff pattern** for multi-stage pipelines: each stage writes output to a timestamped file, and the next stage reads it back with explicit `[CHAIN]` log messages confirming data integrity.

## Scenario

- **Research question**: Does a new glucose-lowering treatment reduce blood glucose more than placebo?
- **Design**: Two-arm parallel group (Treatment n=30, Control n=30)
- **Primary endpoint**: Change in fasting blood glucose (mg/dL) from baseline to week 12
- **Analysis**: Two-sample comparison with assumption-guided method selection

## Requirements

Install dependencies:

```bash
pip install numpy pandas scipy matplotlib seaborn
```

Minimum versions: Python 3.9+, numpy 1.24+, pandas 2.0+, scipy 1.10+, matplotlib 3.7+, seaborn 0.12+.

## Running the Example

```bash
cd examples/
python end_to_end_example.py
```

The script generates:

| Output | Description |
|--------|-------------|
| `data_raw_YYYYMMDD_HHMMSS.csv` | Raw synthetic dataset |
| `data_clean_YYYYMMDD_HHMMSS.csv` | Cleaned dataset after validation |
| `fig_glucose_reduction_YYYYMMDD_HHMMSS.svg` | Publication-ready vector figure |
| `fig_glucose_reduction_YYYYMMDD_HHMMSS.tiff` | High-resolution raster (300 DPI) |

All files are timestamped for reproducibility and audit trail.

## Expected Console Output

The script prints structured log messages at each stage:

```
[DATA] Generated synthetic data: 60 rows × 3 columns
[VALIDATE] Raw data passed validation
[DATA] Data cleaning: 0 rows removed, 0 outliers flagged
[CLEANING] Saved: data_clean_20260624_143022.csv (60 rows)
[CHAIN] Handoff: DATA_CLEANING → STAT_TESTING | Loaded: 60 rows, 3 columns
[ASSUMPTION] Shapiro-Wilk (Treatment): W=0.978, p=0.8234
[ASSUMPTION] Shapiro-Wilk (Control): W=0.981, p=0.8765
[ASSUMPTION] Levene: W=0.156, p=0.6942
[METHOD] Selected: Welch's t-test (scipy.stats.ttest_ind, equal_var=False)
[METHOD] Rationale: Shapiro-Wilk p_A=0.8234, p_B=0.8765, Levene p=0.6942
[STAT] Welch's t-test: t=-4.512, df=57.3, p=0.000033
[STAT] Cohen's d: -1.165, 95% CI: [-1.721, -0.602]
[EFFECT] Large effect size (|d| > 0.8)
[CHAIN] Handoff: STAT_TESTING → VISUALIZATION
[FIGURE] Saved: fig_glucose_reduction_20260624_143022.svg
[FIGURE] Saved: fig_glucose_reduction_20260624_143022.tiff (DPI: 300)
[DONE] Analysis pipeline complete.
```

The critical line to verify is `[METHOD] Selected:` — it must appear AFTER the assumption checks, confirming that the method was chosen dynamically rather than hardcoded.

## Verifying Guard 1 (the Morey Test)

To confirm that method declaration is dynamic and not a hardcoded lie, modify the synthetic data generator to produce non-normal data (e.g., use an exponential distribution) and re-run. The `[METHOD]` line should now show Mann-Whitney U instead of Welch's t-test, proving the method selection adapts to data characteristics rather than echoing a preset string.

## Key Design Decisions

1. **Synthetic data with known ground truth**: The treatment group's mean reduction is set to 25 mg/dL vs. 10 mg/dL for control, so we know there is a real difference to detect.
2. **FILE handoff over MEMORY handoff**: Writing each stage's output to disk provides an audit trail and allows re-running individual stages without re-executing the entire pipeline.
3. **Colorblind-safe visualization**: Uses seaborn's Set2 palette, which is distinguishable under common forms of color vision deficiency.
4. **Both SVG and TIFF output**: Vector format for journal typesetting, raster format for quick preview — matching Nature's supplementary figure requirements.

## Related Files

- [../SKILL.md](../SKILL.md) — Full skill workflow and safety guard documentation
- [../prompt-templates.md](../prompt-templates.md) — Nine reusable prompt templates for scientific coding
- [../risk-checklist.md](../risk-checklist.md) — Pre- and post-execution verification checklist
- [../vibe-blueprint-template.md](../vibe-blueprint-template.md) — Reproducibility documentation template
