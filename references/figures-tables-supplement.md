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

## Guardrails

- Never fabricate data, results, or a figure image. You mark candidates and, at most, draft a
  caption or a table skeleton from text that is already there.
- Do not move a paragraph to the supplement if the main argument depends on it — a supplement
  is for support, not for load-bearing content.
- Leave the actual decision to the author when it affects the paper's message. Your marker plus
  a one-line rationale is enough; the final report lists them all.
