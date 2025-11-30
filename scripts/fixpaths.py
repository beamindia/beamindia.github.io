import os
import re

# Matches href="/something" or src="/something"
# and removes the leading slash from the value.
pattern = re.compile(
    r'(?P<attr>href|src)(?P<ws>\s*=\s*")/(?P<path>[^"]*)"'
)

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content, count = pattern.subn(
        r'\g<attr>\g<ws>\g<path>"', content
    )

    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return count

def main():
    root = os.getcwd()
    total_changes = 0

    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                changed = fix_file(full_path)
                if changed:
                    rel = os.path.relpath(full_path, root)
                    print(f"Updated {rel} ({changed} occurrence(s))")
                    total_changes += changed

    if total_changes == 0:
        print("No href/src paths starting with '/' were found.")
    else:
        print(f"\nDone. Total replacements: {total_changes}")

if __name__ == "__main__":
    main()
