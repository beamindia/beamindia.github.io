import os
import re
import sys

# ------------------------------------------------------------
# 1. Determine the repo root (one directory above /scripts/)
# ------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

print(f"Running from: {SCRIPT_DIR}")
print(f"Targeting repo root: {REPO_ROOT}")

os.chdir(REPO_ROOT)

# ------------------------------------------------------------
# 2. Delete old favicon in assets/ if it exists
# ------------------------------------------------------------
old_favicon_path = os.path.join(REPO_ROOT, "assets", "favicon.ico")
if os.path.exists(old_favicon_path):
    print(f"Removing old favicon: {old_favicon_path}")
    os.remove(old_favicon_path)
else:
    print("No old assets/favicon.ico found. Skipping removal.")

# ------------------------------------------------------------
# 3. Favicon block to inject
# ------------------------------------------------------------
FAVICON_BLOCK = """
    <!-- FAVICONS (BeamIndia) -->
    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
    <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
    <link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
    <link rel="icon" type="image/png" sizes="128x128" href="/favicon-128.png">
    <link rel="icon" type="image/png" sizes="256x256" href="/favicon-256.png">
"""

# ------------------------------------------------------------
# 4. Regex to remove old favicon link tags
# ------------------------------------------------------------
FAVICON_LINK_RE = re.compile(
    r'\s*<link[^>]+rel=["\'](?:shortcut icon|icon)["\'][^>]*>\s*',
    re.IGNORECASE
)

# ------------------------------------------------------------
# 5. Update a single HTML file
# ------------------------------------------------------------
def process_html_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already injected
    if "<!-- FAVICONS (BeamIndia) -->" in content:
        print(f"[SKIP] Already updated: {path}")
        return

    original = content

    # Remove existing icon tags
    content = FAVICON_LINK_RE.sub("", content)

    # Find closing </head>
    lower = content.lower()
    head_close_idx = lower.find("</head>")

    if head_close_idx == -1:
        print(f"[WARN] No </head> tag: {path}")
        return

    new_content = (
        content[:head_close_idx]
        + FAVICON_BLOCK
        + "\n"
        + content[head_close_idx:]
    )

    if new_content != original:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        print(f"[OK] Updated: {path}")
    else:
        print(f"[NO CHANGE] {path}")


# ------------------------------------------------------------
# 6. Walk repo and update all HTML files
# ------------------------------------------------------------
def main():
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip the scripts directory itself
        if "scripts" in root:
            continue

        for name in files:
            if name.lower().endswith(".html"):
                path = os.path.join(root, name)
                process_html_file(path)

    print("Done.")

if __name__ == "__main__":
    main()
