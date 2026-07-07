# Deep Review — 10-Pass, 5-Reviewer Panel

Use this for a journal-level, adversarial, submission-readiness revision. It is the heavy mode.
Ten passes, each with a five-reviewer panel and a distinct focus, each pass committed
separately. The bottom-up read-then-fix traversal from `SKILL.md` still governs *how* each pass
reads and edits — the panel decides *what* to look for in that pass.

The defining principle: **do not only comment — apply.** Every pass reviews, identifies
concrete weaknesses, proposes improvements, and applies the safe ones to the LaTeX source,
then commits. Pass *k+1* reviews the output of pass *k*, not the original.

Preserve mathematical notation and claims unless a change is clearly safe or the user asked for
a math correction (the non-negotiables in `SKILL.md` still hold).

---

## The five reviewer personas (run every pass)

These are simulated roles, not real people. Do not invent names or affiliations. If your host
has sub-agents, spawn one per persona for independence; otherwise adopt each lens in turn.

**Expert reviewers (at least three):**

- **R1 — Technical correctness.** Is the model right? Are assumptions, terminology, and claims
  correct? Hunt for wrong definitions, unsupported claims, weak assumptions, notation
  inconsistency, and missing explanations.
- **R2 — Structure and contribution.** Is there a strong research story? Check motivation,
  gap, contributions, section order, paragraph flow, and whether each section serves its role
  (`references/paper-structure.md`).
- **R3 — Academic writing.** Clarity, concision, grammar, sentence and paragraph structure.
  Remove verbose, vague, inflated, or machine-generated prose. Avoid unnecessary semicolons.
  Enforce `references/writing-style.md`.

**Adversarial reviewers (at least two), skeptical, looking for reasons to reject:**

- **R4 — Adversarial novelty.** Is it actually novel? Is the contribution incremental, obvious,
  weakly differentiated from prior work, or overstated? Flag where positioning must sharpen.
- **R5 — Adversarial evidence and reproducibility.** Are claims backed by analysis,
  experiments, citations, and reproducibility detail? Is the evaluation fair — right baselines,
  justified metrics, results interpreted without overclaiming?

---

## Per-pass procedure (repeat for passes 1–10)

### Step 1 — Working copy
Create the pass input without overwriting the previous pass.
- Single-file project: `review_versions/main_pass_01.tex`, `..._02.tex`, ...
- Multi-file project (`sections/*.tex`): a per-pass directory `review_versions/pass_01/`,
  `pass_02/`, ... Each pass preserves both its input and output.

### Step 2 — Run the five-reviewer panel
For each reviewer record: (1) main concerns, (2) specific locations, (3) required changes,
(4) severity `critical | major | minor`, (5) apply-now vs author-judgment. Save the report to
`review_reports/pass_01_review.md` with the five sections plus a consolidated plan:

```
# Pass XX Review Report
## Reviewer 1: Technical Correctness
## Reviewer 2: Structure and Contribution
## Reviewer 3: Academic Writing
## Reviewer 4: Adversarial Novelty
## Reviewer 5: Adversarial Evidence and Reproducibility
## Consolidated Improvement Plan
```

### Step 3 — Consolidate the improvement plan
Sort every issue into:
```
A. Changes to apply now (safe)
B. Changes requiring author judgment
C. Citation-needed issues
D. Figure/table/supplement candidates
E. Risky claims or unclear notation
```
Do not apply anything that changes technical meaning, notation, equations, or experimental
claims unless it is clearly safe or explicitly requested.

### Step 4 — Apply the safe improvements to the LaTeX
Edit the pass-specific `.tex` using the bottom-up traversal. If tracked changes are wanted, use
the `changes` package (setup in `SKILL.md` Step 0) and annotate meaningful edits with why:
```latex
\comment[id=CR]{[PASS 03 | R2 | STRUCTURE] Sentence moved to improve paragraph flow.}
\comment[id=CR]{[PASS 05 | R4 | NOVELTY] Claim softened; previous wording overstated the contribution.}
\comment[id=CR]{[PASS 07 | R5 | EVIDENCE] Citation or experimental support may be needed here.}
```
Never put `changes` commands in `.bib`. Make bibliography edits directly and document them.

### Step 5 — Check layout, references, compilation
At minimum `git diff --stat`. If LaTeX tooling exists, `latexmk -pdf main.tex` (or the project
build). Fix syntax errors your edits introduced; do not ignore build failures.

### Step 6 — Commit the pass (separately)
```bash
git status && git diff --stat
git add review_versions/pass_01 review_reports/pass_01_review.md
git commit -m "review pass 01: improve manuscript clarity and structure"
```
Do not collapse passes into one commit. Do not commit build artifacts unless already tracked.

---

## The distinct focus of each pass (do not repeat the same review)

Each pass emphasizes something different. All five personas still participate, but through that
pass's lens.

1. **Global structure.** Section order, missing/redundant sections, is the story clear, are
   problem/gap/method/results aligned.
2. **Introduction and contribution framing.** Motivation, gap, contribution bullets, novelty
   claims, paper organization. Remove inflated or unsupported contribution wording.
3. **Related work and positioning.** Logical grouping, fair comparison, clear gap, citations
   that actually support the claims, any broad negative claim that needs stronger evidence.
4. **System model and problem formulation.** Assumptions, notation, variable definitions,
   problem statement, text↔equation consistency. Do not change equations except for clear
   syntax errors or on explicit request.
5. **Proposed method / analysis.** Method clarity, algorithm flow, derivation explanation,
   assumptions↔results link, distinguishability from baselines.
6. **Evaluation setup.** Dataset/simulator/environment, baselines, metrics, parameters,
   fairness and reproducibility. Flag missing details.
7. **Results and discussion.** Every figure/table explained, conclusions follow from results,
   trends interpreted correctly, limitations visible, no overclaiming.
8. **Figures, tables, algorithms, supplement mapping.** Find text-heavy paragraphs that should
   become a figure, table, algorithm, flowchart, taxonomy, or supplement item, and mark them
   (`references/figures-tables-supplement.md`).
9. **Bibliography and citation integrity.** Follow `references/bibliography.md` in full: every
   `\cite` resolves, no duplicate keys, no malformed entries, Title Case protected with outer
   braces, acronyms braced, repeated-author dashes disabled, uncited entries listed.
10. **Final submission-readiness.** Abstract matches the paper, intro matches contributions,
    related work supports the gap, system model supports the method, evaluation supports the
    claims, conclusion adds no new claims, writing is clear and human-authored, no stray
    semicolons, no excessive repetition, no unresolved review comments left dangling. Produce
    the final file `review_versions/final_reviewed_main.tex` (or `review_versions/final/` for
    multi-file) and commit:
    ```bash
    git commit -m "review pass 10: finalize submission-ready manuscript"
    ```

Suggested commit messages for the middle passes:
```
review pass 02: address technical consistency and notation issues
review pass 03: refine contribution framing and related work
review pass 04: strengthen evidence and reduce overclaiming
review pass 05: improve paragraph flow and readability
review pass 06: adversarial novelty revision
review pass 07: adversarial reproducibility revision
review pass 08: polish figures, tables, and supplement mapping
review pass 09: bibliography and citation integrity
```

---

## Anti-shallow-review rule

A pass is not valid unless it produces **all** of:

1. A reviewer report with all five perspectives.
2. A consolidated improvement plan (A–E).
3. At least one concrete manuscript-level action: a text revision, an inline comment, a
   citation-needed marker, a figure/table/supplement marker, a bibliography fix, a structural
   recommendation, or an unresolved author-judgment note.
4. A new pass-specific `.tex` version or pass directory.
5. A separate git commit.

Do not perform superficial review, and do not merely declare the manuscript "clear". If no safe
edit exists in a pass, explain why, add author-judgment comments where warranted, and still
produce the report and the commit.

---

## Final deep-review summary (after all 10 passes)

```
# Final Multi-Pass Review Summary

## Files created
- review_versions/pass_01/... ... review_versions/final/...

## Git commits
- <hash> review pass 01: ...  ...  <hash> review pass 10: ...

## Major improvements applied
## Remaining author-judgment issues
## Citation-needed issues
## Figure/table/supplement recommendations
## Risky claims or unclear notation
## Compilation status
## Final manuscript path
```

The final response must include the latest commit hash and the path to the final reviewed
manuscript. Do not claim submission-readiness unless every critical and major issue is either
fixed or explicitly listed as requiring author judgment.
