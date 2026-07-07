#!/usr/bin/env python3
"""bib_check.py — citation-integrity and .bib risk scan.

Standard-library only. Heuristic; confirm findings by reading and by compiling.

Usage:
    python bib_check.py path/to/project_dir
    python bib_check.py path/to/main.tex

Reports:
    - \\cite keys with no matching .bib entry  (cited-but-missing -> undefined references)
    - .bib entries never cited                 (uncited -> author decides keep/cite/remove)
    - duplicate entry keys
    - titles lacking outer-brace protection     (may lose Title Case under IEEE .bst)
    - bibliography system (BibTeX+bst / biblatex)
    - whether repeated-author dashes are disabled
"""

import os
import re
import sys

CITE_RE = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\s*\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
BIBSTYLE_RE = re.compile(r"\\bibliographystyle\s*\{([^}]+)\}")
BIBLATEX_RE = re.compile(r"\\(?:usepackage|RequirePackage)\s*(\[[^\]]*\])?\s*\{[^}]*biblatex[^}]*\}")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def gather(target, ext):
    if os.path.isfile(target):
        if target.endswith(ext):
            return [target]
        base = os.path.dirname(target)
    else:
        base = target
    out = []
    for root, _d, files in os.walk(base):
        for name in files:
            if name.endswith(ext):
                out.append(os.path.join(root, name))
    return out


def matching_brace(s, i):
    """Index of the brace matching s[i]=='{', or -1."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    return -1


def field_value(entry, field):
    """Return the raw value string of a field (contents of its {...} or "..."), or None."""
    m = re.search(r"\b" + field + r"\s*=\s*", entry, re.IGNORECASE)
    if not m:
        return None
    k = m.end()
    if k >= len(entry):
        return None
    if entry[k] == "{":
        end = matching_brace(entry, k)
        return entry[k + 1:end] if end > k else None
    if entry[k] == '"':
        end = entry.find('"', k + 1)
        return entry[k + 1:end] if end > k else None
    return None


def is_fully_braced(value):
    v = value.strip()
    if not v.startswith("{"):
        return False
    return matching_brace(v, 0) == len(v) - 1


def parse_entries(bib_text):
    """Yield (type, key, raw_entry_body)."""
    for m in ENTRY_RE.finditer(bib_text):
        etype, key = m.group(1), m.group(2)
        open_brace = bib_text.find("{", m.start())
        end = matching_brace(bib_text, open_brace)
        body = bib_text[open_brace + 1:end] if end > 0 else ""
        yield etype.lower(), key, body


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    target = sys.argv[1]

    tex_files = gather(target, ".tex")
    bib_files = gather(target, ".bib")
    if not tex_files:
        print(f"No .tex files under {target}"); sys.exit(1)

    tex_all = "\n".join(read(f) for f in tex_files)

    cited = set()
    for m in CITE_RE.finditer(tex_all):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                cited.add(key)

    defined = {}
    duplicates = []
    title_risks = []
    control_key_present = False
    for bib in bib_files:
        text = read(bib)
        for etype, key, body in parse_entries(text):
            if etype == "ieeetranbstctl":
                control_key_present = True
                continue
            if key in defined:
                duplicates.append(key)
            defined[key] = bib
            title = field_value(body, "title")
            if title is not None and not is_fully_braced(title):
                title_risks.append((os.path.basename(bib), key, title[:60]))

    missing = sorted(k for k in cited if k not in defined and k != "IEEEexample:BSTcontrol")
    uncited = sorted(k for k in defined if k not in cited)

    # bibliography system + dash config
    bststyle = BIBSTYLE_RE.search(tex_all)
    biblatex = BIBLATEX_RE.search(tex_all)
    system = "unknown"
    if biblatex:
        system = "biblatex"
    elif bststyle:
        system = f"BibTeX + {bststyle.group(1)}"

    dash_ok = None
    if system == "biblatex":
        opts = biblatex.group(1) or ""
        dash_ok = "dashed=false" in opts.replace(" ", "")
    elif bststyle and "ieeetran" in bststyle.group(1).lower():
        has_ctl_entry = control_key_present or "@IEEEtranBSTCTL" in "".join(read(b) for b in bib_files)
        has_cite = "\\bstctlcite" in tex_all
        dash_ok = has_ctl_entry and has_cite

    # ---- report ----
    print("=== Citation integrity ===")
    print(f"cite keys used: {len(cited)}   .bib entries: {len(defined)}   .bib files: {len(bib_files)}")
    print(f"\ncited-but-MISSING ({len(missing)}):")
    for k in missing:
        print(f"  - {k}")
    print(f"\nduplicate keys ({len(set(duplicates))}):")
    for k in sorted(set(duplicates)):
        print(f"  - {k}")
    print(f"\nuncited entries ({len(uncited)}):")
    for k in uncited:
        print(f"  - {k}")

    print("\n=== Title-case protection ===")
    print(f"titles WITHOUT outer-brace wrap ({len(title_risks)}) — consider {{...}} if the")
    print("venue prints Title Case and the style lowercases titles:")
    for bibname, key, snippet in title_risks:
        print(f"  - [{bibname}] {key}: {snippet}")

    print("\n=== Bibliography system ===")
    print(f"system: {system}")
    if dash_ok is None:
        print("repeated-author dashes: could not determine automatically")
    elif dash_ok:
        print("repeated-author dashes: DISABLED (good)")
    else:
        print("repeated-author dashes: NOT disabled — add the config (see references/bibliography.md)")


if __name__ == "__main__":
    main()
