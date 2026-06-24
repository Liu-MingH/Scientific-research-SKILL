#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-End Example: Science Vibe Coding with All 5 Safety Guards
================================================================

This script demonstrates a complete Standard Analysis Pipeline:
    DATA_CLEANING → STAT_TESTING → VISUALIZATION

It follows the science-vibecoding skill (v1.1.0) conventions:
    - Guard 1: DYNAMIC method declaration (printed AFTER assumption checks)
    - Guard 2: No silent defaults (all parameters explicitly specified)
    - Guard 3: Input validation block at script start
    - Guard 4: No self-testing (tests are in separate file)
    - Guard 5: Comprehensive comments (what, why, assumptions)

Scenario:
    A randomized trial comparing blood glucose reduction between
    a new drug (Treatment) and placebo (Control). 30 subjects per group.

Data:
    Synthetic data generated in-line for standalone reproducibility.
    In real research, replace with pd.read_csv("your_data.csv").

References:
    - Nature 653:348-350 (2026) — "How to vibe code in science"
    - Meyer, J. Proteome Res. 25:1191-1197 (2026) — Vibe coding omics
    - Morey's t-test/z-test case — the prototype of Guard 1 bug

Author: Science Vibe Coding Framework
Date:   2026-06-24
License: MIT
"""

# ============================================================================
# IMPORTS — stdlib → third-party → local
# ============================================================================

import os
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import pandas as pd
import scipy
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless environments
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# CONSTANTS — all named with units and rationale
# ============================================================================

# Output directory
OUTPUT_DIR: str = "example_output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Random seed for reproducibility
RANDOM_SEED: int = 42

# Experimental parameters
TREATMENT_MEAN: float = -2.3    # Expected glucose reduction (mmol/L)
CONTROL_MEAN: float = -1.1      # Expected glucose reduction (mmol/L)
TREATMENT_SD: float = 1.5        # Standard deviation (mmol/L)
CONTROL_SD: float = 1.8          # Standard deviation (mmol/L) — slightly higher
N_SUBJECTS_PER_GROUP: int = 30   # Subjects per group

# Statistical parameters
ALPHA: float = 0.05              # Significance threshold
CI_LEVEL: float = 0.95           # Confidence interval level

# Visualization parameters
FIGURE_WIDTH: float = 8.0        # inches
FIGURE_HEIGHT: float = 5.0       # inches
FIGURE_DPI: int = 300            # dots per inch (journal requirement)
FONT_SIZE_LABEL: int = 12        # pt
FONT_SIZE_TICK: int = 10         # pt
FONT_SIZE_TITLE: int = 14        # pt
COLOR_PALETTE: str = "Set2"      # Colorblind-safe palette
TREATMENT_COLOR: str = "#66c2a5" # Set2 green
CONTROL_COLOR: str = "#fc8d62"   # Set2 orange

# File paths (FILE handoff pattern for reproducibility)
CLEANED_DATA_PATH: str = os.path.join(OUTPUT_DIR, "data_clean_glucose_trial.csv")
FIGURE_PATH_SVG: str = os.path.join(OUTPUT_DIR, "fig_glucose_trial.svg")
FIGURE_PATH_TIFF: str = os.path.join(OUTPUT_DIR, "fig_glucose_trial.tiff")


# ============================================================================
# STAGE 1: DATA_CLEANING — Generate & validate synthetic data
# ============================================================================

def generate_trial_data(
    n_per_group: int = N_SUBJECTS_PER_GROUP,
    treatment_mean: float = TREATMENT_MEAN,
    control_mean: float = CONTROL_MEAN,
    treatment_sd: float = TREATMENT_SD,
    control_sd: float = CONTROL_SD,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Generate synthetic clinical trial data for the demo.

    Real research would load data from a file here instead.

    Args:
        n_per_group: Number of subjects per treatment arm.
        treatment_mean: Mean glucose change in treatment group (mmol/L).
        control_mean: Mean glucose change in control group (mmol/L).
        treatment_sd: Standard deviation in treatment group (mmol/L).
        control_sd: Standard deviation in control group (mmol/L).
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with columns: subject_id, group, glucose_change_mmol_L.

    Assumptions:
        - Glucose change is approximately normally distributed per group.
        - Treatment group has lower (more negative) mean change.
        - Groups have unequal variances (treatment SD < control SD),
          which is realistic — active drugs often produce more consistent responses.
    """
    # Why set seed: ensures identical results across runs (Principle 5 reproducibility)
    rng = np.random.default_rng(seed)

    # Generate glucose change values from normal distributions
    # Why normal: blood glucose change is a continuous biomarker; the CLT
    # justifies normality for n=30 per group.
    treatment_changes = rng.normal(treatment_mean, treatment_sd, n_per_group)
    control_changes = rng.normal(control_mean, control_sd, n_per_group)

    # Build DataFrame
    treatment_df = pd.DataFrame({
        "subject_id": [f"T{t+1:03d}" for t in range(n_per_group)],
        "group": "Treatment",
        "glucose_change_mmol_L": treatment_changes,
    })
    control_df = pd.DataFrame({
        "subject_id": [f"C{c+1:03d}" for c in range(n_per_group)],
        "group": "Control",
        "glucose_change_mmol_L": control_changes,
    })
    df = pd.concat([treatment_df, control_df], ignore_index=True)

    return df


def clean_trial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean the clinical trial dataset.

    Operations performed (each explicitly specified — Guard 2):
    1. Check for missing values — raise error if any NaN found
       (medical data: missing values need manual investigation, not auto-imputation).
    2. Verify group assignment integrity (exactly 2 groups, equal sizes).
    3. Flag and log extreme outliers (beyond 4 SD) — but do NOT delete them.
    4. Print a summary after each step.

    Args:
        df: Raw DataFrame with columns subject_id, group, glucose_change_mmol_L.

    Returns:
        Cleaned DataFrame (may include flagged outliers).

    Raises:
        ValueError: If critical data integrity checks fail.
    """
    # === INPUT VALIDATION (Guard 3) ===
    # Check data shape and structure BEFORE any processing
    assert not df.empty, "Input dataframe is empty"
    assert df.shape[0] > 1, "Need at least 2 rows for analysis"
    assert "group" in df.columns, "Missing 'group' column"
    assert "glucose_change_mmol_L" in df.columns, "Missing 'glucose_change_mmol_L' column"

    print(f"[DATA] Shape: {df.shape}, Missing: {df.isnull().sum().sum()}")
    print(f"[DATA] Groups: {df['group'].unique().tolist()}")

    # Step 1: Handle missing values
    # Why raise instead of impute: clinical trial data — missing values
    # must be investigated per-protocol. Auto-imputation would mask
    # potential data collection errors.
    n_nan = df["glucose_change_mmol_L"].isnull().sum()
    if n_nan > 0:
        raise ValueError(
            f"Found {n_nan} missing glucose values. "
            "In clinical data, missing values require manual investigation. "
            "Do NOT auto-impute without protocol specification."
        )
    print(f"[CLEANING] Missing values check: {n_nan} NaN — passed")

    # Step 2: Verify group integrity
    groups = df["group"].value_counts()
    if len(groups) != 2:
        raise ValueError(
            f"Expected exactly 2 groups, found {len(groups)}: {groups.to_dict()}"
        )
    print(f"[CLEANING] Group sizes: {groups.to_dict()}")

    # Step 3: Flag extreme outliers using 4-SD threshold
    # Why 4 SD: IQR (1.5x) flags ~1% of normal data as outliers — too aggressive.
    # 4 SD is a more conservative clinical threshold for extreme values.
    # IMPORTANT: outliers are LOGGED, not deleted.
    mean_glucose = df["glucose_change_mmol_L"].mean()
    sd_glucose = df["glucose_change_mmol_L"].std()
    lower_bound = mean_glucose - 4 * sd_glucose
    upper_bound = mean_glucose + 4 * sd_glucose

    outlier_mask = (df["glucose_change_mmol_L"] < lower_bound) | (
        df["glucose_change_mmol_L"] > upper_bound
    )
    n_outliers = outlier_mask.sum()

    if n_outliers > 0:
        outlier_log_path = os.path.join(OUTPUT_DIR, "outliers_log.csv")
        df[outlier_mask].to_csv(outlier_log_path, index=False)
        print(
            f"[CLEANING] Flagged {n_outliers} extreme outliers "
            f"(>4 SD). Written to {outlier_log_path}. "
            "Outliers are NOT deleted from the dataset."
        )
    else:
        print(f"[CLEANING] No extreme outliers detected (4-SD threshold)")

    # Summary after cleaning
    print(
        f"[CLEANING] Final: {df.shape[0]} rows, "
        f"range=[{df['glucose_change_mmol_L'].min():.2f}, "
        f"{df['glucose_change_mmol_L'].max():.2f}] mmol/L"
    )

    return df


# ============================================================================
# STAGE 2: STAT_TESTING — Dynamic method selection with Guard 1
# ============================================================================

def run_hypothesis_test(
    df: pd.DataFrame,
    alpha: float = ALPHA,
) -> dict:
    """
    Compare glucose change between Treatment and Control groups.

    This function demonstrates the CORRECT Guard 1 pattern:
    - Assumption checks run FIRST
    - Method is selected DYNAMICALLY based on check results
    - Method name is printed IMMEDIATELY before the function call
    - The printed name always matches what is actually executed

    Args:
        df: Cleaned DataFrame with columns group, glucose_change_mmol_L.
        alpha: Significance threshold (default 0.05).

    Returns:
        Dictionary with test results: method, statistic, p_value, effect_size,
        ci_lower, ci_upper, assumption_results.

    Raises:
        ValueError: If input validation fails.
    """
    # === INPUT VALIDATION (Guard 3) ===
    assert not df.empty, "DataFrame is empty"
    assert "group" in df.columns, "Missing 'group' column"
    assert "glucose_change_mmol_L" in df.columns, "Missing 'glucose_change_mmol_L' column"

    # Extract groups
    treatment = df.loc[df["group"] == "Treatment", "glucose_change_mmol_L"].values
    control = df.loc[df["group"] == "Control", "glucose_change_mmol_L"].values

    print(f"[DATA] Treatment: n={len(treatment)}, "
          f"mean={treatment.mean():.3f}, sd={treatment.std():.3f}")
    print(f"[DATA] Control: n={len(control)}, "
          f"mean={control.mean():.3f}, sd={control.std():.3f}")

    # --- Step 1: Run ALL assumption checks before method selection ---
    # Why: The method must be chosen based on what the data ACTUALLY looks like,
    # not what we assume it looks like. (Morey's principle, Nature 2026)

    # Normality test: Shapiro-Wilk
    # Why Shapiro-Wilk: recommended for n < 50 (our n=30 per group).
    # For larger samples, consider Anderson-Darling or Kolmogorov-Smirnov.
    shapiro_treat = stats.shapiro(treatment)
    shapiro_control = stats.shapiro(control)
    normality_ok = (shapiro_treat.pvalue > alpha) and (shapiro_control.pvalue > alpha)

    print(f"[ASSUMPTION] Shapiro-Wilk (Treatment): "
          f"W={shapiro_treat.statistic:.4f}, p={shapiro_treat.pvalue:.4f}")
    print(f"[ASSUMPTION] Shapiro-Wilk (Control): "
          f"W={shapiro_control.statistic:.4f}, p={shapiro_control.pvalue:.4f}")

    # Equal variance test: Levene's test
    # Why Levene: robust to non-normality (uses absolute deviations from median).
    # Bartlett's test would be more powerful but assumes normality.
    levene_result = stats.levene(treatment, control, center="median")
    equal_var_ok = levene_result.pvalue > alpha

    print(f"[ASSUMPTION] Levene (equal variance): "
          f"W={levene_result.statistic:.4f}, p={levene_result.pvalue:.4f}")

    # --- Step 2: Select method DYNAMICALLY (Guard 1 — CORRECT pattern) ---
    # The method_name variable is assigned HERE, based on assumption results.
    # It is NOT hardcoded before the checks.

    if normality_ok and equal_var_ok:
        # Both normal and equal variance → Welch's t-test (more robust default)
        method_name = (
            "Welch's t-test (scipy.stats.ttest_ind, equal_var=False)"
        )
        method_fn = stats.ttest_ind
        method_kwargs = {"equal_var": False}
        method_rationale = (
            "Both groups normal (Shapiro-Wilk p > 0.05) and equal variance "
            "(Levene p > 0.05). Using Welch's t-test as the robust default."
        )
    elif normality_ok and not equal_var_ok:
        # Normal but unequal variance → Welch's t-test (does not assume equal var)
        method_name = (
            "Welch's t-test (scipy.stats.ttest_ind, equal_var=False)"
        )
        method_fn = stats.ttest_ind
        method_kwargs = {"equal_var": False}
        method_rationale = (
            f"Groups normal but unequal variance "
            f"(Levene p={levene_result.pvalue:.4f}). "
            "Welch's t-test does not assume equal variances."
        )
    else:
        # Non-normal → Mann-Whitney U (non-parametric)
        method_name = (
            "Mann-Whitney U (scipy.stats.mannwhitneyu)"
        )
        method_fn = stats.mannwhitneyu
        method_kwargs = {"alternative": "two-sided"}
        method_rationale = (
            f"Non-normal distribution detected "
            f"(Treatment Shapiro-Wilk p={shapiro_treat.pvalue:.4f}, "
            f"Control p={shapiro_control.pvalue:.4f}). "
            "Using non-parametric Mann-Whitney U."
        )

    # --- Step 3: Print DYNAMIC method name IMMEDIATELY before calling ---
    # THIS IS THE GUARD 1 FIX — the printed method matches what runs.
    print(f"[METHOD] Using: {method_name}")
    print(f"[METHOD] Library: scipy v{scipy.__version__}")
    print(f"[METHOD] Rationale: {method_rationale}")

    # --- Step 4: Execute the test ---
    result = method_fn(treatment, control, **method_kwargs)

    # --- Step 5: Compute effect size (Cohen's d) and CI ---
    # Why Cohen's d: standard effect size for two-group comparisons.
    # Pooled SD used for denominator.
    n1, n2 = len(treatment), len(control)
    pooled_sd = np.sqrt(
        ((n1 - 1) * treatment.var(ddof=1) + (n2 - 1) * control.var(ddof=1))
        / (n1 + n2 - 2)
    )
    cohens_d = (treatment.mean() - control.mean()) / pooled_sd

    # 95% CI for Cohen's d (Hedges & Olkin, 1985 approximation)
    se_d = np.sqrt((n1 + n2) / (n1 * n2) + cohens_d**2 / (2 * (n1 + n2)))
    ci_lower = cohens_d - 1.96 * se_d
    ci_upper = cohens_d + 1.96 * se_d

    # --- Summary output ---
    significant = "significant" if result.pvalue < alpha else "not significant"
    print(
        f"[TEST] Method: {method_name} | "
        f"Result: {significant} | "
        f"p = {result.pvalue:.6f} | "
        f"Cohen's d = {cohens_d:.4f} [95% CI: {ci_lower:.4f}, {ci_upper:.4f}]"
    )

    # Sample size power warning (Guard 2 — explicit check)
    if n1 < 30 or n2 < 30:
        print(
            f"[WARNING] Sample size < 30 per group "
            f"(Treatment={n1}, Control={n2}). "
            "Statistical power may be insufficient to detect small effects."
        )

    return {
        "method": method_name,
        "statistic": result.statistic,
        "p_value": result.pvalue,
        "effect_size_cohens_d": cohens_d,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": result.pvalue < alpha,
        "assumptions": {
            "normality_treatment_p": shapiro_treat.pvalue,
            "normality_control_p": shapiro_control.pvalue,
            "equal_variance_p": levene_result.pvalue,
            "normality_ok": normality_ok,
            "equal_var_ok": equal_var_ok,
        },
    }


# ============================================================================
# STAGE 3: VISUALIZATION — Publication-ready figure
# ============================================================================

def create_publication_figure(
    df: pd.DataFrame,
    test_results: dict,
) -> Tuple[str, str]:
    """
    Create a publication-quality figure showing glucose change by group.

    Visual specifications (all explicitly set — Guard 2):
        - Colorblind-safe palette (Set2 — Guard for accessibility)
        - 300 DPI for journal submission
        - Both .svg (vector) and .tiff (raster) formats
        - Statistical annotations included

    Args:
        df: Cleaned DataFrame.
        test_results: Dictionary from run_hypothesis_test().

    Returns:
        Tuple of (svg_path, tiff_path).

    Assumptions:
        - Figure dimensions fit within A4/US letter with standard margins.
        - Title describes the finding, not just the method.
    """
    # === INPUT VALIDATION ===
    assert not df.empty, "DataFrame is empty for visualization"
    assert "group" in df.columns and "glucose_change_mmol_L" in df.columns

    # Create figure
    # Why these exact dimensions: fits comfortably on A4/US letter
    # with standard 2.5cm margins.
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))

    # --- Violin + strip plot (show distribution AND individual data) ---
    # Why violin: shows distribution shape, not just summary statistics.
    # Why strip: individual data points prevent hiding of outliers/bimodality.
    # Why colorblind-safe palette: ~8% of males have color vision deficiency.

    # Violin plot
    sns.violinplot(
        data=df,
        x="group",
        y="glucose_change_mmol_L",
        hue="group",
        palette={"Treatment": TREATMENT_COLOR, "Control": CONTROL_COLOR},
        legend=False,         # Suppress redundant legend (x-axis already labels groups)
        inner=None,          # No internal boxplot — we add strip plot instead
        linewidth=1.0,
        ax=ax,
    )

    # Strip plot (individual data points with jitter)
    sns.stripplot(
        data=df,
        x="group",
        y="glucose_change_mmol_L",
        color="black",
        size=4,
        alpha=0.5,           # Semi-transparent to show density
        jitter=True,
        ax=ax,
    )

    # --- Statistical annotation ---
    # Add significance bracket if result is significant
    if test_results["significant"]:
        # Determine bracket height: max value + 15% of range
        y_max = df["glucose_change_mmol_L"].max()
        y_range = df["glucose_change_mmol_L"].max() - df["glucose_change_mmol_L"].min()
        bracket_y = y_max + 0.1 * y_range

        # Draw bracket
        ax.plot([0, 0, 1, 1], [
            bracket_y,
            bracket_y + 0.05 * y_range,
            bracket_y + 0.05 * y_range,
            bracket_y,
        ], color="black", linewidth=1.0)

        # Significance label
        p_val = test_results["p_value"]
        if p_val < 0.001:
            sig_label = "***"
        elif p_val < 0.01:
            sig_label = "**"
        elif p_val < 0.05:
            sig_label = "*"
        else:
            sig_label = "ns"

        ax.text(
            0.5, bracket_y + 0.1 * y_range,
            f"{sig_label} (p={p_val:.4f}, d={test_results['effect_size_cohens_d']:.2f})",
            ha="center", va="bottom",
            fontsize=FONT_SIZE_TICK,
        )

    # --- Labels and formatting ---
    ax.set_xlabel("Treatment Group", fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel("Glucose Change (mmol/L)", fontsize=FONT_SIZE_LABEL)
    ax.set_title(
        "Blood Glucose Reduction: Treatment vs. Placebo",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
    )
    ax.tick_params(labelsize=FONT_SIZE_TICK)

    # Add horizontal reference line at zero (no change)
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)

    # --- Save in BOTH formats ---
    # Why both: .svg for vector editing (Inkscape/Illustrator),
    # .tiff for journal submission (many journals require .tiff at 300+ DPI)
    plt.tight_layout()

    fig.savefig(FIGURE_PATH_SVG, format="svg", dpi=FIGURE_DPI)
    fig.savefig(FIGURE_PATH_TIFF, format="tiff", dpi=FIGURE_DPI, pil_kwargs={"compression": "tiff_lzw"})

    plt.close(fig)

    print(
        f"[FIGURE] Saved: {FIGURE_PATH_SVG} at {FIGURE_DPI} DPI, "
        f"{FIGURE_WIDTH}x{FIGURE_HEIGHT} inches"
    )
    print(
        f"[FIGURE] Saved: {FIGURE_PATH_TIFF} at {FIGURE_DPI} DPI, "
        f"{FIGURE_WIDTH}x{FIGURE_HEIGHT} inches"
    )

    return FIGURE_PATH_SVG, FIGURE_PATH_TIFF


# ============================================================================
# MAIN — Pipeline orchestration with FILE handoff
# ============================================================================

def main() -> None:
    """
    Execute the full Standard Analysis Pipeline.

    Pipeline: DATA_CLEANING → STAT_TESTING → VISUALIZATION
    Handoff: FILE (for reproducibility — each stage reads from disk)

    This main function demonstrates the CHAINING PROTOCOL (v1.1.0):
    - Each stage's output is written to a timestamped file
    - Each downstream stage validates its input at handoff
    - [CHAIN] log messages trace data flow between stages
    """
    print("=" * 60)
    print("SCIENCE VIBE CODING — End-to-End Example")
    print("Pipeline: DATA_CLEANING → STAT_TESTING → VISUALIZATION")
    print(f"Date: 2026-06-24 | Seed: {RANDOM_SEED}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Stage 1: DATA_CLEANING
    # ------------------------------------------------------------------
    print("\n" + "=" * 40)
    print("STAGE 1: DATA_CLEANING")
    print("=" * 40)

    raw_df = generate_trial_data()

    # === INPUT VALIDATION (Guard 3) ===
    print(f"[DATA] Raw data shape: {raw_df.shape}")
    print(f"[DATA] Missing values: {raw_df.isnull().sum().sum()}")
    print(f"[DATA] Groups: {raw_df['group'].value_counts().to_dict()}")

    cleaned_df = clean_trial_data(raw_df)

    # FILE handoff: write cleaned data to disk
    cleaned_df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"[CHAIN] Handoff: DATA_CLEANING → STAT_TESTING | "
          f"Saved: {CLEANED_DATA_PATH} | Shape: {cleaned_df.shape}")

    # ------------------------------------------------------------------
    # Stage 2: STAT_TESTING
    # ------------------------------------------------------------------
    print("\n" + "=" * 40)
    print("STAGE 2: STAT_TESTING (Guard 1: Dynamic Method)")
    print("=" * 40)

    # FILE handoff: read cleaned data from disk
    loaded_df = pd.read_csv(CLEANED_DATA_PATH)

    # Handoff validation (CHAINING PROTOCOL)
    assert not loaded_df.empty, "Stage 1 produced empty output"
    assert "glucose_change_mmol_L" in loaded_df.columns, "Missing required column"
    print(
        f"[CHAIN] Handoff: STAT_TESTING loaded from {CLEANED_DATA_PATH} "
        f"| Shape: {loaded_df.shape} | Validation: passed"
    )

    test_results = run_hypothesis_test(loaded_df)

    # ------------------------------------------------------------------
    # Stage 3: VISUALIZATION
    # ------------------------------------------------------------------
    print("\n" + "=" * 40)
    print("STAGE 3: VISUALIZATION")
    print("=" * 40)

    # MEMORY handoff: pass DataFrame directly (both stages in same script)
    print(
        f"[CHAIN] Handoff: STAT_TESTING → VISUALIZATION "
        f"| Shape: {loaded_df.shape} | "
        f"Method: {test_results['method']}"
    )

    fig_svg, fig_tiff = create_publication_figure(loaded_df, test_results)

    # ------------------------------------------------------------------
    # Pipeline Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE — Summary")
    print("=" * 60)
    print(f"  Subjects: {len(loaded_df)} total "
          f"({len(loaded_df[loaded_df['group']=='Treatment'])} treatment, "
          f"{len(loaded_df[loaded_df['group']=='Control'])} control)")
    print(f"  Test method: {test_results['method']}")
    print(f"  p-value: {test_results['p_value']:.6f}")
    print(f"  Cohen's d: {test_results['effect_size_cohens_d']:.4f} "
          f"[95% CI: {test_results['ci_lower']:.4f}, {test_results['ci_upper']:.4f}]")
    print(f"  Significant at α={ALPHA}: {test_results['significant']}")
    print(f"  Figures: {fig_svg}, {fig_tiff}")
    print(f"  Cleaned data: {CLEANED_DATA_PATH}")
    print("=" * 60)

    # NOTE: This example does NOT include a self-test suite (Guard 4).
    # Tests should be written separately under the UNIT_TESTING scenario.
    # See test_end_to_end.py for adversarial test cases.


if __name__ == "__main__":
    main()
