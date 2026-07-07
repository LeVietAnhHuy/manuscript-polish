# Paper Structure Conventions

Read this before the section-level consolidation. It tells you what role each section is
supposed to play, so you can judge whether a section delivers on its promise or drifts.

Do not force a paper into a template. Section counts vary. But most technical papers have
6–8 main sections, and each has a well-understood job. When a section is not doing its job,
that is a structural finding to raise (and, if safe, to fix by moving material).

---

## Common layouts

**Safe 6-section form (very common, empirical/systems papers):**

```latex
\section{Introduction}
\section{Related Work}
\section{System Model and Problem Formulation}
\section{Proposed Method}
\section{Performance Evaluation}
\section{Conclusion}
```

**7–8 section empirical form:**

```latex
\section{Introduction}
\section{Related Work}
\section{System Model / Problem Formulation}
\section{Proposed Method}
\section{Experimental Setup / Evaluation Setup}
\section{Results and Discussion}
\section{Conclusion}
```

**Theory-leaning form:**

```latex
\section{Introduction}
\section{Related Work}
\section{Preliminaries}
\section{Problem Formulation}
\section{Proposed Method / Analysis}
\section{Theoretical Results}
\section{Numerical Evaluation}
\section{Conclusion}
```

Use `Background / Preliminaries` only when the reader genuinely needs concepts before the main
model. Split `Results and Discussion` out of `Evaluation` when the results need real
interpretation, not just a setup description.

---

## The job of each section (use this to audit)

1. **Introduction** — Why does this problem matter? What is the gap? What does this paper do?
   Should contain: motivation, the specific problem, the research gap left by prior work, the
   main idea, and a clear list of contributions. If the intro does not state the gap and the
   contributions, that is a major finding.

2. **Related Work** — What have others done, and how is this paper different? Not a list of
   summaries. A good Related Work groups prior work logically and *ends at the gap* this paper
   fills. If it reads as an annotated bibliography with no gap, flag it.

3. **Background / Preliminaries** (optional) — The concepts, notation, systems, or theory the
   reader must know before the main model. Include only what is actually used later.

4. **System Model / Problem Formulation** — The "rules of the game": the system under study,
   assumptions, notation, and the precise problem statement. Every symbol used later should be
   defined here or where first introduced. Check text and equations agree.

5. **Proposed Method / Framework / Analysis** — The main contribution: what is proposed and how
   it works. The reader should be able to distinguish it clearly from the baselines. If the
   method is not distinguishable from prior work as written, that is a novelty-positioning
   finding.

6. **Evaluation Setup** — How the claims are tested: dataset/simulator/testbed, baselines,
   metrics, parameters, environment. Enough detail to reproduce. Flag anything missing that a
   reader would need to rerun the study.

7. **Results and Discussion** — What the results say and *why*. Not just "Fig. 6 shows X".
   Interpret trends, trade-offs, limitations, and the insight. Every figure and table must be
   referenced and explained. Conclusions must follow from what is shown, without overclaiming.

8. **Conclusion** — Summarize the problem, contribution, main results, and (optionally)
   limitations and future work. **No new claims or new results here.** If the conclusion
   introduces something not shown earlier, flag it.

---

## Two-tier manuscript: main text vs supplement

A well-organized submission has two layers. Keeping the main text lean is a real quality
signal, not just a page-limit tactic.

- **Main manuscript** — the core story, told directly. Prioritize the figures and tables that
  carry the argument. Every paragraph should earn its place in the narrative.
- **Supplementary material** — supporting detail that would interrupt the main flow: long
  proofs, extended derivations, full hyperparameter tables, additional ablations, extra
  sensitivity sweeps, implementation details, and a reproducibility checklist.

During consolidation, when a main-text paragraph is dense supporting detail rather than part
of the core argument, mark it as a supplement candidate (see
`references/figures-tables-supplement.md`) instead of deleting it.

---

## A reasonable figure/table budget (guidance, not a quota)

Use this to notice what is *missing* or what is *text that should be a visual*, not to demand
a fixed count.

```
Introduction     Fig. 1: motivation / problem illustration
                 Table I: contribution or prior-work comparison (if it helps)
Related Work     Table II: comparison with existing methods (if the literature is dense)
System Model     Fig. 2: system model;  Table III: notation;  Fig. 3: protocol/workflow
Proposed Method  Fig. 4: framework;  Algorithm 1: main algorithm;  Fig. 5: a key module
Evaluation Setup Table IV: parameters;  Table V: baselines and metrics
Results          Fig. 6: main result;  Fig. 7: ablation;  Fig. 8: sensitivity/scalability;
                 Table VI: quantitative comparison
Conclusion       usually no figure
```

If, say, the system model is described only in prose and there is no Fig. 2, that is a strong
figure-candidate finding — reviewers strongly prefer to *see* the system. Conversely, if three
"additional sensitivity" figures crowd the main results, they are supplement candidates.

---

## What a structural finding looks like

When a section does not serve its role, raise it concretely, for example:

- "Related Work lists prior methods but never states the gap this paper fills. Add one closing
  paragraph that names the gap. — structure, major"
- "The Conclusion introduces a new robustness claim not shown in Section VI. Either support it
  in Results or remove it. — structure, major"
- "System Model defines `\lambda` but it is first used two paragraphs earlier in the
  Introduction with a different meaning. Reconcile. — notation, major"

Fix what is safe (reordering paragraphs, moving a sentence, adding a topic sentence). For
anything that changes the argument or needs new content, leave a tagged comment and list it in
the final report for the author.
