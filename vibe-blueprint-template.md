# Vibe Blueprint Template

A reproducibility document for AI-assisted scientific code generation. Based on the "vibe blueprint" concept proposed by Jesse Meyer (J. Proteome Res., 2026).

**Purpose**: Record everything needed for another researcher to reproduce your AI-assisted analysis from scratch, without access to your conversation history.

---

## How to Use

Generate this document alongside every piece of AI-assisted scientific code. Fill in each section as you work. This is your reproducibility insurance policy.

---

# Vibe Blueprint: [Project Title]

**Author**: [Your Name]
**Date**: [YYYY-MM-DD]
**Associated Paper**: [Paper title or "N/A"]
**Repository**: [GitHub/GitLab URL or "To be created"]

---

## 1. Environment

| Item | Value |
|------|-------|
| AI Tool | [e.g., Claude Code, GitHub Copilot, Cursor, Replit Agent] |
| Model | [e.g., claude-opus-4-20250514, gpt-4o-2024-08-06] |
| API Version | [if applicable] |
| Runtime | [e.g., Python 3.11.7, R 4.3.2] |
| OS | [e.g., macOS 15.1, Windows 11, Ubuntu 24.04] |
| Key Libraries | [library==version for all major dependencies] |

## 2. Prompt Log

Record EVERY prompt sent to the AI, in order. Include the full text, not summaries.

### Prompt 1: [Purpose]

**Timestamp**: [HH:MM]
**Full prompt text**:

```
[Paste the exact prompt here]
```

**AI response summary**: [What the AI generated — code files, line counts, any errors]
**Cost**: [$X.XX in tokens/credits]
**Time**: [X minutes from prompt to working output]

### Prompt 2: [Purpose]

**Timestamp**: [HH:MM]
**Full prompt text**:

```
[Paste the exact prompt here]
```

**AI response summary**: [What changed — fixes, additions, etc.]
**Cost**: [$X.XX]
**Time**: [X minutes]

*[Continue for all prompts...]*

### Prompt Summary

| # | Purpose | Cost | Time | Outcome |
|---|---------|------|------|---------|
| 1 | Initial prototype | $X.XX | X min | [working / needed fix] |
| 2 | Bug fix | $X.XX | X min | [resolved / new issue] |
| ... | ... | ... | ... | ... |
| **Total** | — | **$X.XX** | **X min** | — |

## 3. Data Description

| Item | Detail |
|------|--------|
| Dataset name | [filename or URL] |
| Source | [Where the data came from] |
| Size | [rows × columns, or file size] |
| Format | [CSV, FASTA, NetCDF, etc.] |
| Preprocessing before AI | [Any cleaning done before giving data to AI] |
| Synthetic data used? | [Yes/No — if yes, describe generation method] |

## 4. Generated Code Summary

| File | Lines | Purpose |
|------|-------|---------|
| [main.py] | [N] | [Primary analysis script] |
| [plot.py] | [N] | [Visualization module] |
| [utils.py] | [N] | [Helper functions] |
| **Total** | **[N]** | — |

## 5. Verification Results

### Automated Tests

| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| [Test name] | [input description] | [expected output] | [actual output] | PASS / FAIL |
| ... | ... | ... | ... | ... |

### Manual Review

- [ ] Method fidelity check: [PASS/FAIL — notes]
- [ ] No silent data modification: [PASS/FAIL — notes]
- [ ] Output sanity check: [PASS/FAIL — notes]
- [ ] Reproducibility (seed test): [PASS/FAIL — notes]
- [ ] Data leakage check (ML): [PASS/FAIL / N/A]

### Independent Validation

Describe any validation against ground truth, reference implementations, or published results:

```
[Describe how you validated the AI output against known-correct results]
```

## 6. Modifications After Generation

Record any manual edits you made to the AI-generated code:

| File | Lines Changed | What | Why |
|------|--------------|------|-----|
| [file] | [lines] | [description of change] | [reason] |
| ... | ... | ... | ... |

## 7. Known Limitations

List any known issues, edge cases, or scenarios where the code may fail:

1. [Limitation 1]
2. [Limitation 2]
3. ...

## 8. AI Usage Disclosure

Statement for journal submission (adapt to your journal's policy):

> "Portions of the data analysis code were generated with assistance from [AI tool name, version] using natural language prompts. All generated code was manually reviewed, verified against independent implementations, and validated for correctness before use in this study. The complete code, prompts, and verification logs are available at [repository URL]."

## 9. Cost-Benefit Analysis

| Metric | With AI | Estimated Without AI | Ratio |
|--------|---------|---------------------|-------|
| Development time | [X hours] | [Y hours] | [Y/X]x |
| Cost | [$X.XX tokens] | [$Y.YY developer hours] | — |
| Lines of code | [N] | [M estimated] | — |
| Iterations to working code | [N prompts] | [M attempts] | — |

## 10. Lessons Learned

Record insights for future vibe coding sessions:

1. [What worked well]
2. [What went wrong and how you caught it]
3. [What you would do differently]

---

*Blueprint generated using the Science Vibe Coding framework.*
*Template version: 1.0.0*
