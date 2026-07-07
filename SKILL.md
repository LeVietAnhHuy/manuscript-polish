---
name: manuscript-polish
description: >-
  Multi-agent workflow to polish and revise academic paper manuscripts (LaTeX/.tex,
  also Markdown/Word) to journal-submission quality. It walks the paper bottom-up —
  sentence, paragraph, subsubsection, subsection, section, then the whole manuscript —
  reading then fixing at every level, and enforces plain, precise, non-overclaiming
  academic English (no AI-sounding prose, minimal semicolons). It also checks section
  structure, flags figure/table/supplement candidates, and repairs .bib integrity
  (title-case protection, repeated-author dashes, citation coverage). Includes an
  optional 10-pass, 5-reviewer adversarial panel for deep journal-level revision.
  Use this WHENEVER the user wants to polish, proofread, refine, tighten, "de-AI",
  clean up, or revise a paper / manuscript / .tex / draft, prepare a submission
  (e.g., IoT-J, TNSE, JSAC, APCC, TNSE, IEEE/ACM/Elsevier venues), run a journal-level
  or adversarial review, reduce overclaiming, improve academic writing and flow,
  restructure sections, or fix a bibliography — even if they never say the words
  "skill" or "polish".
---

# Manuscript Polish

A workflow for polishing an academic paper to submission quality by spawning agents
that read and fix the manuscript **bottom-up**, one structural level at a time, in
plain and precise academic English.

The goal is not to rewrite the paper into something that *sounds* impressive. The goal
is a manuscript that a busy reviewer understands on the first read and trusts, because
every sentence is clear, every claim is sized to its evidence, and the structure carries
the story. Fancy prose is a liability here, not an asset.

---

## The one rule that governs everything: read, then fix — bottom-up

However long the paper is, the order of work never changes. Fix small, then zoom out and
re-read the assembled whole, because local edits routinely break the flow around them.

```
read each SENTENCE            → fix it
  end of a PARAGRAPH          → re-read the whole paragraph → fix it
    end of a SUBSUBSECTION    → re-read the whole subsubsection → fix it
      end of a SUBSECTION     → re-read the whole subsection → fix it
        end of a SECTION      → re-read the whole section → fix it
          end of the PAPER    → re-read the whole manuscript → fix it
```

Each level has a different job, so re-reading is never wasted:

| Level | What you are fixing on the re-read |
|---|---|
| Sentence | Word choice, precision, length, overclaim, semicolons, AI-voice |
| Paragraph | One-job-per-paragraph, topic sentence, internal flow, redundancy |
| Subsubsection / Subsection | Order of paragraphs, transitions, consistent terminology, figure/table candidates |
| Section | Does the section deliver its promised role? Gaps, overlaps, forward/back references |
| Whole manuscript | Abstract↔body match, intro↔contributions↔conclusion alignment, notation consistency, no new claims in conclusion, bibliography |

This traversal is the skeleton of both modes below. Do not skip the re-read steps — they
are where most real improvements happen.

---

## Two modes

Pick based on what the user asked for. When unsure, ask; default to Polish.

- **Polish (default).** One thorough bottom-up traversal of the manuscript. Fix wording,
  flow, structure, and obvious problems. Fast, safe, one commit (or a handful). Use for
  "clean this up", "make it read better", "proofread", "tighten the intro", "de-AI this".

- **Deep review (10-pass panel).** Ten passes, each with a five-reviewer panel (three
  expert + two adversarial), each pass with a distinct focus, each pass committed
  separately. Use for "journal-level review", "adversarial review", "get this ready for
  submission", "reviewer 2 is going to hate this — help". This is heavy. Read
  `references/review-panel.md` and follow it exactly. The bottom-up traversal still
  governs how each pass reads and edits.

---

## Non-negotiables (why they matter)

These protect the author from an over-eager editor. Violating them turns a helpful polish
into a dangerous one.

1. **Never change technical meaning, math, or claims.** Preserve every equation, symbol,
   number, label, `\ref`, `\cite`, and units exactly. Do not "fix" a formula unless it is
   a clear LaTeX **syntax** error or the user explicitly asked for a math correction. If a
   claim looks wrong or unsupported, do not silently reword it into something new — flag it
   (see the comment convention below) and let the author decide.

2. **Edit surgically.** Change wording, not substance. Keep the author's voice and the
   paper's terminology. Do not swap a defined term for a synonym — consistent terminology is
   correctness, not repetition to be "varied away". Do not delete content to make prose
   shorter; move detail to a supplement or a figure/table instead (see
   `references/figures-tables-supplement.md`).

3. **Plain, precise, honest English.** This is the house style and it is not optional.
   Full contract in `references/writing-style.md`. In one breath: short sentences, simple
   words, one term per phenomenon, no overclaiming, semicolons only when truly needed, and
   no machine-generated filler.

4. **Preserve, don't destroy.** Work on a copy or a git branch. Never overwrite the
   author's file in place without a recoverable version. Commit as you go.

5. **Report, don't hide.** At the end, tell the author exactly what you changed, what you
   flagged for their judgment, and what you could not safely touch.

---

## Step 0 — Recon and setup (do this before any editing)

Editing before you understand the project is how you break a build. Spend a few minutes here.

1. **Find the source.** Locate the main file (the one with `\documentclass` and
   `\begin{document}`) and any section files pulled in with `\input`/`\include`. Note the
   `\documentclass` and options — they tell you the target venue and column format
   (e.g., `IEEEtran`, `elsarticle`, `acmart`).

2. **Detect the bibliography system.** BibTeX with `\bibliographystyle{IEEEtran}` +
   `\bibliography{...}`, or `biblatex`. This decides how you fix repeated-author dashes
   later. See `references/bibliography.md`.

3. **Set up a safe workspace.**
   - If the project is a git repo: create a branch, e.g. `git switch -c polish/manuscript`.
   - If it is **not** a git repo: `git init` it (or copy the sources into a
     `review_versions/` working copy) so every change is recoverable. Confirm with the user
     before `git init` on a directory you did not create.

4. **Decide tracked changes.** Ask, or infer from the request:
   - *Reviewable diff wanted* (author wants to see and accept/reject each edit) → use the
     `changes` package. If it is not already loaded, add to the preamble:
     ```latex
     \usepackage[authormarkup=none]{changes}
     \definechangesauthor[name={Review}, color=blue]{CR}
     ```
     Then edit with `\added[id=CR]{...}`, `\deleted[id=CR]{...}`,
     `\replaced[id=CR]{new}{old}`, and `\comment[id=CR]{...}`. Never put `changes` commands
     inside `.bib` files.
   - *Clean output wanted* (author just wants the improved text) → edit the `.tex` directly
     and rely on `git diff` as the record. This is the usual default for the Polish mode.

5. **Build the outline and a pre-scan.** Run the bundled helpers to plan the traversal and
   focus attention. They are best-effort heuristics, not judges — they tell you *where to
   look*, never *what to conclude*.
   ```bash
   python scripts/outline.py <main.tex or project dir>      # structure tree + traversal order
   python scripts/style_lint.py <main.tex or project dir>   # overclaim / semicolons / long sentences / AI-tells
   python scripts/bib_check.py <project dir>                # citation coverage + .bib risks
   ```
   Read `scripts/README.md` for what each flag means. Use the outline to divide work and the
   lint hits to prioritize — but you still read every sentence yourself.

---

## Step 1 — The bottom-up traversal (the heart of the workflow)

This is where you "call the agents out to work". The traversal parallelizes naturally: the
smallest units are independent and can be polished at the same time, while each re-read of a
larger unit must wait for its children. Think of it as waves rising from the leaves.

### How to divide the work among agents

- **Work unit = the smallest structural block** (a paragraph, or a short subsubsection).
  Assign each unit to one agent. That agent does the sentence-by-sentence pass *and* the
  paragraph re-read for its unit — the two innermost levels — then edits its span.
- **Consolidation unit = a parent block** (subsubsection → subsection → section). After all
  children of a parent are done, one agent re-reads the assembled parent and fixes flow,
  transitions, terminology drift, and structure, and flags figure/table/supplement
  candidates.
- **Whole manuscript** is the final consolidation (Step 2).

If your host supports parallel sub-agents (e.g., a Task/Agent tool), fan out across
**disjoint** spans so edits never collide, and run consolidation waves only after their
children finish. If your host has no sub-agents, do the exact same procedure yourself,
sequentially, in the same bottom-up order. The order and the re-reads are what matter, not
the concurrency.

### What to hand each agent

Give every spawned agent a tight, self-contained brief so it does not need the whole paper
in context:

- The **exact span** to work on (file + line range, or the section-file path).
- The **writing-style contract**: point it at `references/writing-style.md` (or paste the
  short "style contract" block from there).
- The **non-negotiables** above, especially "never change math/claims; edit surgically".
- The **pre-scan hits** for that span (relevant `style_lint.py` lines), so it starts with
  the known suspects.
- The **surrounding terminology** it must stay consistent with (defined symbols, the exact
  name of the proposed method, key acronyms) so parallel agents do not diverge.
- Instruction to **return a short change log** for its span: what it changed and why, plus
  anything it flagged rather than fixed.

### The per-unit procedure each agent follows

```
For the assigned unit:
  1. Read sentence by sentence. For each sentence, fix:
       - unclear meaning, buried subject, or a sentence doing two jobs → split it
       - long/comma-heavy sentence (>~30 words, stacked "which/thereby/thus/moreover") → shorten
       - overclaim words (solve, guarantee, optimal, comprehensive, superior, significantly...) → size to evidence
       - a difficult word where a simple one is exact → simplify
       - vague term where a precise mechanism exists → name the mechanism
       - a semicolon that is not truly needed → make two sentences or use a comma
       - AI-voice filler ("plays a crucial role", "it is worth noting", "in today's world") → cut
  2. Re-read the WHOLE unit. Fix:
       - topic sentence present and the paragraph does exactly one job
       - internal order: topic → explanation → detail/evidence → implication
       - redundancy across sentences; kill repeats
       - transitions between sentences read naturally, not mechanically
  3. Apply edits to the .tex (tracked or direct, per Step 0).
  4. Return the change log.
```

### The consolidation waves

After a parent's children are done, spawn one agent (or do it yourself) to re-read the whole
parent:

- **Subsubsection / Subsection re-read:** Do the paragraphs appear in the right order? Are
  transitions between paragraphs smooth? Is terminology identical throughout (same symbol,
  same method name, same acronym)? Is any paragraph now redundant after the leaf edits? Does
  any dense paragraph now clearly want to be a figure, table, or supplement item? Leave a
  marker (see below), do not fabricate the figure.
- **Section re-read:** Does the section deliver the role its type promises (see
  `references/paper-structure.md`)? Are there gaps or overlaps with adjacent sections? Do
  forward/back references (`as shown in Section~\ref{...}`) still hold after edits?

### Marking figure / table / supplement candidates (never fabricate)

When a paragraph is really a diagram, a table, or belongs in a supplement, do **not** invent
data or draw a fake figure. Leave a clearly tagged marker so the author can act, and — where
useful — draft the caption or a table skeleton from text that already exists:

```latex
% [FIGURE CANDIDATE | R2] This paragraph describes a multi-stage pipeline (encode → channel
% → decode → predict → act). Convert to a workflow figure; suggested caption drafted below.
% [TABLE CANDIDATE | R2] Six parameters listed in prose (arrival rate, queue size, ...) —
% move to a parameter table for readability.
% [MOVE TO SUPPLEMENT | R5] This derivation is useful but interrupts the main flow.
```

The full decision rules ("when is a paragraph really a figure?") are in
`references/figures-tables-supplement.md`. Read it before the section-level consolidation.

---

## Step 2 — Whole-manuscript consolidation

After every section is polished and consolidated, read the entire manuscript once more as a
single artifact. This is where cross-section problems surface. Run a light five-perspective
check (the same panel used in deep review — defined in `references/review-panel.md`):

- **Technical correctness:** notation consistent everywhere; assumptions stated before use;
  every symbol defined once; no term silently reused for two things.
- **Structure and story:** the abstract matches what the paper actually does; the
  introduction's contribution bullets match the conclusion; each section still earns its place.
- **Writing:** consistent voice and terminology; no leftover AI-filler; semicolons justified;
  no paragraph doing two jobs.
- **Adversarial novelty:** is any contribution claim larger than the evidence? Flag, soften,
  or point to where the evidence lives — do not inflate.
- **Adversarial evidence / reproducibility:** is every figure and table referenced and
  explained in the text? Do conclusions follow from the results shown? Are baselines,
  metrics, and parameters stated well enough to reproduce?

Then run the **bibliography pass** — this is easy to forget and reviewers notice. Follow
`references/bibliography.md`: verify every `\cite` key exists, remove duplicates, protect
Title Case with outer braces where the style would otherwise lowercase it, protect acronyms,
and disable repeated-author dashes (`IEEEtranBSTCTL` + `\bstctlcite`, or biblatex
`dashed=false`).

Fix what is safe. For anything that needs the author (a claim that may be too strong, a
missing citation, a figure that should exist but does not), leave a tagged comment and list
it in the final report.

---

## Step 3 — Check and commit

1. **Build if you can.** If LaTeX tooling exists, compile to catch syntax errors your edits
   introduced:
   ```bash
   latexmk -pdf main.tex      # or the project's build command
   ```
   Do not ship a change that breaks the build. If you cannot compile in this environment,
   say so in the report and at minimum sanity-check brace/`$`/environment balance around
   your edits.

2. **Review the diff.** `git status` and `git diff --stat`, then read the actual diff of a
   few units to make sure edits are surgical and no math moved.

3. **Commit.** In Polish mode, one clear commit is fine (or a few, grouped by section):
   ```bash
   git add -A
   git commit -m "polish: tighten wording and flow across the manuscript"
   ```
   In Deep-review mode, commit **each pass separately** with the messages listed in
   `references/review-panel.md`. Never collapse ten passes into one commit. Do not commit
   build artifacts (`*.aux`, `*.pdf`, ...) unless the repo already tracks them.

---

## Final report (always produce this)

Close every run with a short, honest summary so the author knows what happened:

```
# Manuscript Polish — Summary

## Mode
Polish | Deep review (N passes)

## What changed
- <section>: <one line on the kind of edits, e.g. "split 4 long sentences, removed 3 overclaims">
- ...

## Left for your judgment (I did NOT change these)
- <claim / notation / missing evidence>, at <file:line> — why it needs you

## Citation-needed
- <statement at file:line> — appears to need a reference

## Figure / table / supplement candidates
- <file:line> — <figure|table|supplement> — <one line why>

## Bibliography
- .bib file edited: <path> | Style: BibTeX+IEEEtran | biblatex
- Titles wrapped for Title Case: <n> | Acronyms protected: <list> | Repeated-author dashes: disabled? yes/no
- Still-risky entries: <list or none>

## Build / commits
- Compilation: passed | failed (<error>) | not attempted (<why>)
- Commits: <hash> <message> ...
```

Do not claim the manuscript is "submission-ready" unless every critical and major issue is
either fixed or explicitly listed under "Left for your judgment". Honesty about what remains
is more useful to the author than a confident all-clear.

---

## Reference files (read them when the step says to)

- `references/writing-style.md` — the academic-English style contract, with good/bad
  examples. Read before Step 1; hand it to every editing agent.
- `references/paper-structure.md` — section conventions and the role of each section. Read
  before section-level consolidation.
- `references/figures-tables-supplement.md` — when prose should become a figure, table, or
  supplement, and how to mark it. Read before Step 1's consolidation waves.
- `references/bibliography.md` — `.bib` title casing, repeated-author dashes, citation
  integrity, and the required bibliography report. Read during Step 2.
- `references/review-panel.md` — the full 10-pass, 5-reviewer deep-review playbook. Read
  when running Deep-review mode.
- `scripts/README.md` — what `outline.py`, `style_lint.py`, and `bib_check.py` do and how to
  read their output.
