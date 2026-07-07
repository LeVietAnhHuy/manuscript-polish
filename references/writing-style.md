# Academic Writing Style Contract

This is the house style for the manuscript-polish workflow. Hand it to every editing agent.
The target is technical academic English that a reviewer understands on the first read and
trusts. Clear beats clever. Precise beats impressive. Modest-but-exact beats grand-but-vague.

The examples below use a running wireless/random-access topic only for illustration. The
rules are topic-agnostic — apply the same thinking to any field.

---

## The short style contract (paste this into an agent brief)

> Write plain, precise academic English. Prefer short sentences and simple words. Use one
> term for one phenomenon and never rename it. State claims no larger than the evidence
> supports — avoid *solve, guarantee, optimal, comprehensive, superior, revolutionary,
> significantly, novel, powerful, seamlessly*. Use a semicolon only when it is truly needed;
> usually two sentences or a comma is better. Give each paragraph one job with a clear topic
> sentence. Cut machine-generated filler. Do not change technical meaning, math, symbols, or
> numbers — flag anything doubtful instead of rewording it into a new claim.

---

## 1. Clear meaning first, decoration never

A good academic sentence is understood on one read. Do not try to sound sophisticated by
stacking clauses. The content is the sophistication.

**Weak (stuffed, self-congratulatory):**
> The proposed comprehensive framework, by leveraging the inherent programmability of O-RAN,
> significantly and effectively mitigates the severe PRACH storm problem in NTN scenarios.

**Better (plain, credible):**
> The proposed framework uses O-RAN control functions to reduce PRACH congestion in NTN
> scenarios.

The second sentence is not decorated, but it is clearer and more believable. Believable is
what gets papers accepted.

---

## 2. Technical precision — one term, one phenomenon

Academic writing must not be vague. Give each distinct phenomenon its own name and use that
name consistently. Reusing one word for several things, or one thing under several words,
both cost the reader.

In a random-access paper, for instance, keep these distinct and never blur them:
`collision`, `false detection`, `ghost demand`, `RAR limitation`, `grant waste`,
`access failure`. Each names a different mechanism.

**Too general (technically loose):**
> PRACH failures occur because many devices collide and the network becomes overloaded.

**Precise (names the mechanism):**
> PRACH failures arise from both real-device contention and false detections that consume
> random access response (RAR) capacity.

The second is more academic because it says *what actually happens*. Whatever the field:
when you can name the mechanism, name it.

---

## 3. Do not overclaim — size the claim to the evidence

Reviewers distrust papers that oversell. Treat the following as red-flag words and only keep
them when the evidence is genuinely overwhelming:

`solve`, `solved`, `guarantee`, `optimal`, `comprehensive`, `superior`, `revolutionary`,
`groundbreaking`, `significantly improve`, `dramatically`, `powerful`, `robustly`,
`seamlessly`, `fully`, `always`, `novel` (as a mere adjective), `state-of-the-art` (unless
you actually compare against it).

**Overclaimed:**
> Our method solves the PRACH storm problem in NTN.

**Sized to evidence:**
> Our method reduces RAR waste caused by false detections under the evaluated PRACH storm
> scenarios.

The second is narrower, and that narrowness is exactly why it is more trustworthy. Bound the
claim to *what was evaluated*. Prefer *reduce/lower/improve* over *solve/eliminate*, and
*can/may* over *will*, unless a proof or a strong result backs the stronger word.

The "sized" example above assumes an evaluation exists to bound the claim to ("under the
evaluated scenarios"). Often a draft has **no results yet**. Do not invent a smaller result
to replace the overclaim — that fabricates evidence. Instead, rewrite the claim as honest
*intent* and flag it: "Our method is designed to reduce RAR waste from false detections" or
"We aim to reduce ...". Intent language is accurate even before results exist, and the
`% [CHECK]` flag reminds the author to state the actual result once they have it. This is the
precedence rule spelled out in `SKILL.md` non-negotiable #1.

---

## 4. Short sentences, clear structure

A common failure is the long sentence full of commas, `which`, `thereby`, `thus`, and
`moreover`. Good technical English rarely needs it. Break one long sentence into two or three
short ones.

**Hard to read (one 45-word sentence):**
> In NTN systems, where LEO satellites provide intermittent and predictable coverage to
> massive IoT devices, a large number of buffered devices may attempt random access almost
> simultaneously, thereby causing severe contention, excessive preamble collisions, increased
> false alarms, and degraded access success probability.

**Easy to read (three sentences):**
> In NTN systems, LEO satellites provide intermittent and predictable coverage to massive IoT
> devices. When coverage becomes available, many buffered devices may attempt random access
> almost simultaneously. This near-synchronous access can increase preamble collisions, false
> detections, and access failures.

Same content, far easier to read. As a rough guide, watch any sentence over ~30 words or with
three or more commas — it is usually two sentences wearing a trench coat.

One exception: a long sentence that is really a *list* — a notation dump ("we denote N by ...,
M by ..., λ by ...") or a parameter enumeration — should not be split into many short
sentences. That just scatters the definitions. Turn it into a table instead and mark it a
table candidate (`references/figures-tables-supplement.md`), leaving the content intact.

---

## 5. One job per paragraph

A strong paragraph does exactly one thing, in this shape:

```
topic sentence  →  explanation  →  technical detail / evidence  →  implication
```

**Good (one job: why NTN PRACH storms differ from terrestrial congestion):**
> PRACH storms in NTN differ from conventional terrestrial random-access congestion. In
> terrestrial networks, access attempts are often spread over time because devices experience
> relatively continuous coverage. In LEO NTN, coverage windows are short and orbitally
> predictable. Buffered IoT devices may therefore initiate access in a near-synchronous manner
> when the satellite becomes visible. This temporal concentration increases the risk of
> collision, false detection, and RAR capacity exhaustion.

If a paragraph is trying to do two jobs, split it. If you cannot write its one-sentence job,
the paragraph has not decided what it is about yet.

---

## 6. Academic, but human-written — kill the AI voice

Machine-generated prose has tells. Reviewers now spot them fast, and they read as low-effort.
Replace generic flourish with a concrete technical statement.

**AI-sounding (says nothing specific):**
> This paper presents a novel, comprehensive, and efficient framework to address the
> challenging problem of random access in modern networks.

**Human, specific (says the actual contribution):**
> This paper models false detections as ghost demand that consumes RAR capacity and displaces
> real devices from the response window.

The target voice is: **clear + technical + restrained + no filler.**

**Good target example:**
> We model each PRACH false detection as ghost demand. Although no device claims the
> corresponding response, the gNB may still allocate a RAR grant to the false detection. This
> grant consumes limited RAR capacity and can prevent real devices from receiving a response.
> The resulting waste is not captured by collision-only random-access models.

**Avoid this voice:**
> We propose a powerful and comprehensive O-RAN-enabled framework that effectively resolves
> the critical PRACH storm issue by intelligently mitigating false alarms and improving access
> performance in massive NTN IoT environments.

### AI-voice phrases to cut on sight

These add length and no information. Delete or replace with something concrete:

- "plays a (crucial/vital/pivotal/key) role", "it is worth noting that", "it is important to
  note", "as we all know", "in today's world", "in the modern era", "the advent of"
- "delve into", "shed light on", "pave the way", "a myriad of", "a plethora of", "vast
  array", "realm of", "landscape of", "navigate the challenges"
- "seamlessly", "effortlessly", "robustly", "holistic", "cutting-edge", "game-changing",
  "unlock", "harness the power of", "leverage" (prefer *use*)
- Reflexive "Moreover, / Furthermore, / Additionally, / Thereby, / Thus," at the start of
  every other sentence — keep one when it earns its place, cut the rest.
- Empty openers: "It should be emphasized that ...", "Needless to say, ...".

---

## 7. Semicolons — only when truly needed

Because the manuscript is technical English aimed at clarity, avoid semicolons unless one is
genuinely the best tool. Most semicolons should become either two sentences or a comma.

- Joining two full clauses for effect → usually better as two sentences.
- Separating list items that themselves contain commas → this is a legitimate semicolon; keep
  it.

When you remove a semicolon, make sure the result is still grammatical and the logical link
between the ideas survives (add "because", "and", "so", or a new sentence as needed).

---

## 8. Word-level preferences (simple and exact)

Prefer the simpler word when it is just as exact. Do not "upgrade" vocabulary for its own sake.

| Prefer | Over |
|---|---|
| use | utilize, leverage |
| show | demonstrate, illustrate (unless a figure literally illustrates) |
| because | due to the fact that, owing to the fact that |
| to | in order to |
| about / on | regarding, pertaining to, with respect to |
| we measure | it is measured that |
| method / approach | methodology (unless you mean the study of methods) |
| many / several (exact count if known) | a myriad of, numerous, a plethora of |
| reduce / lower | mitigate (fine occasionally, not every line) |
| help | facilitate |

But do keep the exact technical term when it is the exact term. "Preamble", "handover",
"eigenvalue", "gradient" are not to be simplified. Simplicity applies to the *connective*
prose, not to domain vocabulary.

---

## 9. Small consistency rules that reviewers notice

- Define every acronym once, at first use, then use the acronym: "random access response
  (RAR)". Do not redefine it later.
- Keep one spelling and one hyphenation throughout ("random-access" vs "random access" — pick
  one per part of speech and stick to it).
- Numbers and units: consistent style, non-breaking space before units (`5~\mu s`), consistent
  decimal places in the same table.
- Tense: present for general truths and what the paper does ("we propose", "Fig. 3 shows"),
  past for specific completed experiments ("we ran 1000 trials").
- Reference style: consistent "Fig.~\ref{}", "Table~\ref{}", "Section~\ref{}" with
  non-breaking spaces.
- Equation references: write "(\ref{eq:...})" or, if `amsmath` is loaded, "\eqref{eq:...}".
  Note that `IEEEtran` does not load `amsmath` by default, so prefer "(\ref{...})" unless you
  can confirm `amsmath` is available — do not add `\eqref` and silently break the build.

---

## 10. Space economy — the fewest pages that stay clear

Page limits are real, and a tight paper reads as a confident one. The target is the **shortest
length that is still complete and clear** — not the shortest length, and not padding to look
substantial. Reach it by compression, never by cutting substance.

How to shorten without losing anything:

- **Cut filler, not content.** Every AI-voice phrase (§6), empty opener, and redundant
  restatement is free space. Removing "It is worth noting that" costs the reader nothing.
- **Say it once.** If the intro, the method, and the conclusion each state the same
  contribution in similar words, keep the sharpest and trim the echoes. Repetition across
  sections is the biggest hidden source of length.
- **Prefer the compact construction.** "in order to" → "to"; "due to the fact that" →
  "because"; a five-word wind-up before the verb → start with the subject. §4 and §8 already
  do most of this; here the *motive* is also page count.
- **Move detail out, do not delete it.** A dense derivation, a parameter list, or an extra
  ablation belongs in a figure, a table, or the supplement — not deleted (non-negotiable #2).
  A table often replaces a whole paragraph and is easier to read (see
  `references/figures-tables-supplement.md`).
- **Mind the layout tax.** In a fixed format, a paragraph whose last line holds a single word,
  or a heading stranded at the bottom of a column, wastes a line or more. Tightening that
  paragraph by a few words can reclaim a whole line. Do this only when the wording stays
  natural — never mangle a sentence to save a line.

What space economy is **not**: deleting a needed explanation, dropping a limitation to look
stronger, removing a citation, or shrinking figures until they are unreadable. If cutting
would remove information the reader needs, relocate it instead of deleting it.

## 11. Equations — fit the column, keep the math intact

A long equation that runs past the column edge (an `Overfull \hbox`, common in two-column
formats) is a real defect. Fixing it is a **layout** change, not a math change: breaking a wide
equation across lines, or introducing intermediate symbols, does not alter the mathematics, so
it is allowed under the "never change the math" rule (SKILL.md non-negotiable #1) — **as long as
every symbol, operator, and the meaning are preserved exactly.** Never make an equation fit by
*simplifying the mathematics*; that changes content. If a break might change grouping or meaning
and you are unsure, flag it with `% [CHECK]` instead of guessing.

How to make a wide equation fit, in order of preference:

1. **Break across lines with a multi-line environment.** Use `align`/`split` (align at the
   `=`), `multline` (one long expression: first line flush left, last line flush right), or
   `IEEEeqnarray` (IEEE's recommended tool). Break at a binary operator, and by convention start
   the continuation line with that operator:
   ```latex
   \begin{split}
   P_s ={}& \text{(first part)} \\
        &+ \text{(continuation starts with the operator)}
   \end{split}
   ```
2. **Introduce intermediate notation.** Define the bulky sub-expressions once ("let
   $A = \dots$ and $B = \dots$"), then write the main equation compactly with $A$ and $B$. This
   usually fits *and* reads better — often the best fix, not merely a space fix.
3. **Tighten spacing locally.** `\tfrac` instead of `\frac` in a cramped spot, thin spaces, or
   regrouping — small adjustments that do not touch the math.
4. **Last resort: shrink.** `\resizebox{\columnwidth}{!}{$...$}` scales the whole equation down.
   Avoid it — the math font becomes smaller than the body text and inconsistent between
   equations. Prefer breaking or notation.

Other cases:
- **Inline math that overflows** → move it into a displayed equation.
- **A genuinely full-width equation** in a two-column paper → put it in a two-column-spanning
  float (`\begin{figure*}`/`\begin{table*}`, or an IEEEtran top/bottom strip), not crammed into
  one column.

Detection: the `grep "Overfull" *.log` check after a build (SKILL.md Step 3) is the reliable
signal. `scripts/style_lint.py` also flags a very long single-line display equation as
`long-equation` — a candidate to break; confirm at compile.

## What "fixing" a sentence looks like (worked micro-edits)

- *Overclaim:* "significantly outperforms all existing methods" → "achieves lower RAR waste
  than the evaluated baselines".
- *Vague:* "the network becomes overloaded" → "the RAR window is exhausted before all real
  devices are served".
- *Too long:* one 40-word sentence with three "which" clauses → split at the natural breaks
  into two or three sentences.
- *AI filler:* "It is worth noting that our framework plays a crucial role in mitigating the
  challenges" → "Our framework reduces RAR waste from false detections".
- *Semicolon:* "devices collide; the RAR window fills" → "When devices collide, the RAR window
  fills." or two sentences.

Every one of these keeps the technical meaning identical while making the sentence clearer,
smaller, and more credible. That is the whole job.
