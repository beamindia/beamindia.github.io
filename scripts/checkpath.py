import os
import re

# Attributes we want to check for leading-slash paths
ATTRS = ("href", "src", "action")

# Regex: href="/something", src="/something", action="/something"
pattern = re.compile(
    r'(?P<attr>' + "|".join(ATTRS) + r')\s*=\s*"(?P<value>/[^"]*)"'
)

def check_file(path):
    issues = []
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for m in pattern.finditer(line):
                attr = m.group("attr")
                value = m.group("value")

                # You *might* want to allow protocol-relative URLs like //cdn...
                # If so, skip those here:
                if value.startswith("//"):
                    continue

                issues.append((lineno, attr, value, line.rstrip("\n")))
    return issues

def main():
    root = os.getcwd()
    total_issues = 0

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(".html"):
                full_path = os.path.join(dirpath, filename)
                issues = check_file(full_path)
                if issues:
                    rel = os.path.relpath(full_path, root)
                    print(f"\n🔍 {rel}")
                    for lineno, attr, value, line in issues:
                        print(f"  Line {lineno}: {attr}=\"{value}\"")
                        print(f"    {line}")
                    total_issues += len(issues)

    if total_issues == 0:
        print("✅ All good: no href/src/action values starting with '/' were found.")
    else:
        print(f"\n⚠ Found {total_issues} leading-slash path issue(s). Fix and re-run.")

if __name__ == "__main__":
    main()
