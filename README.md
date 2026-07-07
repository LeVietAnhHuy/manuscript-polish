# manuscript-polish

A portable **agent skill** for polishing an academic paper manuscript to submission quality.
It orchestrates agents to read and fix the paper **bottom-up** — sentence, paragraph,
subsubsection, subsection, section, then the whole manuscript — in plain, precise, honest
academic English. It also audits structure, flags figure/table/supplement candidates, and
repairs the bibliography. An optional 10-pass, 5-reviewer adversarial panel handles deep
journal-level revision.

The skill is model- and host-agnostic: the entry point is `SKILL.md` (Markdown + YAML
frontmatter), and everything else is plain Markdown and dependency-free Python. It is designed
to run under any coding agent that can read a skill file and spawn sub-agents (Claude Code,
and similar). Hosts without sub-agents run the same procedure sequentially.

## What it does

- **Bottom-up read-then-fix traversal** — the fixed work order, however long the paper is.
- **Academic writing style** — short sentences, simple words, one term per phenomenon, no
  overclaiming, minimal semicolons, no AI-sounding filler. Never changes math or claims.
- **Structure audit** — checks each section delivers its role; suggests reordering/moves.
- **Figure / table / supplement candidates** — marks prose that should become a visual, and
  drafts captions/skeletons from existing text (never fabricates data).
- **Bibliography integrity** — citation coverage, Title-Case protection, repeated-author dashes.
- **Deep review mode** — 10 passes, 5 reviewer personas, committed pass by pass.
- **Supplement merge (optional)** — when a supplement file must fit a page limit (e.g. TNSE
  18 pages), merge it into a page-limited manuscript with a compact appendix, in new files.

## Layout

```
manuscript-polish/
├── SKILL.md                              # entry point: the workflow
├── README.md                             # this file
├── references/
│   ├── writing-style.md                  # the academic-English style contract
│   ├── paper-structure.md                # section roles and layout conventions
│   ├── figures-tables-supplement.md      # when prose should become a visual / supplement
│   ├── bibliography.md                   # .bib title casing, dashes, citation integrity
│   ├── review-panel.md                   # the 10-pass, 5-reviewer deep-review playbook
│   └── supplement-merge.md               # optional: merge supplement into a page-limited paper
└── scripts/                              # dependency-free helpers (pre-scan, never edit)
    ├── README.md
    ├── outline.py                        # structure tree + traversal plan
    ├── style_lint.py                     # overclaim / semicolon / long-sentence / AI-voice
    └── bib_check.py                      # citation coverage + .bib risks
```

## Install

Point your coding agent at this folder, or drop it into the agent's skills directory:

- **Claude Code** — copy or symlink into `~/.claude/skills/` (user) or `<project>/.claude/skills/`:
  ```bash
  ln -s "$(pwd)/manuscript-polish" ~/.claude/skills/manuscript-polish
  ```
- **Other agents** — place the folder where the agent discovers skills, or reference `SKILL.md`
  directly. The content is plain Markdown, so it also works as a pasted system/context prompt.

## Use

Ask the agent to polish or review a manuscript, for example:

- "Polish this manuscript in `paper/main.tex` for submission."
- "Do a journal-level adversarial review of my paper and apply the fixes."
- "Tighten the introduction and remove the AI-sounding wording."
- "Clean up the bibliography and check every citation resolves."

The skill triggers on polish/proofread/revise/review requests for papers, manuscripts, `.tex`
drafts, and submissions. It works on a git branch or a working copy and commits as it goes, so
every change is recoverable.

## Safety

It never changes equations, symbols, numbers, or the size of a claim. Anything doubtful is
flagged for the author rather than silently rewritten, and the final report lists exactly what
changed, what was flagged, and what still needs the author's judgment.
