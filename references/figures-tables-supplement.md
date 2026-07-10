# When Prose Should Become a Figure, Table, or Supplement

Read this before the section-level consolidation waves. Dense prose that describes a
structure, a process, or a long list is usually easier to *show* than to *read*. Your job is
to **spot these paragraphs and mark them** — not to fabricate figures or invent data. Where it
helps, draft a caption or a table skeleton from text that already exists, so the author has a
starting point.

Marking convention (a `.tex` comment in Polish mode, or `\comment[id=CR]{...}` in tracked mode
— same tags as `SKILL.md` "Marking flags and candidates"):

```latex
% [FIGURE CANDIDATE] <one line: what kind of figure and why>
% [TABLE CANDIDATE] <one line: what the columns/rows would be>
% [ALGORITHM CANDIDATE] <one line: which procedure to formalize>
% [MOVE TO SUPPLEMENT] <one line: why it interrupts the main flow>
```

The reviewer id (`| R2`, `| R5`, ...) is only for **deep review**, where a marker should trace
back to the persona that raised it. In Polish mode omit it.

---

## Convert to a FIGURE when the paragraph has one of these signals

### Signal 1 — Multiple components that interact
A paragraph naming several blocks and how data/control flows between them is an architecture
diagram in disguise.

> The system consists of an input module, a feature extractor, a scheduler, a controller, and
> an output module. The input module forwards processed features to the scheduler. The
> scheduler selects an action based on the controller state, while the controller updates its
> policy using feedback from the output module.

→ **System architecture figure.** In the text keep only:
> Fig. X shows the overall architecture. Data flow proceeds from sensing to scheduling, and
> feedback updates the controller.

### Signal 2 — A multi-step process
"First ... then ... next ... finally ..." is a pipeline figure.

> First, the device observes the environment. Then it encodes the observation into a latent
> representation. The representation is transmitted over a noisy channel. The receiver
> reconstructs the latent state and uses it for prediction. Finally, the prediction selects an
> action.

→ **Pipeline / workflow figure** (Observation → Encoder → Channel → Decoder → Prediction →
Action). Text shrinks to: "Fig. X summarizes the end-to-end pipeline."

### Signal 3 — Branching logic / cases
"If ... otherwise ..." across several conditions is a flowchart or decision tree.

> If the channel is good, the device sends a high-rate representation. If moderate, it sends a
> compressed one. If poor, it delays or sends only essential information.

→ **Decision flowchart.** Text: "The transmission mode is selected according to channel
quality, as shown in Fig. X."

### Signal 4 — A taxonomy of methods
"Methods divide into A, B, and C ..." is a taxonomy figure (or a comparison table — see below).

### Signal 6 — A hard-to-picture system model
If the reader must mentally assemble a network of nodes/servers/users from prose, give them a
**system model figure**. Reviewers strongly prefer to see the system in one glance.

---

## Convert to a TABLE when the paragraph packs one of these

- Many symbols → **notation table**.
- Many parameters → **parameter/settings table**.
- Many baselines, metrics, categories, or comparisons → **comparison table**.
- Repeated "compared with / unlike / advantage / limitation" language → **comparison table**.

Example — a notation dump in prose:

> We denote the number of users by N, channels by M, arrival rate by lambda, service rate by
> mu, queue length by Q_t, and control action by a_t.

→ **Notation table** with columns `Symbol | Meaning`. Text: "Table X summarizes the notation."

Example — a parameter dump:

> The model considers user density, arrival rate, channel condition, queue size, resource
> capacity, and control interval.

→ **Parameter table.** You may draft the skeleton (rows = the six parameters, columns =
`Parameter | Symbol | Value`) and leave the values for the author.

---

## Move to the SUPPLEMENT when the paragraph is

- A long proof or an auxiliary derivation.
- An additional ablation or a parameter-sensitivity sweep that is not a main result.
- Deep implementation detail.
- Extra results that "show similar trends and are omitted for space".

Example:

> We also evaluate the method under additional arrival rates, queue sizes, channel conditions,
> and model sizes. These results show similar trends and are omitted due to space.

→ Main text: "Additional sensitivity results are provided in the supplementary material."
Mark the detail `[MOVE TO SUPPLEMENT]`; do not delete it.

Typical supplement sections: additional derivations/proofs, extended setup, baseline details,
hyperparameters, additional results, more ablations, complexity/runtime, reproducibility
checklist.

---

## Fast keyword heuristics (from the pre-scan)

`style_lint.py` flags these, but you confirm by reading:

- Many of: *consists of, includes, forwards, interacts with, feedback, pipeline, stage,
  module, component, first, then, finally, if, otherwise* → likely a **figure**.
- Many of: *compared with, unlike, category, type, method, limitation, advantage, baseline*
  → likely a **table**.
- Many of: *detailed proof, additional result, sensitivity, implementation detail, omitted
  for space* → likely a **supplement** item.

A practical rule: **a paragraph carrying three or more parallel list-like items is usually a
table or a figure.**

---

## Worked example: text → figure + drafted caption

**Original prose:**
> The proposed method consists of three stages. In the first stage, raw observations are
> collected and converted into state features. In the second stage, the controller evaluates
> candidate decisions based on the current state, predicted future condition, and system
> constraints. In the third stage, the selected decision is applied, and the resulting
> feedback updates the controller. This process repeats periodically.

**Rewritten main text (short, points to the figure):**
> Fig. X shows the three-stage control pipeline. The system first converts raw observations
> into state features. The controller then evaluates candidate decisions under system
> constraints. The selected decision is applied, and the resulting feedback is used in the next
> control period.

**Drafted caption (for the author to pair with a real figure):**
> Fig. X. Three-stage control pipeline. Raw observations are converted into state features,
> candidate decisions are evaluated under system constraints, and feedback from the applied
> decision is used in the next control period.

Note what did **not** happen: no numbers were invented, no figure was drawn, no claim changed.
You extracted the structure that was already in the prose and handed the author a clean
starting point.

---

## Figure quality and layout

A figure earns its space only if the reader understands it at a glance, on paper, without
zooming. Apply this checklist and the layout rule to every figure.

### One figure, one message
Each figure answers one clear question ("does the certified bound predict the collapse region as
storm size grows?"). A figure trying to answer several questions at once becomes unreadable —
split it.

### Readable at 100% (print and on-screen PDF)
A beautiful figure with tiny text is a broken figure. Minimum bar: axis labels, tick labels, and
legend all readable without zooming; lines thick enough and markers large enough to tell apart;
a self-contained caption. For IEEE two-column, text *inside* the figure should end up roughly
8–10 pt after placement. If the in-figure text renders much smaller than the caption, the figure
was scaled down too hard — enlarge or simplify the source, do not just shrink it to fit.

### No long title inside the plot
Drop the in-plot title, or keep it very short, and put the detail in the caption. Do not bake
`Certified operating curve at fixed per-cell C_RAR (pool R*M=2048)` into the plot — it crowds
the axes. Keep only something like `R_pass vs. Q_k`, or nothing if the caption already says it.

### Caption: self-contained but not overloaded
Say what the figure tests, the main condition, what the curves/markers mean, and the single
insight. Do not repack formulas already in the text. (Length and placement rules are in
"Captions and fit" below.)

### Visual encoding survives grayscale
Distinguish curves by line style **and** marker shape **and** label — not by color alone. Many
reviewers print in grayscale, where color-only encoding collapses into identical grey lines.

### Layout: never crowd plots side-by-side in one column
An IEEE column is ~3.5 in wide. Two subfigures placed side-by-side in one column
(`0.48\columnwidth` each ≈ 1.7 in) are almost always too small for a technical plot with axes, a
legend, or a log scale. Decide with this rule:

- **Two or more plots with x/y axes → default to `figure*`** (spans both columns; each panel
  gets close to a full column and stays readable). Best when both panels matter and the reader
  compares them side by side.
- **Want to stay in one column → stack the panels vertically, not horizontally.** Taller figure,
  but each panel keeps full-column width and stays readable.
- **Each panel is an independent result → split into two separate figures.** Cleanest when each
  caption is long or each plot carries its own insight.
- **Forced to keep two panels in one column → simplify hard:** drop in-plot titles, use one
  shared legend outside the plots, fewer ticks, thicker lines, bigger markers, shorter axis
  labels, and move detail like "(3000 seeds)" into the caption.

Side-by-side-in-one-column is acceptable only for *simple* figures — a small diagram, a
qualitative image, or a plot with very little text. For axis/legend/log-scale plots, do not do
it. `scripts/style_lint.py` flags two or more narrow panels packed into a single-column `figure`
as `crowded-figure`; the fix is `figure*` or a vertical stack.

Minimal `figure*` skeleton for two axis plots:

```latex
\begin{figure*}[t]
  \centering
  \begin{subfigure}{0.48\textwidth}
    \includegraphics[width=\linewidth]{fig_a.pdf}
    \caption{Residual-backlog validation.}\label{fig:a}
  \end{subfigure}\hfill
  \begin{subfigure}{0.48\textwidth}
    \includegraphics[width=\linewidth]{fig_b.pdf}
    \caption{Reliability lower-bound validation.}\label{fig:b}
  \end{subfigure}
  \caption{In-window rebuild-term validation under Poisson arrivals.}\label{fig:val}
\end{figure*}
```

## Captions and fit (length, placement, no overflow)

Once a figure or table exists, two things go wrong most often: the caption is either useless or
a paragraph long, and the float overflows the column or the page. Both are easy to catch.

### Caption length and quality
A caption should be **just enough** — say what the reader is looking at and the single takeaway,
then stop. Not a bare label, not a re-derivation of the method.

- **Too short (a label):** "Fig. 3. Results." → the reader learns nothing.
- **Too long (a paragraph):** a caption that re-explains the whole setup and every curve
  belongs partly in the body, not the caption.
- **Right:** "Fig. 3. Access success probability versus offered load. The proposed method keeps
  more RAR capacity for real devices than the collision-only baseline." One or two sentences,
  self-contained enough to grasp the figure without hunting through the text.
- **Placement convention:** a **table** caption goes *above* the table; a **figure** caption
  goes *below* the figure (IEEE/most venues). `style_lint.py` flags captions over ~40 words as
  `long-caption` — shorten or move the excess into the text.

### The float must fit — no overflow into the next column or off the page
A figure or table that spills past the column edge (very common in two-column IEEE formats) is
an instant reviewer complaint. The reliable detector is the build log: `grep "Overfull" *.log`.
Fixes, in order of preference:

- **Wide content → full-width float.** Use the starred environments `figure*` / `table*`, which
  span both columns, instead of forcing wide content into one column.
- **Size the graphic to the column.** `\includegraphics[width=\columnwidth]{...}` (or
  `\linewidth`). Never include a graphic with no size option — at natural size it usually
  overflows. `style_lint.py` flags this as `figure-nowidth`.
- **Shrink a wide table.** Drop the table body to `\small` or `\footnotesize`, abbreviate
  column headers, or wrap it in `\resizebox{\columnwidth}{!}{...}` (use resizebox sparingly —
  it also scales the font, which can become tiny).
- **Do not** fix overflow by deleting columns or data. Compress the presentation, not the
  content — and if a table is genuinely too big, move the full version to the supplement and
  keep a reduced version in the main text.

Leave a marker when you spot a likely-overflowing float but cannot compile to confirm:

```latex
% [CHECK] Wide table in a two-column layout — likely overflows the column. Use table* or \small.
% [CHECK] \includegraphics has no width — set width=\columnwidth to avoid overflow.
```

## Senior figure/table standards (S4)

These come from the senior-review standard **S4** (origin:
`senior-paper-review/references/review-history.md`) and add to "Figure quality" and "Captions and
fit" above.

### Inspect the rendered PDF — mandatory for the float pass
The `.log` catches overfull boxes; it does **not** catch a label sitting on a box border, an arrow
overlapping a curve, or an inset colliding with the main axis. So for the figure/table pass you
must **look at the rendered PDF**: read the PDF pages visually, and zoom-crop dense figures to
pixel level. (Origin: the first senior run found a Figure 1 arrow-label overlapping the box border
only by pixel-zoom of the rendered PDF — grepping the log would never have caught it.)

### Zoom-inset placement (three rules)
A magnified inset helps only if placed right. Three consecutive senior corrections on one figure
produced these:
1. **Zoom where the curves diverge**, not an arbitrary region — the inset exists to show the
   difference that matters.
2. **The inset must not overlap the main curves.** Make headroom (shrink it, or move it to an
   empty corner) so it covers no data.
3. **Inset ticks must not collide with the main-axis ticks.** Offset or thin the inset ticks.

### Diagram hygiene
- **Zero overlaps**, verified on the rendered PDF at pixel zoom — no box-on-box, label-on-border,
  or arrow-on-curve.
- A panel `fit=` box (TikZ) must **enclose every annotation it visually claims** — a label that
  belongs to a panel sits inside that panel's box.
- **Legends must not wrap an orphan item** onto a line by itself; resize or re-order the legend.

### Plot → table conversion (when the difference is invisible)
If a plot's curves are visually indistinguishable, convert it to a table (this also saves space —
see the compression order in `references/supplement-merge.md`). The recipe:
- **Bold the best value in each row.** If several tie at the printed precision, bold **all** of
  them — never bold one arbitrarily.
- **State the % improvement once** — in the caption **or** the body, never both (repeating it is a
  duplicate; see writing-style §12).
- **Define every column abbreviation** (e.g., "GT" = ground truth) in the caption or a note.

### Captions (senior tightening)
In addition to the length/placement rules in "Captions and fit":
- **1–2 sentences.** Longer means the caption is re-explaining the body.
- **No internal artifact paths** — a camera-ready caption never contains `e02/REPORT.md`-style
  build paths or run IDs.
- **Do not restate the body's interpretation sentence** in the caption; say what the reader is
  looking at and let the body carry the interpretation once. `scripts/style_lint.py` flags a
  caption sharing an 8-gram with body prose as `caption-restates-body`.

## Guardrails

- Never fabricate data, results, or a figure image. You mark candidates and, at most, draft a
  caption or a table skeleton from text that is already there.
- Do not move a paragraph to the supplement if the main argument depends on it — a supplement
  is for support, not for load-bearing content.
- Leave the actual decision to the author when it affects the paper's message. Your marker plus
  a one-line rationale is enough; the final report lists them all.
