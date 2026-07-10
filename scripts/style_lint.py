#!/usr/bin/env python3
"""style_lint.py — heuristic pre-scan for academic-style problems in a LaTeX manuscript.

Standard-library only. This is a flashlight, not a judge: it points at sentences worth a human
look. Every hit must be read and confirmed. It never edits anything.

Usage:
    python style_lint.py path/to/main.tex
    python style_lint.py path/to/project_dir
    python style_lint.py path/to/main.tex --only overclaim,semicolon

Categories:
    overclaim      words that usually oversell (solve, optimal, significantly, ...)
    semicolon      a semicolon in prose (usually better as two sentences or a comma)
    ai-voice       machine-generated filler phrases
    weasel         vague intensifiers (very, extremely, highly, ...)
    transition     sentence-initial Moreover/Furthermore/... (cut if overused)
    long-sentence  a sentence over ~30 words
    comma-heavy    a sentence with 3+ commas
    abstract-math       math/equation inside the abstract (abstracts should be plain prose)
    abstract-citation   a \\cite inside the abstract (most venues forbid references there)
    abstract-crossref   a \\ref/\\eqref inside the abstract (it must stand alone)
    long-caption        a figure/table caption over ~40 words (usually too long)
    figure-nowidth      \\includegraphics with no width/scale (risks overflowing the column)
    crowded-figure      2+ narrow panels side-by-side in a one-column figure (use figure*/stack)
    long-equation       a single display-math line wide enough to overflow the column
    repeated-sentence   a substantial sentence that appears more than once (near-verbatim)
    misplaced-future-work  future-work wording outside a Conclusion/Discussion section
    note-header         a paragraph opening with a bold/italic mini-title (scaffolding)
    dup-caveat          a long phrase repeated across two or more sections
    unicode-dash        a Unicode en/em dash in the source (use ASCII -- / ---)
    subsection-count    number of subsection/subsubsection headings (metric; 0 in letter style)
    acronym-first-use   an acronym first used without a parenthesized expansion
    caption-restates-body  a caption sharing an 8-gram with body prose
    list-abuse          a short-item itemize/enumerate outside the Introduction
"""

import os
import re
import sys

OVERCLAIM = [
    "solve", "solves", "solved", "solving", "guarantee", "guarantees", "guaranteed",
    "optimal", "optimally", "comprehensive", "comprehensively", "superior", "superiority",
    "revolutionary", "groundbreaking", "novel", "powerful", "seamless", "seamlessly",
    "robustly", "dramatically", "drastically", "significantly", "fully", "unprecedented",
    "remarkable", "remarkably", "tremendous", "effortless", "effortlessly", "ultimate",
    "perfectly", "unmatched", "state-of-the-art", "cutting-edge", "best-in-class",
]
AI_PHRASES = [
    r"plays? an? (?:crucial|vital|key|pivotal|important|significant) role",
    r"it is worth noting", r"it is important to note", r"it should be (?:noted|emphasized)",
    r"in today'?s world", r"in the modern era", r"the advent of", r"delve into",
    r"shed(?:s|ding)? light", r"pave(?:s|d)? the way", r"a myriad of", r"a plethora of",
    r"vast array", r"realm of", r"landscape of", r"navigat\w+ the challenges",
    r"harness(?:ing)? the power", r"unlock(?:ing)? the potential", r"game[- ]chang\w+",
    r"holistic", r"first and foremost", r"last but not least", r"needless to say",
    r"as we all know", r"ever[- ]evolving", r"rapidly evolving",
]
WEASEL = ["very", "extremely", "highly", "vastly", "hugely", "tremendously", "incredibly",
          "basically", "actually", "really", "quite", "fairly"]
TRANSITION = ["moreover", "furthermore", "additionally", "besides", "thereby"]
# an abstract must be plain, self-contained prose: no math, no citations, no cross-references
AB_MATH_RE = re.compile(
    r"(?<!\\)\$|(?<!\\)\\\(|(?<!\\)\\\[|"
    r"\\begin\{(?:equation|align|gather|multline|eqnarray|displaymath|math)\*?\}")
AB_CITE_RE = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\b")
AB_REF_RE = re.compile(r"\\(?:eqref|ref|autoref|cref|Cref|pageref)\b")
# figure/table caption length and graphic sizing (overflow risk)
CAPTION_RE = re.compile(r"\\caption\*?\s*(?:\[[^\]]*\])?\s*\{")
INCLUDEGFX_RE = re.compile(r"\\includegraphics\s*(\[[^\]]*\])?\s*\{")
# narrow panels crammed side-by-side in a single-column figure
SUBFIG_RE = re.compile(r"\\begin\{subfigure\}\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}")
GFX_WIDTH_RE = re.compile(r"width\s*=\s*(\d*\.?\d+)\s*\\(?:columnwidth|linewidth|textwidth)")
WIDTH_FACTOR_RE = re.compile(r"(\d*\.?\d+)\s*\\(?:columnwidth|linewidth|textwidth)")
# a single display-math line this wide (macros counted as ~1 glyph) likely overflows a column
MATH_ENVS = {"equation", "align", "gather", "multline", "eqnarray", "displaymath",
             "alignat", "flalign", "ieeeeqnarray"}
MATH_BEGIN_RE = re.compile(r"\\begin\{([A-Za-z]+)\*?\}")
MATH_END_RE = re.compile(r"\\end\{([A-Za-z]+)\*?\}")
EQUATION_GLYPH_LIMIT = 52
# senior-review-derived checks
NOTE_HEADER_RE = re.compile(r"^\s*\\(?:textbf|emph|textit|textsc)\{[^}]{2,40}[.:]\}")
UNICODE_DASH_RE = re.compile("[–—]")
LIST_ENVS = {"itemize", "enumerate", "description"}
ROMAN_RE = re.compile(r"^[IVXLCDM]+$")
# tokens that are all-caps but do not need a first-use expansion (venues, formats, units)
ACRONYM_ALLOW = {
    "IEEE", "ACM", "TNSE", "JSAC", "APCC", "IOT", "PDF", "DOI", "URL", "HTML", "HTTP",
    "HTTPS", "ISBN", "USA", "UK", "EU", "AC", "DC", "GHZ", "MHZ", "KHZ", "HZ", "DB",
    "DBM", "MS", "US", "NS", "KM", "MW", "KW", "OK", "ID", "FAQ",
}
# future-work language belongs in the Conclusion, not the model/method/results
SECTION_TITLE_RE = re.compile(r"\\section\*?\s*\{")
SUBSECTION_TITLE_RE = re.compile(r"\\subsection\*?\s*\{")
ALLOWED_FUTURE = ("conclusion", "concluding", "future", "outlook", "discussion",
                  "summary", "remarks", "closing", "perspective")
FUTURE_RE = re.compile(
    r"future work|future research|future direction|future extension|in the future|"
    r"for future work|as future work|left (?:for|to) future|"
    r"leave (?:it |this |them )?(?:for|to) future", re.IGNORECASE)

SKIP_ENVS = {"equation", "align", "gather", "multline", "eqnarray", "verbatim",
             "lstlisting", "tikzpicture", "algorithmic", "minted"}
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
# structural lines that must not be folded into the running sentence buffer
STRUCT_RE = re.compile(
    r"\\(?:sub)*section\*?\b|"
    r"\\(?:paragraph|subparagraph|title|author|maketitle|begin|end|bibliography|"
    r"bibliographystyle|documentclass|usepackage|appendix|appendices|label|"
    r"bstctlcite|IEEEpeerreviewmaketitle|caption|includegraphics)\b")


def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2]); i += 2; continue
        if c == "%":
            break
        out.append(c); i += 1
    return "".join(out)


def matching_brace(s, i):
    """Index of the brace matching s[i]=='{', or -1 if unbalanced."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    return -1


def braced_title(text, cmd_regex):
    """Return the brace-balanced argument of a command matched by cmd_regex, or None."""
    m = cmd_regex.search(text)
    if not m:
        return None
    b = text.find("{", m.start())
    if b < 0:
        return ""
    e = matching_brace(text, b)
    return text[b + 1:e] if e > 0 else text[b + 1:]


def strip_math(text):
    text = re.sub(r"\$[^$]*\$", " math ", text)
    text = re.sub(r"\\\([^)]*\\\)", " math ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)   # drop command names
    text = re.sub(r"[{}]", " ", text)
    return text


def resolve(path, base):
    for cand in (path, path + ".tex"):
        p = cand if os.path.isabs(cand) else os.path.join(base, cand)
        if os.path.isfile(p):
            return p
    return None


def flatten(main_path, seen=None):
    if seen is None:
        seen = set()
    real = os.path.realpath(main_path)
    if real in seen:
        return []
    seen.add(real)
    base = os.path.dirname(real)
    rows = []
    try:
        with open(main_path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, raw in enumerate(fh, 1):
                text = strip_comment(raw.rstrip("\n"))
                m = INPUT_RE.search(text)
                if m:
                    target = resolve(m.group(1).strip(), base)
                    if target:
                        rows.extend(flatten(target, seen)); continue
                rows.append((main_path, lineno, text))
    except OSError as exc:
        print(f"  (could not read {main_path}: {exc})", file=sys.stderr)
    return rows


def find_main(path):
    if os.path.isfile(path):
        return path
    best = None
    for root, _d, files in os.walk(path):
        for name in files:
            if not name.endswith(".tex"):
                continue
            full = os.path.join(root, name)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    head = fh.read(8000)
            except OSError:
                continue
            if "\\begin{document}" in head or "\\documentclass" in head:
                if best is None or full.count(os.sep) < best.count(os.sep):
                    best = full
    return best


def lint(rows, only):
    hits = []
    env_stack = []
    buf = ""
    buf_line, buf_file = None, None

    def want(cat):
        return not only or cat in only

    def evaluate(sentence, sfile, sline):
        s = sentence.strip()
        if not s or sfile is None:
            return
        wc = len(re.findall(r"[A-Za-z][A-Za-z\-']+", s))
        commas = s.count(",")
        if wc > 30 and want("long-sentence"):
            hits.append((sfile, sline, "long-sentence", f"~{wc} words"))
        if commas >= 3 and want("comma-heavy"):
            hits.append((sfile, sline, "comma-heavy", f"{commas} commas"))

    for fpath, lineno, text in rows:
        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()
        if skipping:
            continue

        prose = strip_math(text)
        low = prose.lower()

        # ---- lexical, line-precise checks (run on every prose/heading line) ----
        if want("overclaim"):
            for w in OVERCLAIM:
                if re.search(r"\b" + re.escape(w) + r"\b", low):
                    hits.append((fpath, lineno, "overclaim", w))
        if want("ai-voice"):
            for pat in AI_PHRASES:
                m = re.search(pat, low)
                if m:
                    hits.append((fpath, lineno, "ai-voice", m.group(0)))
        if want("weasel"):
            for w in WEASEL:
                if re.search(r"\b" + re.escape(w) + r"\b", low):
                    hits.append((fpath, lineno, "weasel", w))
        if want("transition"):
            for w in TRANSITION:
                if re.match(r"\s*" + w + r"\b", low):
                    hits.append((fpath, lineno, "transition", w))
        if want("semicolon"):
            for _ in range(prose.count(";")):
                hits.append((fpath, lineno, "semicolon", ";"))

        # ---- sentence buffering for length/comma checks ----
        # Headings, structural commands, and blank lines end the current sentence and are
        # never folded into it, so line attribution stays close to the real sentence.
        if STRUCT_RE.match(text.strip()) or prose.strip() == "":
            evaluate(buf, buf_file, buf_line)
            buf, buf_line, buf_file = "", None, None
            continue

        if not buf.strip():
            buf_line, buf_file = lineno, fpath
        buf += " " + prose
        while True:
            m = re.search(r"[.!?]\s", buf)
            if not m:
                break
            evaluate(buf[:m.start() + 1], buf_file, buf_line)
            buf = buf[m.end():]
            buf_line, buf_file = lineno, fpath
        if re.search(r"[.!?]\s*$", prose):
            evaluate(buf, buf_file, buf_line)
            buf, buf_line, buf_file = "", None, None
    evaluate(buf, buf_file, buf_line)
    return hits


def lint_abstract(rows, only):
    """Flag math, citations, and cross-references inside the abstract environment.

    An abstract must be plain, self-contained prose. These are high-precision structural
    signals (actual LaTeX math/cite/ref commands), reported so none slip through.
    """
    def want(cat):
        return not only or cat in only

    hits = []
    in_ab = False
    for fpath, lineno, text in rows:
        if "\\begin{abstract}" in text:
            in_ab = True
        if in_ab:
            if want("abstract-math") and AB_MATH_RE.search(text):
                hits.append((fpath, lineno, "abstract-math", "math/equation in abstract"))
            if want("abstract-citation") and AB_CITE_RE.search(text):
                hits.append((fpath, lineno, "abstract-citation", "citation in abstract"))
            if want("abstract-crossref") and AB_REF_RE.search(text):
                hits.append((fpath, lineno, "abstract-crossref", "cross-reference in abstract"))
        if "\\end{abstract}" in text:
            in_ab = False
    return hits


def _join_rows(rows):
    """Join rows into one string plus per-character line/file maps for offset lookup."""
    parts, char_line, char_file = [], [], []
    for fpath, lineno, t in rows:
        piece = t + "\n"
        parts.append(piece)
        char_line.extend([lineno] * len(piece))
        char_file.extend([fpath] * len(piece))
    return "".join(parts), char_line, char_file


def lint_floats(rows, only):
    """Flag over-long captions and graphics with no size (an overflow risk)."""
    def want(cat):
        return not only or cat in only

    if only and not ({"long-caption", "figure-nowidth"} & only):
        return []
    joined, cline, cfile = _join_rows(rows)
    hits = []
    if want("long-caption"):
        for m in CAPTION_RE.finditer(joined):
            brace = m.end() - 1
            end = matching_brace(joined, brace)
            if end < 0:
                continue
            wc = len(re.findall(r"[A-Za-z][A-Za-z\-']+", joined[brace + 1:end]))
            if wc > 40:
                hits.append((cfile[m.start()], cline[m.start()], "long-caption", f"~{wc} words"))
    if want("figure-nowidth"):
        for m in INCLUDEGFX_RE.finditer(joined):
            opt = m.group(1) or ""
            if not re.search(r"width|height|scale", opt):
                hits.append((cfile[m.start()], cline[m.start()], "figure-nowidth",
                             "no width/scale — may overflow"))
    return hits


def lint_figures(rows, only):
    """Flag two or more narrow panels packed side-by-side in a single-column figure.

    A subfigure or graphic sized at <=0.6 column widths is a side-by-side panel; two of them in
    a non-starred figure means each is ~half a ~3.5in column, usually too small for an axis plot.
    Vertical stacks (full-width panels) and figure* (two-column) are not flagged.
    """
    if only and "crowded-figure" not in only:
        return []
    hits = []
    in_fig = is_star = False
    fig_line = fig_file = None
    narrow = 0
    for fpath, lineno, text in rows:
        if "\\begin{figure*}" in text:
            in_fig, is_star, narrow = True, True, 0
            fig_line, fig_file = lineno, fpath
            continue
        if "\\begin{figure}" in text:
            in_fig, is_star, narrow = True, False, 0
            fig_line, fig_file = lineno, fpath
            continue
        if "\\end{figure}" in text or "\\end{figure*}" in text:
            if in_fig and not is_star and narrow >= 2:
                hits.append((fig_file, fig_line, "crowded-figure",
                             f"{narrow} narrow panels side-by-side in a one-column figure"))
            in_fig = is_star = False
            narrow = 0
            continue
        if in_fig and not is_star:
            for m in SUBFIG_RE.finditer(text):
                fm = WIDTH_FACTOR_RE.search(m.group(1))
                if fm and float(fm.group(1)) <= 0.6:
                    narrow += 1
            for m in INCLUDEGFX_RE.finditer(text):
                wm = GFX_WIDTH_RE.search(m.group(1) or "")
                if wm and float(wm.group(1)) <= 0.6:
                    narrow += 1
    return hits


def _norm_math_len(s):
    """Rough rendered width of a math line (heuristic).

    Delimiters/spacing add nothing; wide operators (sum/prod/int, frac, sqrt) count for more;
    every other macro counts as ~one glyph, as does each ordinary symbol.
    """
    s = s.replace("\\\\", " ").replace("&", " ")
    s = re.sub(r"\\(?:left|right|big|Big|bigg|Bigg)[lr]?\b", "", s)
    s = re.sub(r"\\(?:sum|prod|int|oint|iint|iiint|bigcup|bigcap|coprod)\b", "xxx", s)
    s = re.sub(r"\\(?:frac|dfrac|sqrt|binom|overline|underline|hat|widehat|tilde)\b", "xx", s)
    s = re.sub(r"\\[a-zA-Z]+", "x", s)        # any other macro renders as ~one symbol
    s = re.sub(r"[\s{}$^_]", "", s)
    return len(s)


def lint_equations(rows, only):
    """Flag a single display-math line wide enough to overflow the column (a break candidate)."""
    if only and "long-equation" not in only:
        return []
    hits = []
    depth = 0
    for fpath, lineno, text in rows:
        begins = [m.group(1).lower() for m in MATH_BEGIN_RE.finditer(text)]
        ends = [m.group(1).lower() for m in MATH_END_RE.finditer(text)]
        in_math = depth > 0 or any(b in MATH_ENVS for b in begins)
        if in_math:
            residual = re.sub(r"\\(?:begin|end)\{[A-Za-z]+\*?\}", " ", text)
            residual = re.sub(r"\\label\{[^}]*\}", " ", residual)
            n = _norm_math_len(residual)
            if n > EQUATION_GLYPH_LIMIT:
                hits.append((fpath, lineno, "long-equation",
                             f"~{n} glyphs on one math line — may overflow; break it"))
        for b in begins:
            if b in MATH_ENVS:
                depth += 1
        for e in ends:
            if e in MATH_ENVS:
                depth = max(0, depth - 1)
    return hits


def iter_sentences(rows):
    """Yield (sentence, fpath, start_lineno) for prose sentences, skipping math and structure."""
    env_stack = []
    buf = ""
    buf_line = buf_file = None
    for fpath, lineno, text in rows:
        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()
        if skipping:
            continue
        prose = strip_math(text)
        if STRUCT_RE.match(text.strip()) or prose.strip() == "":
            if buf.strip():
                yield buf, buf_file, buf_line
            buf, buf_line, buf_file = "", None, None
            continue
        if not buf.strip():
            buf_line, buf_file = lineno, fpath
        buf += " " + prose
        while True:
            m = re.search(r"[.!?]\s", buf)
            if not m:
                break
            yield buf[:m.start() + 1], buf_file, buf_line
            buf = buf[m.end():]
            buf_line, buf_file = lineno, fpath
        if re.search(r"[.!?]\s*$", prose):
            yield buf, buf_file, buf_line
            buf, buf_line, buf_file = "", None, None
    if buf.strip():
        yield buf, buf_file, buf_line


def lint_repeats(rows, only):
    """Flag a substantial sentence (>=10 words) that near-duplicates another one.

    Uses token-set Jaccard similarity (>=0.8), so a claim restated with small wording changes
    ("we propose" vs "we proposed …") is caught, not only verbatim copies.
    """
    if only and "repeated-sentence" not in only:
        return []
    sents = []
    for sentence, fpath, lineno in iter_sentences(rows):
        toks = re.sub(r"[^a-z0-9 ]", " ", sentence.lower()).split()
        if len(toks) >= 10:
            sents.append((set(toks), fpath, lineno))
    flagged = [False] * len(sents)
    for i in range(len(sents)):
        for j in range(i + 1, len(sents)):
            a, b = sents[i][0], sents[j][0]
            inter = len(a & b)
            if inter and inter / len(a | b) >= 0.8:
                flagged[i] = flagged[j] = True
    return [(fpath, lineno, "repeated-sentence", "near-duplicate of another sentence")
            for k, (_toks, fpath, lineno) in enumerate(sents) if flagged[k]]


def lint_misplaced(rows, only):
    """Flag future-work language that appears outside a Conclusion/Discussion-type section."""
    if only and "misplaced-future-work" not in only:
        return []
    hits = []
    sec_title = None
    sub_title = None
    started = False
    for fpath, lineno, text in rows:
        if "\\begin{document}" in text:
            started = True
        if not started:
            continue
        if SECTION_TITLE_RE.search(text):
            sec_title = braced_title(text, SECTION_TITLE_RE) or ""
            sub_title = None
            continue
        if SUBSECTION_TITLE_RE.search(text):
            sub_title = braced_title(text, SUBSECTION_TITLE_RE) or ""
            continue
        if sec_title is None:          # still in front matter / abstract
            continue
        titles = (sec_title + " " + (sub_title or "")).lower()
        if any(k in titles for k in ALLOWED_FUTURE):
            continue
        if FUTURE_RE.search(text):
            hits.append((fpath, lineno, "misplaced-future-work",
                         f"future-work language in section '{sec_title[:30]}'"))
    return hits


def lint_note_headers(rows, only):
    """Flag a paragraph that opens with a bold/italic mini-title used as scaffolding (S1)."""
    if only and "note-header" not in only:
        return []
    hits = []
    env_stack = []
    for fpath, lineno, text in rows:
        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()
        if skipping:
            continue
        m = NOTE_HEADER_RE.match(text)
        if m:
            hits.append((fpath, lineno, "note-header", m.group(0).strip()))
    return hits


def lint_unicode_dash(rows, only):
    """Flag a Unicode en/em dash in the source (use ASCII -- / --- instead) (S5)."""
    if only and "unicode-dash" not in only:
        return []
    return [(fpath, lineno, "unicode-dash", "Unicode en/em dash — use ASCII -- / ---")
            for fpath, lineno, text in rows if UNICODE_DASH_RE.search(text)]


def lint_subsection_count(rows, only):
    """Report the number of subsection/subsubsection headings (0 only in flat letter style, S2)."""
    if only and "subsection-count" not in only:
        return []
    n = 0
    first = None
    for fpath, lineno, text in rows:
        for _m in re.finditer(r"\\subsection\*?\b|\\subsubsection\*?\b", text):
            n += 1
            if first is None:
                first = (fpath, lineno)
    if not first:
        return []
    return [(first[0], first[1], "subsection-count",
             f"{n} subsection/subsubsection headings (0 only in flat letter style)")]


def lint_dup_caveat(rows, only):
    """Flag a long phrase (8-gram) repeated across two or more distinct sections (S1/S5)."""
    if only and "dup-caveat" not in only:
        return []
    toks = []
    sec = None                       # None until the first \section: skips title/abstract
    env_stack = []
    for fpath, lineno, text in rows:
        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()
        if SECTION_TITLE_RE.search(text):
            sec = (braced_title(text, SECTION_TITLE_RE) or "").strip().lower() or "(sec)"
            continue
        if skipping or sec is None:  # skip front matter (title, abstract) — paraphrase is normal there
            continue
        for w in re.findall(r"[a-z0-9]+", strip_math(text).lower()):
            toks.append((w, sec, fpath, lineno))
    grams = {}
    n = 8
    for i in range(len(toks) - n + 1):
        window = toks[i:i + n]
        key = " ".join(w for w, _s, _f, _l in window)
        grams.setdefault(key, []).append((window[0][1], window[0][2], window[0][3]))
    hits = []
    seen_loc = set()
    for occ in grams.values():
        if len({s for s, _f, _l in occ}) >= 2:
            for _s, fpath, lineno in occ:
                if (fpath, lineno) not in seen_loc:
                    seen_loc.add((fpath, lineno))
                    hits.append((fpath, lineno, "dup-caveat", "long phrase repeated across sections"))
    return hits


ACRONYM_TOKEN_RE = re.compile(r"(?<![A-Za-z])[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*(?![A-Za-z])")


def lint_acronyms(rows, only):
    """Flag an acronym that is never given a parenthesized expansion anywhere (S3).

    Two passes so that an acronym first seen in the title/abstract but expanded later in the body
    is not flagged; only acronyms with no `(EXPANSION)` / `ACRONYM (…)` anywhere are reported.
    """
    if only and "acronym-first-use" not in only:
        return []
    cleaned = []
    env_stack = []
    started = False
    for fpath, lineno, text in rows:
        if "\\begin{document}" in text:
            started = True
        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()
        if not started or skipping:        # skip the preamble (package/class names) and math
            cleaned.append((fpath, lineno, ""))
            continue
        c = re.sub(r"\\(?:label|ref|eqref|cref|Cref|autoref|pageref|cite[a-zA-Z]*)\s*\{[^}]*\}",
                   " ", text)
        cleaned.append((fpath, lineno, strip_math(c)))

    defined = set()
    for _f, _l, c in cleaned:
        for m in ACRONYM_TOKEN_RE.finditer(c):
            tok = m.group(0)
            if re.search(r"\(\s*" + re.escape(tok) + r"\b", c) or \
               re.search(re.escape(tok) + r"\s*\(", c):
                defined.add(tok)

    hits = []
    seen = set()
    for fpath, lineno, c in cleaned:
        for m in ACRONYM_TOKEN_RE.finditer(c):
            tok = m.group(0)
            if tok in seen:
                continue
            seen.add(tok)
            if (tok in defined or tok in ACRONYM_ALLOW or ROMAN_RE.match(tok)
                    or sum(ch.isalpha() for ch in tok) < 2):
                continue
            hits.append((fpath, lineno, "acronym-first-use",
                         f"{tok}: never expanded (no parenthesized definition)"))
    return hits


def lint_caption_restates(rows, only):
    """Flag a caption that shares an 8-gram with body prose (restating the interpretation) (S4)."""
    if only and "caption-restates-body" not in only:
        return []
    joined, cline, cfile = _join_rows(rows)
    caps, spans = [], []
    for m in CAPTION_RE.finditer(joined):
        b = m.end() - 1
        e = matching_brace(joined, b)
        if e < 0:
            continue
        caps.append((joined[b + 1:e], cfile[m.start()], cline[m.start()]))
        spans.append((b, e + 1))
    body = list(joined)
    for s, e in spans:
        for i in range(s, min(e, len(body))):
            body[i] = " "
    body_tokens = re.findall(r"[a-z0-9]+", strip_math("".join(body)).lower())
    body_grams = {" ".join(body_tokens[i:i + 8]) for i in range(len(body_tokens) - 7)}
    hits = []
    for text, fpath, lineno in caps:
        toks = re.findall(r"[a-z0-9]+", strip_math(text).lower())
        if any(" ".join(toks[i:i + 8]) in body_grams for i in range(len(toks) - 7)):
            hits.append((fpath, lineno, "caption-restates-body", "shares an 8-gram with body prose"))
    return hits


def lint_lists(rows, only):
    """Flag a short-item itemize/enumerate outside the Introduction (definitional bullets) (S1)."""
    if only and "list-abuse" not in only:
        return []
    hits = []
    sec_intro = False
    stack = []
    for fpath, lineno, text in rows:
        if SECTION_TITLE_RE.search(text):
            sec_intro = "introduction" in (braced_title(text, SECTION_TITLE_RE) or "").lower()
        for m in BEGIN_RE.finditer(text):
            if m.group(1) in LIST_ENVS:
                stack.append({"line": lineno, "file": fpath, "intro": sec_intro,
                              "items": [], "cur": 0, "started": False})
        if stack:
            top = stack[-1]
            cleaned = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", text)
            for idx, part in enumerate(re.split(r"\\item\b", cleaned)):
                if idx > 0:
                    if top["started"]:
                        top["items"].append(top["cur"])
                    top["cur"], top["started"] = 0, True
                if top["started"]:
                    top["cur"] += len(re.findall(r"[A-Za-z][A-Za-z\-']+", strip_math(part)))
        for m in END_RE.finditer(text):
            if m.group(1) in LIST_ENVS and stack:
                top = stack.pop()
                if top["started"]:
                    top["items"].append(top["cur"])
                items = top["items"]
                if len(items) >= 2 and not top["intro"]:
                    avg = sum(items) / len(items)
                    if avg < 15:
                        hits.append((top["file"], top["line"], "list-abuse",
                                     f"{len(items)} items, avg ~{avg:.0f} words — consider prose"))
    return hits


def parse_args(argv):
    positional, only = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--only="):
            only = {x.strip() for x in a.split("=", 1)[1].split(",") if x.strip()}
        elif a == "--only":
            i += 1
            if i < len(argv):
                only = {x.strip() for x in argv[i].split(",") if x.strip()}
        elif a.startswith("--"):
            pass
        else:
            positional.append(a)
        i += 1
    return positional, only


def main():
    positional, only = parse_args(sys.argv[1:])
    if not positional:
        print(__doc__); sys.exit(1)
    main_path = find_main(positional[0])
    if not main_path:
        print(f"No main .tex found under {positional[0]}"); sys.exit(1)

    rows = flatten(main_path)
    hits = (lint(rows, only) + lint_abstract(rows, only) + lint_floats(rows, only)
            + lint_figures(rows, only) + lint_equations(rows, only)
            + lint_repeats(rows, only) + lint_misplaced(rows, only)
            + lint_note_headers(rows, only) + lint_unicode_dash(rows, only)
            + lint_subsection_count(rows, only) + lint_dup_caveat(rows, only)
            + lint_acronyms(rows, only) + lint_caption_restates(rows, only)
            + lint_lists(rows, only))
    hits.sort(key=lambda h: (h[0], h[1]))

    base = os.path.dirname(main_path)
    for fpath, lineno, cat, detail in hits:
        rel = os.path.relpath(fpath, base)
        print(f"{rel}:{lineno}: [{cat}] {detail}")

    counts = {}
    for _, _, cat, _ in hits:
        counts[cat] = counts.get(cat, 0) + 1
    print("\nSummary (heuristic — confirm every hit by reading):")
    for cat in ["abstract-math", "abstract-citation", "abstract-crossref",
                "long-caption", "figure-nowidth", "crowded-figure", "long-equation",
                "repeated-sentence", "misplaced-future-work",
                "note-header", "dup-caveat", "unicode-dash", "subsection-count",
                "acronym-first-use", "caption-restates-body", "list-abuse",
                "overclaim", "ai-voice", "semicolon", "long-sentence", "comma-heavy",
                "weasel", "transition"]:
        if counts.get(cat):
            print(f"  {cat:<14} {counts[cat]}")
    if not hits:
        print("  no hits")


if __name__ == "__main__":
    main()
