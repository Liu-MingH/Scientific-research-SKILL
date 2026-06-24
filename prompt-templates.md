# Prompt Templates for Scientific Vibe Coding

Eleven battle-tested prompt templates for common research scenarios. Each template includes explicit safety guards to prevent the most common AI coding errors in science.

**How to use**: Replace `[bracketed placeholders]` with your specific values. Combine templates for multi-step workflows.

---

## 1. DATA_CLEANING — Data Cleaning & Preprocessing

**When to use**: Handling missing values, outliers, normalization, deduplication.

**Primary risk**: AI uses default imputation methods that may be scientifically inappropriate for your data type.

```
As a rigorous [data scientist / domain expert], process the dataset `[filename.csv]` using Python's `pandas`.

Execute these steps EXACTLY. Do NOT use any imputation library or method I have not explicitly approved:

1. **Delete** all rows where `[column_A]` has missing values. Do NOT impute them.
2. **Impute** missing values in `[column_B]` using the [median / mean / mode] — specifically NOT [method to avoid]. Explain in a comment WHY this choice is appropriate for this variable's distribution.
3. **Flag outliers** in `[column_C]` using the IQR method (Q1 - 1.5*IQR to Q3 + 1.5*IQR). Write flagged rows to `[outliers_log.csv]` — do NOT delete them from the main dataset.
4. **Normalize** `[column_D]` using [z-score / min-max / log transform]. State the formula in a code comment.
5. Add a `print()` summary after EACH step showing: rows remaining, NaN count, and value range for the affected column.

CONSTRAINTS:
- Do NOT silently drop any data. Every removal must be logged.
- Do NOT use `df.dropna()` without specifying the `subset` parameter.
- Print `[CLEANING]` prefix on all status messages for easy grep.
```

**Verification checklist**:
- [ ] Count rows before and after — do removals match expectations?
- [ ] Check that outliers file exists and contains flagged rows
- [ ] Verify imputed values fall within expected range

---

## 2. STAT_TESTING — Statistical Hypothesis Testing

**When to use**: Comparing groups, testing distributions, correlation analysis.

**Primary risk**: AI silently substitutes the requested test with a simpler one (e.g., t-test → z-test), producing results that are "wrong in a subtle way" (Morey, Nature 2026).

```
Perform statistical analysis on `[dataset]`. Compare `[Group_A]` and `[Group_B]` on `[outcome_variable]`.

MANDATORY METHOD: Use [Welch's t-test / Mann-Whitney U / paired t-test / ANOVA / Kruskal-Wallis].
DO NOT use [method to avoid, e.g., "Student's t-test or z-test"].

BEFORE the main test:
1. Run Shapiro-Wilk test for normality on both groups. Print results.
2. Run Levene's test for equal variances. Print results.
3. Based on results above, confirm in a print statement that the chosen test is appropriate, OR recommend an alternative.

OUTPUT REQUIREMENTS:
- Test statistic, degrees of freedom, exact p-value (not "p < 0.05")
- Effect size: [Cohen's d / eta-squared / r]
- 95% confidence interval for the effect
- Print a terminal message: `[TEST] Method: [exact method name] | Result: [significant/not significant] | p = [value] | effect size = [value]`

CONSTRAINTS:
- CRITICAL: The `[METHOD]` print must use a DYNAMICALLY assigned variable — NOT a hardcoded string. Print AFTER all assumption checks, immediately before calling the function. If the method changes based on assumptions, the printed method name must change with it.
- Print the ACTUAL function being called (e.g., `scipy.stats.ttest_ind` with `equal_var=False`)
- Do NOT use any test method different from what I specified above
- If sample size < 30 per group, add a warning about power
```

**Verification checklist**:
- [ ] Read the code — does it call the exact function you requested?
- [ ] Check that `equal_var` parameter matches your Levene's test result
- [ ] Verify p-value precision (not rounded to 2 decimals)
- [ ] Confirm effect size metric matches your field's convention

---

## 3. VISUALIZATION — Publication-Quality Figures

**When to use**: Creating charts, plots, and figures for papers, posters, or presentations.

**Primary risk**: AI uses non-accessible color palettes, wrong DPI, or non-standard formats that journals reject.

```
Create a publication-ready `[chart_type: scatter / violin / heatmap / 3D surface / bar]` using Python's `[matplotlib / seaborn / plotly]`.

DATA: `[dataset.csv]` — show the relationship between:
- X-axis: `[variable_X]` (unit: `[unit]`)
- Y-axis: `[variable_Y]` (unit: `[unit]`)
- Color/hue: `[categorical_variable]` (if applicable)

VISUAL SPECIFICATIONS:
- Color palette: MUST use colorblind-safe scheme (`viridis`, `cividis`, or `Set2`). NEVER use red-green only palettes.
- Figure size: `[width]` x `[height]` inches
- Font size: axis labels ≥ 12pt, tick labels ≥ 10pt, title ≥ 14pt
- DPI: 300 minimum
- Format: save as `.tiff` AND `.svg` (vector for editing)

AXIS & LABELS:
- X-axis label: `[Label (Unit)]`
- Y-axis label: `[Label (Unit)]`
- Title: `[Descriptive title]`
- Legend position: `[upper right / outside right / bottom]`

ADDITIONAL:
- Add error bars showing [SEM / 95% CI / SD] if data includes replicates
- Include a statistical annotation if relevant (e.g., significance brackets)
- Use `plt.tight_layout()` to prevent label clipping
- Print `[FIGURE] Saved: [filename] at [DPI] DPI, [dimensions]`
```

**Verification checklist**:
- [ ] Open the saved figure — are all labels readable?
- [ ] Check colors with a colorblind simulator (e.g., Coblis)
- [ ] Verify DPI matches journal requirements
- [ ] Confirm vector format (.svg/.pdf) is included

---

## 4. FORMAT_CONVERSION — Cross-Software Data Conversion

**When to use**: Converting between file formats (FASTA↔CSV, NetCDF↔DataFrame, etc.) with validation.

**Primary risk**: Silent data loss during conversion; format-specific quirks (e.g., Excel gene name conversion, Ziemann 2016).

```
Convert `[source_file.format_A]` to `[target_format]`.

Extract these features: `[feature_1]`, `[feature_2]`, `[feature_3]`.

VALIDATION REQUIREMENTS (CRITICAL):
1. BEFORE conversion: count total records in source. Print as `[PRE] Source records: [N]`.
2. DURING conversion: for EACH row, validate that all required features are present and correctly typed.
   - If a row has missing or malformed features: issue a `Warning` with the row number and skip it. Do NOT crash or silently discard.
3. AFTER conversion: count total records in output. Print as `[POST] Target records: [M]`.
4. Print a reconciliation report: `[RECON] Source: [N] | Converted: [M] | Skipped: [N-M] | Data loss: [0 / non-zero — INVESTIGATE]`

FORMAT-SPECIFIC GUARDS:
- If source is Excel (.xlsx/.xls): check for auto-converted gene names or date-formatted numbers (Ziemann et al., 2016). Flag any column values that look like "2-Sep", "1-Mar", or scientific notation that wasn't expected.
- If source is FASTA: validate sequence headers match `>identifier` pattern.
- If target is CSV: use `index=False` unless row names are meaningful.

CONSTRAINTS:
- Never overwrite the source file. Always write to a new file.
- Log all skipped/modified rows to `[conversion_log.txt]`.
```

**Verification checklist**:
- [ ] Reconciliation report shows zero unexpected data loss
- [ ] Spot-check 5 random records — do source and target match?
- [ ] Check for Excel auto-formatting artifacts if source is .xlsx
- [ ] Verify character encoding is preserved (UTF-8)

---

## 5. ML_MODELING — Machine Learning / Model Training

**When to use**: Training classifiers, regressors, or clustering models on research data.

**Primary risk**: AI uses default hyperparameters and single train/test splits, producing overoptimistic results.

```
Build a `[Random Forest / SVM / XGBoost / Logistic Regression / Neural Network]` to predict `[target_variable]` using features: `[feature_list]`.

DATA: `[dataset.csv]`

MANDATORY VALIDATION:
- Use STRICT [5-fold / 10-fold] cross-validation. Do NOT do a single train/test split.
- Use stratified folds if the target is categorical (preserve class distribution).

HYPERPARAMETERS (DO NOT use library defaults):
- `[param_1]` = `[value_1]` (rationale: `[why]`)
- `[param_2]` = `[value_2]` (rationale: `[why]`)
- `[param_3]` = `[value_3]` (rationale: `[why]`)

If any hyperparameter is not specified above, STOP and ask me to provide it. Do NOT silently use sklearn defaults.

OUTPUT PER FOLD:
- Confusion matrix
- Precision, Recall, F1-score (per class if multiclass)
- ROC-AUC (binary) or macro-F1 (multiclass)
- Training time

AGGREGATE OUTPUT:
- Mean ± SD for each metric across folds
- `[ML] Model: [name] | CV: [k]-fold | F1 = [mean±sd] | AUC = [mean±sd]`

DATA LEAKAGE PREVENTION:
- All preprocessing (scaling, encoding) MUST be fit on training folds only, then applied to validation fold.
- Print `[LEAKAGE CHECK] Preprocessing fit on train only: [True/False]`
```

**Verification checklist**:
- [ ] Confirm cross-validation is actually k-fold (not a single split)
- [ ] Check that preprocessing is fit_transform on train, transform on test
- [ ] Verify hyperparameters are not sklearn defaults
- [ ] Compare CV scores with a naive baseline (majority class / mean predictor)

---

## 6. UNIT_TESTING — Anti-Lazy Test Generation

**When to use**: Writing tests for analysis functions, data pipelines, or ML code.

**Primary risk**: AI writes "happy path" tests that always pass, giving false confidence (Meyer, Nature 2026).

```
Write comprehensive `pytest` tests for the function `[function_name]` which computes `[description of what it does]`.

CRITICAL: Do NOT only write happy-path tests. Your test suite MUST cover ALL of these adversarial cases:

BOUNDARY INPUTS:
- Zero-length input (empty array, empty DataFrame)
- Single-element input (1 row, 1 value)
- All-identical values (zero variance)
- Input with exactly the minimum required size

NUMERIC EDGE CASES:
- Negative numbers and zero
- Extreme floats: `1e-10`, `1e10`, `-1e10`
- `inf` and `-inf`
- `NaN` (missing values) — should the function raise an error, skip, or impute? Test ALL three expectations.
- `None` values

TYPE MISMATCHES:
- String input where numeric is expected
- Integer input where float is expected (and vice versa)
- Mixed types in a column

SCIENTIFIC CORRECTNESS:
- Verify output against a hand-calculated example (provide the expected values)
- Test that statistical outputs (p-values) are in [0, 1]
- Test that probabilities sum to 1.0 (within floating-point tolerance)

OUTPUT:
- Each test function must have a docstring explaining WHAT it tests and WHY
- Use `pytest.mark.parametrize` for input variations where appropriate
- Print `[TEST SUITE] Total: [N] tests | Edge cases: [M] | Happy path: [K]`
```

**Verification checklist**:
- [ ] Count edge case tests vs. happy path tests (edge cases should be ≥ 60%)
- [ ] Run all tests — do they actually test different code paths?
- [ ] Add one deliberately wrong expected value — does the test catch it?

---

## 7. MATH_MODELING — Mathematical Modeling & Simulation

**When to use**: Solving ODEs/PDEs, running simulations, numerical optimization.

**Primary risk**: AI uses inappropriate solvers or hides numerical instabilities.

````
Write a simulation script using `[equation_name, e.g., Lotka-Volterra predator-prey equations]` to model `[phenomenon]`.

SOLVER: Use `[scipy.integrate.odeint / solve_ivp / custom RK4]` with method `[RK45 / BDF / LSODA]`.
Explain in a comment WHY this solver is appropriate for this system (stiff vs. non-stiff, etc.).

PARAMETERS (define ALL at the top of the script with units):
```python
# === MODEL PARAMETERS ===
# [param_name] = [value]  # [physical/biological meaning] ([units])
# ...
```

INITIAL CONDITIONS:
```python
# === INITIAL CONDITIONS ===
# [variable] = [value]  # [meaning] at t=0
# ...
```

TIME SPAN: t = [t_start] to [t_end], with [N] time steps.

OUTPUT:
1. Time series plot of all state variables
2. Phase portrait (if 2D system)
3. Nullclines (if 2D system)
4. Print steady-state or equilibrium values if they exist

NUMERICAL STABILITY:
- Print `[STABILITY] Max step size used: [value]`
- If solver warnings occur, catch them and print `[WARNING] Solver issue at t=[value]: [message]`
- Run a sensitivity check: perturb initial conditions by ±1% and overlay results

CONSTRAINTS:
- Do NOT use magic numbers anywhere. Every number must be a named constant with units.
- Print the system of equations as a LaTeX-formatted string at the start of output.
````

**Verification checklist**:
- [ ] Compare against known analytical solution (if available)
- [ ] Check conservation laws (energy, mass) are preserved numerically
- [ ] Verify time step is small enough (halve it — does the solution change significantly?)
- [ ] Confirm parameter units are consistent

---

## 8. TEXT_ANALYSIS — Text Mining & Information Extraction

**When to use**: Processing literature, extracting structured data from unstructured text, NLP pipelines.

**Primary risk**: Encoding errors with non-ASCII text; regex patterns that miss edge cases.

```
Write a script to process all `[PDF / TXT / HTML]` files in `[folder_path]`.

GOAL: Extract all sentences containing `[keyword / regex pattern]`.

OUTPUT FORMAT: A structured DataFrame with columns:
- `filename`: source file name
- `page_number`: page where the match was found (or NaN for non-paginated sources)
- `sentence`: the full extracted sentence
- `match_position`: character offset of the match within the sentence

LIBRARY: Use `[PyMuPDF (fitz) / pdfplumber / re module]`.

ENCODING SAFETY:
- Try UTF-8 first, then fall back to latin-1 with a warning: `[ENCODING] Fallback to latin-1 for [filename]`
- Log any files that fail to parse to `[error_log.txt]` with the error message

EXTRACTION RULES:
- Clean extracted text: normalize whitespace, remove hyphenation at line breaks
- If a sentence spans two pages, include both page numbers as `[page1-page2]`
- De-duplicate: if the same sentence appears in multiple files, keep all instances but flag duplicates

SUMMARY:
- Print `[TEXT] Files processed: [N] | Matches found: [M] | Errors: [E]`
- Save results to `[output.csv]` with UTF-8-BOM encoding for Excel compatibility
```

**Verification checklist**:
- [ ] Spot-check 5 extracted sentences — do they match the source?
- [ ] Check error log — were any files silently skipped?
- [ ] Verify encoding handling with a file containing non-ASCII characters
- [ ] Confirm de-duplication logic doesn't remove legitimate repeated findings

---

## 9. CODE_REVIEW — Publication-Ready Code Refactoring

**When to use**: Preparing analysis code for journal submission, supplementary materials, or open-source release.

**Primary risk**: Refactoring changes behavior; AI "improves" code in ways that alter numerical results.

````
Refactor the following research code for submission as supplementary material to `[journal name]` peer review.

ABSOLUTE CONSTRAINTS:
- Do NOT change the algorithmic logic or mathematical computations
- Do NOT change any numerical output — results must be bit-identical before and after
- If you think a computation is wrong, FLAG it with a `# REVIEWER NOTE:` comment but do NOT fix it

FORMATTING:
- PEP-8 compliant (or journal-specific style if specified)
- Maximum line length: 88 characters (black-compatible)
- Use `ruff` formatting conventions

TYPE HINTS:
- Add type hints to ALL function signatures (parameters and return types)
- Use `typing` module for complex types (Optional, Union, List, Dict)
- Add `from __future__ import annotations` for modern syntax

DOCSTRINGS (Google style):
```python
def function_name(param1: type, param2: type) -> return_type:
    """One-line summary of what this function does.

    Detailed explanation of the scientific rationale, including
    assumptions and limitations.

    Args:
        param1: Description with units if applicable.
        param2: Description with expected range/type.

    Returns:
        Description of return value and its format.

    Raises:
        ValueError: When [specific condition].
    """
```

STRUCTURE:
- Group imports: stdlib → third-party → local
- Constants at top, clearly named with units
- Functions ordered: data loading → preprocessing → analysis → visualization → main
- Add a `if __name__ == "__main__":` block with usage example

OUTPUT:
- Print a diff summary: `[REFACTOR] Functions: [N] | Type hints added: [M] | Docstrings added: [K] | Logic changes: 0 (MUST BE ZERO)`
````

**Verification checklist**:

- [ ] Run both versions on the same data — are outputs identical?
- [ ] Check that type hints are accurate (not just `Any` everywhere)
- [ ] Verify docstrings describe the actual behavior, not generic placeholders
- [ ] Confirm zero logic changes in the diff summary

---

## 10. DL_TRAINING — Deep Learning Model Training

**When to use**: Training neural networks (CNN, RNN, Transformer, MLP) with PyTorch or TensorFlow for research.

**Primary risk**: GPU non-determinism silently produces unreproducible results; train/eval mode mismatch corrupts validation metrics; gradient accumulation bugs go unnoticed.

```
Train a `[model_architecture: ResNet-50 / BERT-base / LSTM / custom MLP]` on `[dataset]` using `[PyTorch 2.x / TensorFlow 2.x]` to solve `[task: classification / regression / segmentation / generation]`.

DATA: `[dataset_path]` with input shape `[shape]` and `[N]` classes.

GPU REPRODUCIBILITY (MANDATORY — execute BEFORE any tensor creation):
```python
import torch
import numpy as np
import random

SEED = [42 / your chosen seed]

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
# If using DataLoader with num_workers > 0:
# def seed_worker(worker_id):
#     worker_seed = torch.initial_seed() % 2**32
#     np.random.seed(worker_seed)
# g = torch.Generator()
# g.manual_seed(SEED)
# DataLoader(..., worker_init_fn=seed_worker, generator=g)
```

MODEL ARCHITECTURE:
- Define the model class with explicit layer dimensions in class docstring
- Print parameter count: `[PARAMS] Trainable: {sum(p.numel() for p in model.parameters() if p.requires_grad):,} | Total: {sum(p.numel() for p in model.parameters()):,}`
- Print weight initialization method: `[INIT] [xavier_uniform_ / kaiming_normal_ / orthogonal_]`

TRAINING HYPERPARAMETERS (DO NOT use framework defaults):
- Optimizer: `[Adam / SGD / AdamW / RMSprop]` with learning_rate=`[value]` (rationale: `[why]`)
- Weight decay: `[value]` (rationale: `[why]`)
- Batch size: `[value]` (rationale: `[GPU memory / convergence speed]`)
- Epochs: `[value]`
- Loss function: `[CrossEntropyLoss / MSELoss / BCELoss]` with `[class weights / label smoothing]` 
  if applicable (rationale: `[why]`)
- Learning rate scheduler: `[CosineAnnealingLR / ReduceLROnPlateau / StepLR]` with `[params]` 
  (rationale: `[why]`)
- Gradient clipping: `[value or 'none']` (rationale: `[why]`)

TRAINING LOOP STRUCTURE (print mode switches explicitly):
```python
for epoch in range(num_epochs):
    # === TRAIN ===
    model.train()
    print(f"[MODE] Epoch {epoch+1}/{num_epochs} — TRAIN mode")
    train_loss = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()  # MUST be at top of step
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        if gradient_clip_val:
            torch.nn.utils.clip_grad_norm_(model.parameters(), gradient_clip_val)
        optimizer.step()
        train_loss += loss.item()
    
    # === VALIDATE ===
    model.eval()
    print(f"[MODE] Epoch {epoch+1}/{num_epochs} — EVAL mode")
    val_loss = 0.0
    with torch.no_grad():
        for data, target in val_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            val_loss += criterion(output, target).item()
    
    # Scheduler step (AFTER validation, not before)
    scheduler.step(val_loss)  # or scheduler.step()
    
    print(f"[TRAIN] Epoch {epoch+1}: Train Loss={train_loss/len(train_loader):.4f} | Val Loss={val_loss/len(val_loader):.4f}")
```

DATA LEAKAGE PREVENTION:
- Data augmentation (RandomCrop, RandomHorizontalFlip, etc.) MUST be in `train_transform` ONLY
- Validation transform must be deterministic (only Resize + Normalize + ToTensor)
- Do NOT shuffle the validation DataLoader
- Split train/val BEFORE applying any transforms

ENVIRONMENT DOCUMENTATION:
- Print GPU info: `[GPU] Device: {torch.cuda.get_device_name(0)} | VRAM: {torch.cuda.get_device_properties(0).total_memory/1e9:.1f} GB`
- Print CUDA/cuDNN versions: `[ENV] CUDA: {torch.version.cuda} | cuDNN: {torch.backends.cudnn.version()}`
- Print package versions: `[ENV] PyTorch: {torch.__version__} | NumPy: {np.__version__}`
- Time each epoch and print `[TIME] Epoch [N]: [seconds]s (train) + [seconds]s (val) = [total]s`

OUTPUT:
- Save best model (by validation loss): `torch.save(model.state_dict(), 'best_model.pth')`
- Save training history as CSV: columns = [epoch, train_loss, val_loss, learning_rate, epoch_time]
- Print final summary: `[DL] Model: [name] | Best Val Loss: [value] at epoch [N] | Total params: [count] | Training time: [total]s`
```

**Verification checklist**:
- [ ] Run the script twice with the same seed — are loss curves identical?
- [ ] Check that `model.train()` appears BEFORE the train loop, `model.eval()` before validation
- [ ] Verify `optimizer.zero_grad()` is at the TOP of each training step
- [ ] Confirm validation uses `torch.no_grad()` and deterministic transforms
- [ ] Check GPU memory usage doesn't grow across epochs (memory leak)
- [ ] Verify best model checkpoint actually loads and produces correct output

---

## 11. CS_BENCHMARKING — Algorithm Benchmarking & Complexity Analysis

**When to use**: Comparing algorithm performance, measuring time/space complexity, profiling code, generating benchmark reports.

**Primary risk**: AI compares algorithms under unequal conditions (different hardware loads, warm-up not excluded, single-run results presented as stable).

```
Benchmark `[algorithm_A]`, `[algorithm_B]`, and `[algorithm_C]` on `[task: sorting / search / graph traversal / matrix ops / string matching]`.

IMPLEMENTATION REQUIREMENTS:
- Implement ALL algorithms from scratch in `[Python / C++ / Rust]` — do NOT use library implementations
- Use identical data structures and input format across all implementations
- Document each algorithm's expected time complexity in Big-O notation in the docstring

TEST DATA:
- Generate synthetic test data with these scale levels: `[N=100, N=1,000, N=10,000, N=100,000]`
- Include these edge cases: `[already sorted / reverse sorted / all identical / random]`
- For each scale level, generate `[K=5]` independent random datasets to measure variance

MEASUREMENT PROTOCOL:
```python
import time
import tracemalloc  # or memory_profiler

for algorithm in [alg_A, alg_B, alg_C]:
    for n in [100, 1_000, 10_000, 100_000]:
        for data_variant in ['random', 'sorted', 'reverse', 'identical']:
            # Generate data at scale n
            data = generate_data(n, pattern=data_variant)
            
            # WARM-UP: run once, discard result (JIT compilation, cache warm-up)
            _ = algorithm(data)
            
            # Timed runs
            times = []
            for run in range(K):
                t_start = time.perf_counter()  # perf_counter, not time()
                result = algorithm(data)
                t_end = time.perf_counter()
                times.append(t_end - t_start)
            
            print(f"[BENCH] {algorithm.__name__} | n={n} | {data_variant} | "
                  f"mean={np.mean(times):.6f}s | std={np.std(times):.6f}s")
```

MEMORY PROFILING:
- Measure peak memory usage for each algorithm at each scale level
- Print `[MEM] {algorithm.__name__} | n={n} | peak={peak_mb:.1f} MB`
- If using `tracemalloc`: start before the algorithm, take snapshot after, compute diff

CORRECTNESS VERIFICATION:
- Verify ALL algorithms produce IDENTICAL output for the same input
- If outputs differ, print `[MISMATCH] {alg_A.__name__} vs {alg_B.__name__} differ at n={n}` and STOP
- Use a reference brute-force solution for small n to validate correctness

OUTPUT — Complexity Analysis:
```
[BENCHMARK SUMMARY]
Algorithm          | Expected O()    | Measured scaling | Memory O()   | Status
--------------------|-----------------|------------------|--------------|--------
[alg_A]            | O([n log n])    | [observed]       | O([n])       | [PASS/FAIL]
[alg_B]            | O([n^2])        | [observed]       | O([1])       | [PASS/FAIL]
```

- Generate a log-log plot of runtime vs. input size (all algorithms on one plot)
- Fit a power law (y = a * n^b) to each algorithm's runtime data and print the fitted exponent b
- Compare fitted exponent against theoretical complexity

CONSTRAINTS:
- CRITICAL: Disable CPU frequency scaling and turbo boost during benchmarks (or document that they were not controlled)
- Use `time.perf_counter()` for timing (monotonic, high-resolution), NOT `time.time()`
- Run benchmarks on an idle machine — print `[ENV] CPU load at start: {psutil.cpu_percent()}%`
- Record Python version, OS, CPU model, and RAM at the top of output
```

**Verification checklist**:
- [ ] Run benchmarks twice — are timing results within 5%?
- [ ] Verify that warm-up runs are excluded from timing
- [ ] Check that all algorithms produce identical outputs
- [ ] Confirm log-log plot slope matches theoretical complexity
- [ ] Test with smallest input (n=0 or n=1) — does any algorithm crash?
- [ ] Check memory measurements are monotonically related to input size
