#!/usr/bin/env python3
"""outline.py — print the structure tree of a LaTeX manuscript and a bottom-up traversal plan.

Best-effort, standard-library only. It exists to help the workflow *divide the work*, not to
judge anything. Read every sentence yourself; use this only to plan.

Usage:
    python outline.py path/to/main.tex
    python outline.py path/to/project_dir        # auto-detects the main file

What it does:
    - finds the main file (the one with \\documentclass / \\begin{document}) when given a dir
    - follows \\input{...} and \\include{...} in reading order
    - strips comments (text after an unescaped %)
    - reports \\section / \\subsection / \\subsubsection with file:line and word counts
    - approximates paragraph counts inside the deepest units (blank-line-separated blocks,
      skipping equation/figure/table/algorithm environments)
    - prints the leaf units in document order as the bottom-up traversal plan
"""

import os
import re
import sys

SECTION_LEVELS = {"section": 0, "subsection": 1, "subsubsection": 2}
SEC_RE = re.compile(r"\\(sub)*section\*?\s*\{")
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
SKIP_ENVS = {"equation", "align", "gather", "multline", "eqnarray", "figure", "figure*",
             "table", "table*", "algorithm", "algorithmic", "verbatim", "lstlisting",
             "tikzpicture", "tabular"}
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
END_RE = re.compile(r"\\end\{([^}]+)\}")
# lines that carry no prose and must not be counted as a paragraph
NOCOUNT_RE = re.compile(
    r"\\(?:bibliography|bibliographystyle|label|maketitle|title|author|appendix|"
    r"appendices|newpage|clearpage|vspace|hspace|centering|includegraphics|"
    r"bstctlcite|newcommand|def|input|include)\b")


def strip_comment(line):
    """Remove a LaTeX comment: everything after an unescaped %."""
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


def resolve(path, base):
    """Resolve an \\input target to an existing .tex path, relative to base dir."""
    for cand in (path, path + ".tex"):
        p = cand if os.path.isabs(cand) else os.path.join(base, cand)
        if os.path.isfile(p):
            return p
    return None


def flatten(main_path, seen=None):
    """Return a list of (file, lineno, text) with comments stripped, inputs inlined."""
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
                        rows.extend(flatten(target, seen))
                        continue
                rows.append((main_path, lineno, text))
    except OSError as exc:
        print(f"  (could not read {main_path}: {exc})", file=sys.stderr)
    return rows


def find_main(path):
    if os.path.isfile(path):
        return path
    best = None
    for root, _dirs, files in os.walk(path):
        for name in files:
            if not name.endswith(".tex"):
                continue
            full = os.path.join(root, name)
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as fh:
                    head = fh.read(8000)
            except OSError:
                continue
            if "\\begin{document}" in head or "\\documentclass" in head:
                # prefer the shallowest such file
                if best is None or full.count(os.sep) < best.count(os.sep):
                    best = full
    return best


def level_of(text):
    m = SEC_RE.match(text.strip())
    if not m:
        return None
    name = re.match(r"\\((?:sub)*section)", text.strip()).group(1)
    return name


def title_of(text):
    idx = text.find("{")
    if idx < 0:
        return ""
    depth = 0
    out = []
    for c in text[idx:]:
        if c == "{":
            depth += 1
            if depth == 1:
                continue
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        out.append(c)
    return "".join(out).strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    target = sys.argv[1]
    main_path = find_main(target)
    if not main_path:
        print(f"No main .tex found under {target}")
        sys.exit(1)
    print(f"Main file: {main_path}\n")

    rows = flatten(main_path)

    # Walk, tracking the section stack, environment depth, and paragraph blocks.
    headings = []          # (level_name, title, file, lineno)
    units = []             # leaf units: dict(level, title, file, line, words, paragraphs)
    env_stack = []
    cur = None
    words = 0
    para_open = False
    paras = 0

    def close_unit():
        nonlocal cur, words, paras, para_open
        if cur is not None:
            cur["words"] = words
            cur["paragraphs"] = paras
            units.append(cur)
        cur = None
        words = 0
        paras = 0
        para_open = False

    started = False
    for fpath, lineno, text in rows:
        if "\\begin{document}" in text:
            started = True
            continue
        if not started:
            continue
        if "\\end{document}" in text:
            break

        # The abstract is a first-class unit (often the worst overclaim offender), even
        # though it is not a \section. Treat it as a top-level leaf.
        if "\\begin{abstract}" in text:
            close_unit()
            cur = {"level": "abstract", "title": "Abstract", "file": fpath,
                   "line": lineno, "words": 0, "paragraphs": 0}
            continue
        if "\\end{abstract}" in text:
            close_unit()
            continue

        lname = level_of(text)
        if lname:
            close_unit()
            title = title_of(text)
            headings.append((lname, title, fpath, lineno))
            cur = {"level": lname, "title": title, "file": fpath, "line": lineno,
                   "words": 0, "paragraphs": 0}
            continue

        for m in BEGIN_RE.finditer(text):
            env_stack.append(m.group(1))
        skipping = any(e in SKIP_ENVS for e in env_stack)
        for m in END_RE.finditer(text):
            if env_stack and env_stack[-1] == m.group(1):
                env_stack.pop()

        stripped = text.strip()
        if not skipping and cur is not None:
            if stripped == "" or NOCOUNT_RE.match(stripped):
                para_open = False
            else:
                if not para_open:
                    paras += 1
                    para_open = True
                words += len(re.findall(r"[A-Za-z][A-Za-z\-']+", stripped))
    close_unit()

    if not units:
        print("No abstract or \\section headings found. Is this the right file?")
        return

    # Print the tree.
    print("Structure tree (level: title  [file:line]  ~words, ~paragraphs)\n")
    indent = {"section": "", "subsection": "  ", "subsubsection": "    "}
    for u in units:
        rel = os.path.relpath(u["file"], os.path.dirname(main_path))
        pad = indent.get(u["level"], "")
        print(f"{pad}{u['level']}: {u['title'][:70]}")
        print(f"{pad}    [{rel}:{u['line']}]  ~{u['words']} words, ~{u['paragraphs']} paragraphs")

    # Bottom-up traversal plan. A sectioning unit is a "container" when the next unit is a
    # deeper section level (it has children); otherwise it is a "leaf" you polish directly.
    # The abstract and other non-sectioning units are always leaves.
    def is_container(i):
        if i + 1 >= len(units):
            return False
        cur_l, nxt_l = units[i]["level"], units[i + 1]["level"]
        if cur_l not in SECTION_LEVELS or nxt_l not in SECTION_LEVELS:
            return False
        return SECTION_LEVELS[nxt_l] > SECTION_LEVELS[cur_l]

    print("\nBottom-up traversal plan")
    print("Polish each LEAF first (sentence pass + paragraph re-read). Then re-read each")
    print("CONTAINER after its children, rising subsection -> section -> whole manuscript.\n")
    for i, u in enumerate(units):
        kind = "container" if is_container(i) else "leaf"
        rel = os.path.relpath(u["file"], os.path.dirname(main_path))
        print(f"  {i + 1:3d}. [{kind:<9}] {u['level']:<14} {u['title'][:44]:<44} "
              f"[{rel}:{u['line']}] ~{u['paragraphs']}p")
    total_words = sum(u["words"] for u in units)
    n_leaf = sum(1 for i in range(len(units)) if not is_container(i))
    print(f"\nTotals: {len(units)} units ({n_leaf} leaves), ~{total_words} words.")


if __name__ == "__main__":
    main()
