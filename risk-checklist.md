# Risk Verification Checklist for Scientific Vibe Coding

Use this checklist BEFORE using any AI-generated code for publication or decision-making. Based on failure cases documented in Nature 653:348-350 (2026) and Pimenova et al. (2025).

---

## Pre-Execution Checks

### 1. Method Fidelity (the "Morey Test")

Named after Richard Morey's discovery that AI labeled its output as a t-test but actually ran a z-test (Nature, 2026).

- [ ] **Read the actual function call** in the generated code. Does it match what you requested?
- [ ] Check for function aliases or wrapper functions that might hide the real method
- [ ] Verify all parameters passed to the function (especially boolean flags like `equal_var`)
- [ ] Print the method name at runtime and compare against your request

```python
# Add this to any statistical code:
import inspect
print(f"[VERIFY] Function called: {inspect.currentframe().f_code.co_name}")
print(f"[VERIFY] Library: {module.__name__} v{module.__version__}")
```

### 2. Silent Data Modification

AI tends to "helpfully" fix data problems without telling you.

- [ ] Search code for `fillna()`, `dropna()`, `interpolate()`, `replace()` — are any used without your instruction?
- [ ] Search for smoothing functions (`savgol_filter`, `rolling().mean()`) — did you ask for smoothing?
- [ ] Check if the code modifies column names, dtypes, or encodings without instruction
- [ ] Verify row counts before and after each processing step

### 3. Default Parameter Trap

Libraries have defaults. AI often doesn't override them.

| Library | Function | Default | Common Issue |
|---------|----------|---------|-------------|
| scipy.stats | `ttest_ind` | `equal_var=True` | Assumes equal variance — often wrong |
| sklearn | `RandomForestClassifier` | `n_estimators=100` | May be too few for your data |
| sklearn | `train_test_split` | `test_size=0.25` | Single split, no cross-validation |
| pandas | `read_excel` | `dtype=None` | Auto-infers types, may misconvert |
| matplotlib | `savefig` | `dpi=100` | Too low for journal publication |
| scipy | `curve_fit` | `maxfev=800` | May fail on complex models |
| torch | `DataLoader` | `num_workers=0` | Single-process loading — bottleneck for GPU training |
| torch | `BatchNorm2d` | `momentum=0.1` | Too aggressive for small batch sizes (< 16) |
| torch | `Adam` | `betas=(0.9, 0.999)` | May oscillate on sparse gradients |
| torch | `CrossEntropyLoss` | `reduction='mean'` | Biased on imbalanced datasets; use class weights |
| torch | `SGD` | `momentum=0` | No momentum by default — significantly slower convergence |
| TensorFlow | `BatchNormalization` | `momentum=0.99` | Opposite of PyTorch — expects values near 1.0 |

- [ ] Identify ALL library function calls in the generated code
- [ ] Look up each function's defaults — are they appropriate for your data?
- [ ] Add explicit parameter values with comments explaining the choice

---

## Post-Execution Checks

### 4. Output Sanity

- [ ] Do p-values fall in [0, 1]?
- [ ] Do probabilities sum to ~1.0?
- [ ] Are effect sizes in the expected range for your field?
- [ ] Do confidence intervals make physical/biological sense?
- [ ] Are there any `NaN` or `inf` values in the output?

### 5. Reproducibility

- [ ] Set a random seed (`np.random.seed(42)`) and run twice — are results identical?
- [ ] For PyTorch: Set `torch.manual_seed(42)`, `torch.cuda.manual_seed_all(42)`, `torch.backends.cudnn.deterministic = True`, `torch.backends.cudnn.benchmark = False` — run twice, loss curves identical?
- [ ] For TensorFlow: Set `tf.random.set_seed(42)` and `os.environ['TF_DETERMINISTIC_OPS'] = '1'` — run twice, loss curves identical?
- [ ] Are all file paths relative (not absolute to your machine)?
- [ ] Are all package versions pinned (`requirements.txt` or `environment.yml`)?
- [ ] Can a colleague run this code on their machine without modification?

### 6. Data Leakage (ML specific)

- [ ] Is preprocessing (scaling, encoding, imputation) fit ONLY on training data?
- [ ] Are test labels completely untouched during feature engineering?
- [ ] In time series: is the split chronological (not random)?
- [ ] In cross-validation: is preprocessing re-fit inside each fold?

### 6a. Data Leakage (DL specific)

- [ ] Are data augmentations applied ONLY to training data, never to validation/test?
- [ ] Is `model.eval()` set before validation and `model.train()` restored after?
- [ ] Are batch normalization statistics computed ONLY on training batches (not validation)?
- [ ] Is `optimizer.zero_grad()` called at the TOP of each training step (not at the bottom)?
- [ ] Is the learning rate scheduler stepping at the correct frequency (per-epoch vs. per-batch)?
- [ ] In distributed training: are random seeds broadcast to ALL workers?
- [ ] Are dropout layers automatically disabled by `model.eval()`? (Verify, don't assume)

---

## Publication Readiness

### 7. Code Quality

- [ ] No hardcoded paths, passwords, or API keys
- [ ] No `print()` statements used for debugging (use `logging` instead)
- [ ] All magic numbers replaced with named constants
- [ ] No commented-out code blocks
- [ ] No `TODO` or `FIXME` comments remaining

### 8. Documentation

- [ ] README explains how to run the code (dependencies, data requirements, expected output)
- [ ] All functions have docstrings with: purpose, parameters, return values, assumptions
- [ ] Key algorithmic choices are explained in comments
- [ ] License file is included (MIT, Apache 2.0, or as required by your institution)

### 9. Journal Compliance

- [ ] Code format matches journal's supplementary material requirements
- [ ] Figure output meets DPI and format specifications
- [ ] Data availability statement is included where required
- [ ] AI tool usage is disclosed per journal policy (check specific journal guidelines)

---

## Red Flags — STOP and Review

If you encounter any of these, STOP and manually review the code:

| Red Flag | Why It's Dangerous | Source |
|----------|-------------------|--------|
| Code runs without errors on first try | Suspicious — complex analysis rarely works first time | Pimenova 2025 |
| AI generates its own test suite | Tests are likely "hilarious" — designed to always pass | Meyer 2026 |
| Output figure "looks right" but you can't explain why | May be smoothed or interpolated without instruction | Morey 2026 |
| Code file grew from 400 to 3000+ lines | Unreadable by both human and AI; debugging is "chaos" | Pimenova 2025 |
| AI changed 30+ files simultaneously | Version control nightmare; changes likely untracked | Pimenova 2025 |
| Results match your hypothesis "too perfectly" | Possible confirmation bias in AI's sycophantic completion | Nature 2026 |
| Training loss hits near-zero in epoch 1 | Overfitting, label leakage, or loss function bug — not "good convergence" | DL research |
| Validation loss is lower than training loss | Likely train/eval mode mismatch, batch norm contamination, or data leakage into val set | DL research |
| GPU utilization stays below 50% | DataLoader bottleneck — `num_workers=0` or I/O-bound preprocessing | DL research |
| 30+ GB GPU memory for small model + small data | Memory leak (accumulating tensors without detach), or batch size too large for hardware | DL research |

---

## Quick Reference: Common AI Substitutions

These are documented cases where AI used a different method than requested:

| You Asked For | AI Might Use Instead | Why It Matters |
|---------------|---------------------|----------------|
| Welch's t-test | Student's t-test or z-test | Fails for unequal variance or small samples |
| Mann-Whitney U | t-test on ranks | Different null hypothesis |
| Bonferroni correction | Benjamini-Hochberg (or vice versa) | Different error rate control |
| Log transform | Square root transform | Different normalization effect |
| Spearman correlation | Pearson correlation | Assumes linearity vs. monotonicity |
| 5-fold CV | Single train/test split | Overestimates performance |
| Median imputation | Mean imputation | Sensitive to outliers |
| IQR outlier detection | Z-score outlier detection | Assumes normality |

---

## Deep Learning Specific Checks

### 10. GPU Reproducibility

- [ ] Are ALL random seeds set before any tensor operation? (Must include: `random.seed`, `np.random.seed`, `torch.manual_seed`, `torch.cuda.manual_seed_all`)
- [ ] Is `torch.backends.cudnn.deterministic = True` set? (cuDNN non-deterministic convolution algorithms will produce different results per run)
- [ ] Is `torch.backends.cudnn.benchmark = False` set? (auto-tuner varies algorithm selection)
- [ ] Is `PYTHONHASHSEED` set via `os.environ`? (affects DataLoader worker shuffling)
- [ ] Run the training script twice with identical seeds — are the loss curves pixel-perfect identical?
- [ ] For multi-GPU: are seeds broadcast to every process? Does `DistributedSampler` use the same seed?

### 11. Training Loop Integrity

- [ ] Is `model.train()` at the TOP of the training loop, `model.eval()` before validation?
- [ ] Is `optimizer.zero_grad()` at the TOP of each step? (Bottom placement causes gradient accumulation)
- [ ] Is `loss.backward()` followed by `optimizer.step()` — not the reverse?
- [ ] If using gradient accumulation: are gradients scaled by `1/accumulation_steps`?
- [ ] Is `torch.no_grad()` wrapping the validation loop?
- [ ] Is the learning rate scheduler stepped AFTER the optimizer (not before) when stepping per-batch?
- [ ] Print `[MODE] train` / `[MODE] eval` at the start of each epoch for audit trail

### 12. Model Architecture Documentation

- [ ] Does the code print total parameter count? (`sum(p.numel() for p in model.parameters())`)
- [ ] Does it print trainable vs. frozen parameter counts?
- [ ] Are all layer dimensions, activation functions, and normalization layers explicitly documented?
- [ ] Is the input/output shape documented for every module?
- [ ] Are weight initialization methods explicitly specified (not left to library defaults)?

### 13. Compute Environment

- [ ] Are GPU model, CUDA version, cuDNN version, and PyTorch/TensorFlow version printed at startup?
- [ ] Is total GPU memory reported (`torch.cuda.get_device_properties`)?
- [ ] Is per-epoch training time logged (for scaling estimates)?
- [ ] Are all package versions pinned in `requirements.txt` or `environment.yml`?

---

## Emergency Procedures

### If you discover an error AFTER publication:

1. Document the exact discrepancy (method used vs. method reported)
2. Re-run analysis with the correct method
3. Assess whether conclusions change
4. Contact the journal editor with a correction or erratum
5. Update the Vibe Blueprint with the lesson learned

### If the code "works" but you can't explain it:

1. Do NOT submit it for publication
2. Ask the AI to explain the code line-by-line
3. Compare against a textbook or reference implementation
4. If still unclear, consult a domain expert or statistician
5. Remember: "Vibe coding is not a substitute for understanding" (Meyer, 2026)
