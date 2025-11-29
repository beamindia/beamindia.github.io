"""
Reindent HTML files under a target directory while preserving content.
Creates a backup copy of each file before modifying.

Usage: python scripts/reindent_html.py --target ../ 

This script tries to use lxml for pretty printing; if not available it falls back to BeautifulSoup.
It only changes tag/line indentation; textual content, attributes, and asset paths are preserved.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys


def format_with_lxml(html_text: str) -> str:
    try:
        from lxml import etree, html
    except Exception:
        raise
    parser = html.HTMLParser(remove_blank_text=True)
    try:
        doc = html.fromstring(html_text, parser=parser)
        formatted = etree.tostring(doc, pretty_print=True, method="html", encoding="unicode")
        return formatted
    except Exception:
        # fallback: return original
        return html_text


def format_with_bs4(html_text: str) -> str:
    try:
        from bs4 import BeautifulSoup
    except Exception:
        raise
    soup = BeautifulSoup(html_text, "html.parser")
    # BeautifulSoup.prettify may add extra newlines; use it as last resort
    return soup.prettify()


def reindent_file(path: Path, use: str) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        if use == 'lxml':
            new = format_with_lxml(text)
        else:
            new = format_with_bs4(text)
    except Exception:
        # if formatting fails, do not overwrite
        return False
    # Normalize final newline
    if not new.endswith('\n'):
        new = new + '\n'
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def find_formatter() -> str:
    try:
        import lxml  # type: ignore
        return 'lxml'
    except Exception:
        try:
            import bs4  # type: ignore
            return 'bs4'
        except Exception:
            return ''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", default=".", help="Target directory to scan for .html files")
    p.add_argument("--backup-dir", default=".html_backups", help="Directory to store backups")
    args = p.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Target {target} does not exist", file=sys.stderr)
        sys.exit(2)

    backup_root = target / args.backup_dir
    backup_root.mkdir(parents=True, exist_ok=True)

    formatter = find_formatter()
    if not formatter:
        print("Neither lxml nor bs4 (BeautifulSoup) is installed. Please install one (pip install lxml or bs4).", file=sys.stderr)
        sys.exit(3)

    print(f"Using formatter: {formatter}")

    html_files = list(target.rglob("*.html"))
    modified = []
    for f in html_files:
        rel = f.relative_to(target)
        backup_path = backup_root / rel
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, backup_path)
        ok = reindent_file(f, formatter)
        if ok:
            modified.append(str(rel))
            print(f"Reformatted: {rel}")
        else:
            print(f"Unchanged:   {rel}")

    print(f"Done. Reformatted {len(modified)} files. Backups in {backup_root}")

if __name__ == '__main__':
    main()
