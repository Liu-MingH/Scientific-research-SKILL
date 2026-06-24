---
name: science-vibecoding
description: Generate rigorous, publication-ready code for scientific research through structured AI-assisted prompts (vibe coding). Covers data cleaning, statistical testing, visualization, ML modeling (sklearn + deep learning), format conversion, math modeling, text analysis, code review prep, DL training, and CS benchmarking. Use when the user asks to write scientific code, analyze research data, create publication figures, run statistical tests, build ML/DL pipelines, train neural networks, benchmark algorithms, or prepare research code for peer review. Grounded in Nature 653:348-350 (2026) best practices.
version: 1.2.0
---

# Science Vibe Coding

A structured framework for generating rigorous, publication-ready scientific code through AI-assisted natural language prompts. Based on best practices from Nature (Jones, 2026) and validated by early adopters across climate science, proteomics, molecular biology, and statistics.

**Core principle**: AI-generated scientific code is an *untrusted draft* (Meyer, 2026) — it must be verified, not just executed.

## Workflow

When a user requests scientific code generation, follow this 5-step workflow:

```
Task Progress:
- [ ] Step 1: Clarify the research task
- [ ] Step 2: Select scenario & generate prompt
- [ ] Step 3: Generate code with safety guards
- [ ] Step 4: Run verification protocol
- [ ] Step 5: Document the Vibe Blueprint
```

### Step 1: Clarify the Research Task

Ask the user these questions (skip any already answered):

1. **What** is the analysis goal? (e.g., "compare two groups", "visualize temperature trends", "train a classifier")
2. **What** is the input data format? (CSV, FASTA, Excel, NetCDF, etc.)
3. **What** tools/libraries are preferred? (pandas, scipy, matplotlib, scikit-learn, etc.)
4. **What** is the output? (figures, processed data files, statistical reports, web apps)
5. **Is this for publication?** If yes, what journal's formatting standards apply?

### Step 2: Select Scenario & Generate Prompt

Based on the user's task, select the matching scenario and load the corresponding prompt template from [prompt-templates.md](prompt-templates.md):

| Scenario | Keywords | Template |
|----------|----------|----------|
| Data Cleaning & Preprocessing | clean, preprocess, impute, outlier, missing values | `DATA_CLEANING` |
| Statistical Testing | t-test, ANOVA, chi-square, regression, p-value | `STAT_TESTING` |
| Data Visualization | plot, chart, figure, heatmap, publication figure | `VISUALIZATION` |
| Format Conversion | convert, transform, FASTA, CSV, cross-validate | `FORMAT_CONVERSION` |
| ML / Model Training | classify, predict, regression, random forest, SVM | `ML_MODELING` |
| Unit Testing | test, validate, edge case, boundary, pytest | `UNIT_TESTING` |
| Math Modeling | ODE, PDE, simulation, differential equation | `MATH_MODELING` |
| Text Analysis | NLP, extract, parse, keyword, literature review | `TEXT_ANALYSIS` |
| Code Review Prep | refactor, PEP-8, docstring, type hints, peer review | `CODE_REVIEW` |
| Deep Learning Training | neural network, CNN, RNN, Transformer, PyTorch, TensorFlow, train, GPU, CUDA | `DL_TRAINING` |
| CS Benchmarking | benchmark, algorithm comparison, time complexity, performance, profiling | `CS_BENCHMARKING` |

**Multi-scenario tasks**: If the task spans multiple scenarios (e.g., clean data → run stats → plot results), chain the templates in order with explicit data handoff between steps.

#### Chaining Templates: Multi-Scenario Protocol

When chaining 2+ templates, follow these rules to prevent data loss between stages:

**Variable Naming Convention**: Each stage's output variable must use a consistent prefix matching its template:
- `data_clean_*` for DATA_CLEANING outputs
- `stat_*` for STAT_TESTING outputs
- `vis_*` for VISUALIZATION outputs
- `ml_*` for ML_MODELING outputs
- `dl_*` for DL_TRAINING outputs (model state, training history, checkpoints)
- `bench_*` for CS_BENCHMARKING outputs (timing data, memory profiles, scaling results)

This prevents variable name collisions and makes handoff points traceable.

**Data Handoff Patterns** (choose one before generating code):

1. **FILE handoff** (recommended for reproducibility): Each stage writes output to a timestamped file, the next stage reads it.
   ```python
   # Stage 1 output
   cleaned = clean_dataset(raw_df)
   cleaned.to_csv("data_clean_20260624.csv", index=False)
   
   # Stage 2 input
   cleaned = pd.read_csv("data_clean_20260624.csv")
   stat_result = run_test(cleaned)
   ```

2. **MEMORY handoff** (for single-script chains): Use distinct variable names; validate data shape at each handoff.
   ```python
   # Handoff point — always validate
   assert not data_clean_df.empty, "Stage 1 produced empty output"
   print(f"[CHAIN] Handoff: Stage 1 → Stage 2 | Shape: {data_clean_df.shape}")
   stat_result = run_test(data_clean_df)
   ```

3. **CONTRACT handoff** (for distributed/large pipelines): Define a schema file specifying column names, types, and value ranges. Each stage validates input against the contract.

**Handoff Validation**: Every chain point MUST print a `[CHAIN]` log confirming:
- Source stage → destination stage
- Data shape (rows, columns)
- Any dropped or filtered rows
- Whether the data passed validation

**Chain Ordering Rule**: Templates must be executed in this dependency order when combined: DATA_CLEANING → FORMAT_CONVERSION → STAT_TESTING / ML_MODELING / DL_TRAINING / MATH_MODELING → CS_BENCHMARKING / VISUALIZATION → CODE_REVIEW. UNIT_TESTING and TEXT_ANALYSIS can be inserted at any point. Note: DL_TRAINING requires DATA_CLEANING as a prerequisite; CS_BENCHMARKING should run after model implementation but can feed into VISUALIZATION.

### Step 3: Generate Code with Safety Guards

When generating the code, ALWAYS apply these mandatory safety guards:

#### Guard 1: Explicit Method Declaration

**CRITICAL**: The method declaration MUST be determined dynamically AFTER all assumption checks, then printed immediately before the actual function call. A hardcoded string before method selection is a silent bug — it prints the requested method regardless of what the code actually executes.

**CORRECT pattern** (dynamic, after assumption checks):
```python
# Step 1: Run assumption checks
shapiro_stat, shapiro_p = stats.shapiro(group_a)
levene_stat, levene_p = stats.levene(group_a, group_b)

# Step 2: Select method based on assumptions
if shapiro_p > 0.05 and levene_p > 0.05:
    method_name = "Welch's t-test (scipy.stats.ttest_ind, equal_var=False)"
    method_fn = stats.ttest_ind
    method_kwargs = {"equal_var": False}
elif shapiro_p > 0.05 and levene_p <= 0.05:
    method_name = "Student's t-test (scipy.stats.ttest_ind, equal_var=True)"
    method_fn = stats.ttest_ind
    method_kwargs = {"equal_var": True}
else:
    method_name = "Mann-Whitney U (scipy.stats.mannwhitneyu)"
    method_fn = stats.mannwhitneyu
    method_kwargs = {}

# Step 3: Print the DYNAMICALLY determined method IMMEDIATELY before calling it
print(f"[METHOD] Using: {method_name}")
print(f"[METHOD] Library: scipy v{scipy.__version__}")
print(f"[METHOD] Rationale: Shapiro-Wilk p={shapiro_p:.4f}, Levene p={levene_p:.4f}")

# Step 4: Execute
result = method_fn(group_a, group_b, **method_kwargs)
```

**BUG pattern to AVOID** (hardcoded before assumption checks):
```python
# BUG: Prints "Welch's t-test" regardless of what happens below
print(f"[METHOD] Using: Welch's t-test (scipy.stats.ttest_ind with equal_var=False)")

# Assumption checks below may lead to a DIFFERENT method being used,
# but the print above has already lied to the user.
shapiro_stat, shapiro_p = stats.shapiro(group_a)
levene_stat, levene_p = stats.levene(group_a, group_b)
# ... method selection logic that might pick Student's t-test or Mann-Whitney ...
```

Never let the code silently choose a statistical method or algorithm. The user must see confirmation of what was actually executed — and that confirmation must match reality.

#### Guard 2: No Silent Defaults

```python
# MANDATORY: Raise errors for unspecified parameters instead of using library defaults
raise ValueError("Parameter [X] not specified. Please explicitly set this value.")
```

If the user hasn't specified a critical parameter (imputation method, kernel function, significance level), the code must ask — not assume.

#### Guard 3: Input Validation Block

Every generated script must start with a validation section:

```python
# === INPUT VALIDATION ===
# Check data shape, types, missing values BEFORE any analysis
assert not df.empty, "Input dataframe is empty"
assert df.shape[0] > 1, "Need at least 2 rows for analysis"
# ... domain-specific checks
print(f"[DATA] Shape: {df.shape}, Missing: {df.isnull().sum().sum()}")
```

#### Guard 4: No AI Self-Testing

Never generate test cases alongside analysis code unless explicitly requested under the `UNIT_TESTING` scenario. When generating tests, they MUST include adversarial edge cases (see `UNIT_TESTING` template).

#### Guard 5: Comprehensive Comments

Every function and non-trivial code block must have comments explaining:
- **What** it does (the operation)
- **Why** this method was chosen (the scientific rationale)
- **What** assumptions it makes (distribution, sample size, etc.)

### Step 4: Run Verification Protocol

After generating code, walk the user through the [risk-checklist.md](risk-checklist.md). At minimum, verify:

1. **Method fidelity**: Does the executed method match what was requested? (cf. Morey's t-test/z-test case)
2. **No silent data modification**: Does the code alter, impute, or smooth data without explicit instruction?
3. **Test adversarial inputs**: What happens with empty data, NaN values, single-row input?
4. **Output sanity check**: Do results match expected ranges from domain knowledge?

#### Blueprint Checkpoint (MANDATORY)

After completing Step 4 verification, PAUSE and ask the user:

> "The analysis is complete and verified. Would you like me to generate a Vibe Blueprint for reproducibility? This will record the exact prompts, parameters, verification results, and known limitations for inclusion in your paper's supplementary materials."

If the user says yes, proceed to Step 5. If the user says no, record that the blueprint was declined and move on. This checkpoint ensures the blueprint is never silently skipped — reproducibility documentation must be a conscious choice.

### Step 5: Document the Vibe Blueprint

For reproducibility (Meyer, 2026), generate a `VIBE_BLUEPRINT.md` file alongside the code. Use the template in [vibe-blueprint-template.md](vibe-blueprint-template.md).

The blueprint records: the exact prompts used, the AI model and version, all parameter choices, verification results, and known limitations.

## Safety Principles

These principles are derived from Nature 653:348-350 and referenced papers:

### Principle 1: "Vibe coding is not a substitute for understanding" (Meyer, 2026)

If the user cannot explain what the generated code does in their own words, they should not use it for publication. Offer to explain any generated code line by line.

### Principle 2: "Wrong in a subtle way you wouldn't necessarily know" (Morey, via Nature)

AI code can produce results that *look* correct but use wrong methods. The most dangerous errors are the ones that pass visual inspection. Always verify the method, not just the output.

### Principle 3: "It can make some pretty hilarious tests for itself where it just always passes" (Meyer, via Nature)

AI-generated self-tests are unreliable. They tend to verify the simplest path. Researchers must design their own validation tests.

### Principle 4: "Vibe debugging is chaos" (Pimenova et al., 2025)

Keep generated code modular and short. A 400-line file that balloons to 3000 lines becomes unreadable by both human and AI. Split into small, single-responsibility functions.

### Principle 5: "Code should be published alongside the research paper" (Nature consensus)

All generated code should be written as if it will be publicly reviewed. Follow PEP-8, use type hints, write docstrings, and structure for readability.

### Principle 6: "GPU non-determinism must be explicitly controlled" (experience from DL research)

PyTorch and TensorFlow produce different results on every GPU run unless seeds are exhaustively set. Floating-point parallel reduction order varies across CUDA executions. Without `torch.backends.cudnn.deterministic = True`, cuDNN selects different convolution algorithms per run. A paper that reports "70.3% accuracy" from a single run without seed control cannot be reproduced — not by reviewers, not by yourself six months later.

### Principle 7: "Train/eval mode mismatch is the most common silent bug in DL code" (experience from DL research)

Forgetting `model.eval()` before validation causes batch normalization layers to use running statistics instead of batch statistics, silently contaminating validation results. Forgetting `model.train()` after validation keeps dropout active during subsequent training steps. These bugs produce results that look plausible but are wrong — the most dangerous category of error for publication.

## Language-Specific Defaults

| Language | Formatting | Type Hints | Docstring Style | Testing Framework |
|----------|-----------|------------|-----------------|-------------------|
| Python | PEP-8 / ruff | Required | Google-style | pytest |
| R | tidyverse style | roxygen2 types | roxygen2 | testthat |
| MATLAB | MATLAB Lint | Argument blocks | Help text | unittest (built-in) |
| Julia | BlueStyle.jl | Required | Docstrings | Test.jl |

## Quick Commands

Users can trigger specific scenarios with shorthand:

- **"Clean this data"** → `DATA_CLEANING` template
- **"Run a t-test"** → `STAT_TESTING` template (Welch's t-test by default)
- **"Make a figure"** → `VISUALIZATION` template (colorblind-safe palette by default)
- **"Convert formats"** → `FORMAT_CONVERSION` template
- **"Train a model"** → `ML_MODELING` template (5-fold CV by default)
- **"Write tests"** → `UNIT_TESTING` template (adversarial cases included)
- **"Simulate"** → `MATH_MODELING` template
- **"Extract text"** → `TEXT_ANALYSIS` template
- **"Refactor for paper"** → `CODE_REVIEW` template
- **"Train a neural network"** → `DL_TRAINING` template (full reproducibility suite by default)
- **"Benchmark algorithms"** → `CS_BENCHMARKING` template (multi-scale + correctness verification)
- **"Vibe blueprint"** → Generate reproducibility documentation

## Common Pipelines

Reference for common multi-scenario workflows. Each pipeline lists the templates in execution order and the recommended handoff pattern.

| Pipeline | Templates (in order) | Handoff Pattern | Notes |
|----------|---------------------|-----------------|-------|
| **Standard Analysis** | DATA_CLEANING → STAT_TESTING → VISUALIZATION | FILE | Most common pipeline; clean data, test hypotheses, visualize results |
| **ML Pipeline** | DATA_CLEANING → ML_MODELING → VISUALIZATION | FILE | Feature engineering in DATA_CLEANING; use stratified CV in ML_MODELING |
| **Simulation Study** | MATH_MODELING → VISUALIZATION → STAT_TESTING | MEMORY | Run simulations, plot trajectories, then test parameter sensitivity |
| **Publication Prep** | CODE_REVIEW → VISUALIZATION → (Blueprint) | CONTRACT | Refactor code for journal submission, regenerate figures to spec, document |
| **Literature Mining** | TEXT_ANALYSIS → STAT_TESTING → VISUALIZATION | FILE | Extract data from papers, run meta-analysis, visualize findings |
| **DL Research** | DATA_CLEANING → DL_TRAINING → CS_BENCHMARKING → VISUALIZATION | FILE | Clean data, train model with explicit seeds, benchmark performance, plot loss/accuracy curves |
| **Algorithm Study** | CS_BENCHMARKING → STAT_TESTING → VISUALIZATION | FILE | Benchmark multiple algorithms, test performance differences statistically, visualize scaling behavior |

When in doubt, use FILE handoff — it provides the strongest reproducibility guarantee.

## References

- Jones, N. "How to vibe code in science: early adopters share their tips." *Nature* 653, 348-350 (2026). DOI: [10.1038/d41586-026-01477-w](https://doi.org/10.1038/d41586-026-01477-w)
- Meyer, J. G. "Vibe Coding Omics Data Analysis Applications." *J. Proteome Res.* 25, 1191-1197 (2026). DOI: [10.1021/acs.jproteome.5c00984](https://doi.org/10.1021/acs.jproteome.5c00984)
- Ziemann, M., Eren, Y. & El-Osta, A. "Gene name errors are widespread in the scientific literature." *Genome Biol.* 17, 177 (2016). DOI: [10.1186/s13059-016-1044-7](https://doi.org/10.1186/s13059-016-1044-7)
- Pimenova, V. et al. "Good Vibrations? A Qualitative Study of Co-Creation, Communication, Flow, and Trust in Vibe Coding." *arXiv:2509.12491* (2025). DOI: [10.48550/arXiv.2509.12491](https://doi.org/10.48550/arXiv.2509.12491)

## Additional Resources

- For detailed prompt templates (11 scientific scenarios), see [prompt-templates.md](prompt-templates.md)
- For the full risk verification checklist, see [risk-checklist.md](risk-checklist.md)
- For the Vibe Blueprint reproducibility template, see [vibe-blueprint-template.md](vibe-blueprint-template.md)
- For a complete end-to-end example demonstrating all safety guards, see [examples/](examples/)
