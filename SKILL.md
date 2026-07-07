---
name: manuscript-polish
description: >-
  Use this skill for any request to revise, edit, proofread, or clean up an academic paper,
  manuscript, thesis, or draft the user already has — the whole document or just one part
  (abstract, intro, related work, a single .tex file). This is the default tool for that work,
  even when the task sounds simple or the user never says "polish". Typical intents: tighten
  wordy or ChatGPT-sounding prose, fix run-on sentences and stray semicolons, reduce
  overclaiming, smooth flow, reorder or restructure sections, flag which dense paragraphs
  should become figures/tables, repair a .bib (lowercased titles, repeated-author dashes,
  missing/duplicate citations), or run a deep journal-level/adversarial review before
  submitting (IEEE IoT-J, TNSE, JSAC, APCC…). Handles LaTeX/.tex, Markdown, or Word. Do NOT
  use to write brand-new content from scratch, translate, build slides, review code, edit
  non-paper text like emails, or draft rebuttal/cover letters.
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

The **title, the abstract, and every figure/table caption are units too**, not just the body
sections. Give the abstract its own dedicated leaf pass — it is read first by every reviewer
and is usually the worst offender for overclaiming and stacked-clause sentences. Captions get
the same sentence-level care as prose.

The abstract also has hard hygiene rules, because it must stand alone: **no equations or inline
math, no citations, no cross-references (`\ref`/"Fig. 1"/"Section II"), and no undefined
acronyms.** Flag any violation (do not silently delete — see non-negotiable #1) and propose a
plain-words rephrasing. The full rules are in `references/paper-structure.md`, and
`scripts/style_lint.py` reports them mechanically as `abstract-math`, `abstract-citation`, and
`abstract-crossref` so nothing slips through.

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
   number, label, `\ref`, `\cite`, and unit exactly. Do not "fix" a formula unless it is a
   clear LaTeX **syntax** error or the user explicitly asked for a math correction. When a
   claim is a problem, which kind decides what you do — this precedence resolves the common
   "should I reword or flag?" tension:
   - *Overclaimed but supported* (a real result described too grandly) → size it down to what
     the paper actually shows (`references/writing-style.md` §3). Safe, do it.
   - *Unsupported by anything in the paper* (no result, no proof, no citation to size against)
     → do **not** invent a smaller "result" to replace it. Downgrade it to honest intent
     ("we aim to reduce…", "the method is designed to…") **and** flag it, or just flag it.
     Never manufacture a claim the paper cannot back. This case is common when the draft has
     no evaluation yet.
   - *Prose that contradicts an unambiguous equation or definition* (e.g., calling a
     probability "a number of…") → flag it, do not silently rewrite. Rewriting guesses which
     side is wrong and can quietly change the meaning.
   Use the flag convention in "Marking flags and candidates" (Step 1) for all of these.

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
   - **Record the baseline** so the author can diff later: `git tag baseline` (or note the
     pre-edit commit hash) and report it. Heads-up: right after you branch, `git diff` shows
     nothing until you make an edit — that is expected, not a lost-changes bug. Use
     `git diff baseline` to see the whole polish.

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
       - long/comma-heavy sentence (>~30 words, stacked "which/thereby/thus/moreover") → shorten.
         Exception: if it is a list/notation/parameter dump, do not shorten — mark it a table
         candidate and leave the content intact (splitting it just scatters the definitions).
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

### Marking flags and candidates (never fabricate)

When something needs the author's judgment, or a paragraph is really a figure/table/supplement
item, leave a tagged marker instead of guessing or fabricating. In clean/Polish mode the marker
is a LaTeX comment; in tracked mode it is `\comment[id=CR]{...}` with the same tag text. Use
this standard tag vocabulary so markers are easy to grep and the final report can collect them:

```latex
% [CHECK] A claim, notation, or text-vs-equation issue the author must resolve.
% [CITATION NEEDED] A statement that appears to need a reference.
% [FIGURE CANDIDATE] What kind of figure and why; draft a caption below if useful.
% [TABLE CANDIDATE] What the rows/columns would be; draft a skeleton if useful.
% [MOVE TO SUPPLEMENT] Why this detail interrupts the main flow.
```

In **deep review** add the reviewer id, e.g. `% [CHECK | R1]` or `% [FIGURE CANDIDATE | R2]`,
so a marker traces back to the persona that raised it. In **Polish mode** the id is optional —
plain `% [CHECK]` is fine.

For figure/table/supplement candidates, do **not** invent data or draw a fake figure. Mark the
candidate and, where useful, draft the caption or table skeleton from text that already exists.
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
