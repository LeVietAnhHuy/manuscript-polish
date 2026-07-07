# Bibliography and Citation Integrity

Read this during Step 2 (whole-manuscript consolidation), or Pass 9 in deep review. The goal
is that the compiled reference list looks the way the author intends, and that every citation
resolves. Reviewers do read the reference list, and a broken or inconsistent one signals a
rushed submission.

First detect the system, because the fixes differ:

- **BibTeX** — the `.tex` has `\bibliographystyle{IEEEtran}` (or similar) and
  `\bibliography{refs}`.
- **biblatex** — the preamble has `\usepackage[...]{biblatex}` and `\addbibresource{refs.bib}`.

Report which one the project uses.

---

## 1. Title capitalization — protect Title Case with OUTER braces

Some styles, including common IEEE `.bst` files, force article and conference titles to
sentence case. Protecting only the acronyms is **not enough** if the intended output is Title
Case — the style will still lowercase every ordinary word.

If the final PDF must preserve Title Case, wrap the **entire** title in an extra pair of
braces, and still protect acronyms and proper nouns inside.

**Use (Title Case preserved):**
```bibtex
title = {{Analysis of {5G} Random Access for Massive {IoT}}},
```

**Do NOT use when Title Case matters** — this may render as "Analysis of 5G random access for
massive IoT":
```bibtex
title = {Analysis of {5G} Random Access for Massive {IoT}},
```

More examples of the correct outer-brace form:
```bibtex
title = {{Ghost-Aware {PRACH} Storm Modeling in {LEO} {NTN}}},
title = {{{O-RAN}-Enabled Random Access Control for {NTN} {IoT} Networks}},
title = {{Deep Reinforcement Learning for Online Computation Offloading in {MEC} Networks}},
```

Rules:
- Keep acronyms, standards, protocols, datasets, and framework names brace-protected
  (`{5G}`, `{IoT}`, `{PRACH}`, `{O-RAN}`, `{MEC}`).
- Add outer braces to every title whose capitalization must be preserved exactly.
- Do **not** silently convert all titles to sentence case.
- Record every title you wrapped in the final report.

A useful default: if the venue prints titles in Title Case and the style is an IEEE `.bst`,
wrap all titles in outer braces. `scripts/bib_check.py` flags titles that lack the outer wrap.

---

## 2. Repeated-author dashes — keep the full author list

Do not let the style replace a repeated author list with dashes like `——` or `----`. Every
entry should show its complete author list, even when consecutive entries share authors.

**BibTeX with `IEEEtran.bst`:** add this control entry to the `.bib` (once) if it is not
already there:
```bibtex
@IEEEtranBSTCTL{IEEEexample:BSTcontrol,
  CTLdash_repeated_names = "no"
}
```
and cite it once near the top of the document, after `\begin{document}` and before normal
citations:
```latex
\bstctlcite{IEEEexample:BSTcontrol}
```
This control citation configures the style. It must not appear as a normal reference in the
list.

**biblatex:** disable dashes in the package options:
```latex
\usepackage[style=ieee,dashed=false]{biblatex}
```
or add `dashed=false` to the existing `biblatex` options.

Never hand-edit author fields into dashes. Every `.bib` entry keeps its complete `author`
field.

---

## 3. Citation integrity checks

Run `scripts/bib_check.py <project dir>` and then verify by eye:

- Every `\cite{key}` (and `\citep`, `\citet`, `\bstctlcite`) resolves to an entry in the
  `.bib`. List any **cited-but-missing** keys — these become "undefined reference" errors.
- No **duplicate** entry keys in the `.bib`.
- No malformed entries (unbalanced braces, missing commas, missing required fields).
- **Uncited** entries (defined but never cited) — list them; the author decides whether to
  cite or remove.
- Consistent entry style: consistent author formatting, consistent venue abbreviation,
  page ranges with en-dashes (`123--130`), a `doi` where available.

Do **not** insert `changes`-package commands (`\added`, `\deleted`, ...) into `.bib` files.
Edit `.bib` entries directly and document the edits in the report.

---

## 4. Required bibliography report

At the end of the bibliography work, report:

1. Which `.bib` file(s) were edited.
2. Which titles were wrapped in outer braces to preserve Title Case.
3. Which acronyms / proper nouns were brace-protected.
4. Whether repeated-author dashes were disabled, and how (`IEEEtranBSTCTL` + `\bstctlcite`,
   or biblatex `dashed=false`).
5. Whether the project uses BibTeX with `IEEEtran.bst`, another `.bst`, or biblatex.
6. Any entries that still look risky after compilation (e.g., titles you were unsure whether
   to wrap, entries missing a venue or year).

Fold this into the final manuscript report under the "Bibliography" heading.
