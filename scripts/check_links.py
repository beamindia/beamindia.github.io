#!/usr/bin/env python3
"""
Lightweight link checker for the Beamindia static site.

Scans the `beamindia/` directory for HTML files, extracts href/src links,
and reports missing file targets and missing fragment (id) targets.

Usage: python scripts/check_links.py
"""
from pathlib import Path
import re
from urllib.parse import urlparse, unquote
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "beamindia"

HTML_RE = re.compile(r"(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]", re.I)
ID_RE_TEMPLATE = r"\bid\s*=\s*['\"]{anchor}['\"]|\bname\s*=\s*['\"]{anchor}['\"]"


def is_external(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("mailto:")


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def normalize_path(from_file: Path, link_path: str) -> Path:
    # Remove query params and fragments beforehand if present
    p = unquote(link_path.split('?', 1)[0])
    parsed = urlparse(p)
    path = parsed.path
    if path.startswith('/'):
        return SITE_DIR / path.lstrip('/')
    return (from_file.parent / path).resolve()


def find_ids_in(html_text: str):
    ids = set()
    for m in re.finditer(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", html_text):
        ids.add(m.group(1))
    for m in re.finditer(r"\bname\s*=\s*['\"]([^'\"]+)['\"]", html_text):
        ids.add(m.group(1))
    return ids


def main():
    if not SITE_DIR.exists():
        print(f"ERROR: site directory not found: {SITE_DIR}")
        sys.exit(2)

    html_files = sorted(SITE_DIR.rglob("*.html"))
    missing_files = []
    missing_fragments = []
    checked = 0

    # cache ids for files we read
    id_cache = {}

    for hf in html_files:
        text = read_text(hf)
        ids = find_ids_in(text)
        id_cache[str(hf)] = ids

    for hf in html_files:
        text = read_text(hf)
        links = HTML_RE.findall(text)
        for link in links:
            if not link or is_external(link):
                continue
            checked += 1
            # same-page fragment
            if link.startswith('#'):
                anchor = link[1:]
                ids = id_cache.get(str(hf), set())
                if anchor and anchor not in ids:
                    missing_fragments.append((str(hf), link, f"missing id '{anchor}' in same file"))
                continue

            parsed = urlparse(link)
            path = unquote(parsed.path)
            fragment = parsed.fragment

            # If the path is empty but fragment present, same-page
            if (not path or path == '') and fragment:
                anchor = fragment
                ids = id_cache.get(str(hf), set())
                if anchor and anchor not in ids:
                    missing_fragments.append((str(hf), link, f"missing id '{anchor}' in same file (via empty path)"))
                continue

            target = normalize_path(hf, path)

            # try direct file
            if not target.exists():
                # try adding .html if no suffix
                if not target.suffix:
                    alt = Path(str(target) + '.html')
                    if alt.exists():
                        target = alt
                    else:
                        missing_files.append((str(hf), link, str(target)))
                        continue
                else:
                    missing_files.append((str(hf), link, str(target)))
                    continue

            # if fragment present, check id in target
            if fragment:
                ttext = read_text(target)
                tids = find_ids_in(ttext)
                if fragment not in tids:
                    missing_fragments.append((str(hf), link, f"fragment '{fragment}' not found in {target}"))

    # Print report
    print("Link check report for:", SITE_DIR)
    print(f"Checked {len(html_files)} HTML files, {checked} local links (skipped externals).\n")

    if missing_files:
        print("Missing file targets:")
        for src, link, target in missing_files:
            print(f"- In {src}: link '{link}' -> missing target {target}")
    else:
        print("No missing file targets found.")

    print()
    if missing_fragments:
        print("Missing fragment targets (ids):")
        for src, link, note in missing_fragments:
            print(f"- In {src}: link '{link}' -> {note}")
    else:
        print("No missing fragments found.")

    # exit code non-zero if issues
    if missing_files or missing_fragments:
        print('\nSummary: issues found.')
        sys.exit(1)
    else:
        print('\nSummary: no issues found.')
        sys.exit(0)


if __name__ == '__main__':
    main()
