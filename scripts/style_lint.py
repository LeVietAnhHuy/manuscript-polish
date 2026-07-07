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
    misplaced-future-work  future-work wording outside a Conclusion/Discussion section
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
    text = re.sub(r"\$[^$]*\$", " MATH ", text)
    text = re.sub(r"\\\([^)]*\\\)", " MATH ", text)
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
            + lint_misplaced(rows, only))
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
                "long-caption", "figure-nowidth", "misplaced-future-work",
                "overclaim", "ai-voice", "semicolon", "long-sentence", "comma-heavy",
                "weasel", "transition"]:
        if counts.get(cat):
            print(f"  {cat:<14} {counts[cat]}")
    if not hits:
        print("  no hits")


if __name__ == "__main__":
    main()
