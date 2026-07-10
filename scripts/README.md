# Helper scripts

Three standard-library Python scripts (no dependencies) that support the workflow. They are
**pre-scans and planners, never judges**. Run them to focus attention and divide work, then
read every sentence yourself. None of them edit the manuscript.

Run from the skill directory, passing either the main `.tex` or the project directory.

## `outline.py` — structure tree + traversal plan
```bash
python scripts/outline.py path/to/main.tex
python scripts/outline.py path/to/project_dir
```
Finds the main file, follows `\input`/`\include`, and prints the section/subsection/
subsubsection tree with `file:line`, approximate word and paragraph counts, and a numbered
bottom-up traversal plan (which leaf units to polish first). Use it to assign spans to agents.

## `style_lint.py` — academic-style flashlight
```bash
python scripts/style_lint.py path/to/main.tex
python scripts/style_lint.py path/to/main.tex --only overclaim,semicolon
```
Flags likely problems as `file:line: [category] detail`, across several groups:
- **prose:** `overclaim`, `ai-voice`, `weasel`, `transition`, `semicolon`, `long-sentence`,
  `comma-heavy`
- **abstract:** `abstract-math`, `abstract-citation`, `abstract-crossref`
- **floats/math:** `long-caption`, `figure-nowidth`, `crowded-figure`, `long-equation`
- **structure/redundancy:** `misplaced-future-work`, `repeated-sentence`, `dup-caveat`,
  `note-header`, `list-abuse`, `subsection-count`
- **hygiene:** `unicode-dash`, `acronym-first-use`, `caption-restates-body`

Run the full docstring (`python scripts/style_lint.py` with no args) for the one-line meaning of
each. Filter with `--only cat1,cat2`. It skips comments and math. Every hit is a *candidate* —
confirm by reading. Feed the hits for a given span to the agent working that span so it starts
with the known suspects.

## `bib_check.py` — citation integrity + .bib risks
```bash
python scripts/bib_check.py path/to/project_dir
```
Reports cited-but-missing keys, uncited entries, duplicate keys, titles lacking outer-brace
Title-Case protection, the bibliography system (BibTeX+bst vs biblatex), and whether
repeated-author dashes are disabled. Use it during the bibliography pass; see
`../references/bibliography.md` for the fixes.

All three are best-effort and regex-based. On unusual LaTeX they may miss or over-report — they
save time, they do not replace reading.
