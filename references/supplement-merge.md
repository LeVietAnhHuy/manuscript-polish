# Supplement Merge and Page-Limit Fit (optional)

Use this **only** when the manuscript ships with a separate supplement/supplementary file **and**
there is a page limit to hit — for example, TNSE's 18 pages counting the main text, the appendix,
and the references together. If there is no supplement file, or no page limit, skip this entirely;
it does not apply.

The job: merge the supplement into a single page-limited manuscript with a compact appendix, so
that `main text + appendix + references <= the limit`. The goal is **not** a full-length main
paper plus an extra appendix on top.

---

## 1. Work in new files, never the originals

Do not edit `main.tex` directly at the start. Create new, clearly named versions and leave the
originals untouched so nothing is lost:

```
main.tex, supplement.tex, refs.bib      (originals — keep intact)
    -> tnse_main_18p.tex                 (the new page-limited manuscript)
    -> appendix_merged.tex               (the compressed appendix, \input by the main)
```

Name the new main after the target (venue + page budget) so it is unmistakable. All the editing
happens in these new files.

---

## 2. Classify every supplement piece into four buckets

Read the supplement and sort each part:

| Bucket | What it is | Where it goes |
|---|---|---|
| Needed to understand the paper | a definition, assumption, or step the main argument depends on | **into the main text** |
| Needed to verify but too long | a full proof, a long derivation | **into the appendix (compressed)** |
| Secondary result / secondary ablation | a nice-to-have sweep or extra ablation | **summarize in the main text; may be dropped** from the page-limited version |
| Too deep to matter | fine-grained implementation trivia | **left out** if it does not fit |

Two principles govern the sort, and they are not negotiable:

- **The main paper must read on its own.** A reader who never opens the appendix must still
  understand the problem, the method, and the main results.
- **The appendix only supports; it never carries the contribution.** Never push a **core
  contribution, a main equation, a main result, or a key assumption** into the appendix just to
  save pages. If it is load-bearing, it stays in the main text.

---

## 3. Compress — do not bulk-import the supplement

An 8-page supplement does not become an 8-page appendix. Compress hard; keep only what a reviewer
needs to trust the results. Typical ratios:

- Supplement S1 — long proof, 3 pages → **Appendix A: proof sketch + key steps, ~0.7 page.**
- Supplement S2 — extra parameter table, 1 page → **merge into the Evaluation Setup table, ~0.3 page.**
- Supplement S3 — 6 extra figures → **keep the single most important one, or drop them.**
- Supplement S4 — implementation details, 2 pages → **one paragraph + a small table.**

---

## 4. Merge as a compact appendix (IEEEtran)

For IEEEtran, place the appendix near the end, before the references. For several merged parts,
use `\appendices` with one `\section` per part:

```latex
\appendices

\section{Proofs}
\label{app:proofs}
\input{appendix_merged}

\section{Additional Model Details}
\section{Additional Evaluation Details}

\bibliographystyle{IEEEtran}
\bibliography{refs}
```

For a single short appendix, the simpler form is fine:

```latex
\appendix
\section{Proof of Main Result}
```

Use `\appendices` (plural) when the supplement contributes more than one appendix section; use
`\appendix` (singular) for just one.

---

## 5. The page budget and the compression priority order

Target: `main + appendix + references <= the limit` (e.g., 18 pages). When the draft is over,
compress in **this order** — it removes the least valuable material first and protects the core:

1. **Related Work** — stop narrating one paragraph per paper; group by theme and move the
   comparison into a table.
2. **Captions** — shorten over-long captions; keep the main insight in the text (see
   `figures-tables-supplement.md`).
3. **Figures** — drop secondary figures, merge related ones, or move secondary results out of the
   main paper. (Venues such as TNSE explicitly ask that figures be used sparingly and that
   repetitive patterns or results be omitted — this step matches that guidance.)
4. **Repeated explanations** — explain each mechanism once; delete the echoes (the
   `repeated-sentence` lint helps find them).
5. **Long proofs / derivations** — move a compressed version to the appendix.
6. **Secondary evaluation details** — collapse into a table.
7. **Appendix** — trim it last, to only what a reviewer needs to believe the results.

Stop as soon as the document is within the limit. Do not keep cutting into the core to gain blank
space.

---

## 6. Check the page count

Confirm the fit mechanically rather than guessing. After a build:

```bash
pdfinfo tnse_main_18p.pdf | grep Pages      # total page count
```

If `pdfinfo` is unavailable, the last `[NN]` shipout in the build log or the final page number in
the PDF works too. Report the final page count against the limit in the summary, and list what was
moved to the appendix, what was summarized, and what was dropped, so the author can veto any cut.

---

## 7. Safety recap

- New files only; originals untouched.
- Main paper self-contained; appendix supportive only.
- Never demote core content to the appendix to save space — compress *around* it instead.
- Every drop or move is reported for the author to confirm; when unsure whether something is
  droppable, flag it rather than removing it.
