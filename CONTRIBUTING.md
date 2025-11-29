## Contributing

Thanks for helping improve this repository. A few quick notes to keep binary files safe and the repo healthy.

1) Git LFS (recommended for large media)
- If you work with large images, videos, or design files, install Git LFS and track those types:

  ```powershell
  choco install git-lfs -y   # or install from https://git-lfs.github.com/
  git lfs install
  git lfs track "*.mp4"
  git lfs track "*.mov"
  git lfs track "*.psd"
  git add .gitattributes
  git commit -m "chore: track large media with Git LFS"
  ```

- Note: migrating already-committed files into LFS rewrites history; coordinate with maintainers before doing so.

2) EOL / CRLF handling (Windows)
- To avoid accidental corruption of binary files, prefer disabling automatic CRLF conversions and let `.gitattributes` control handling:

  ```powershell
  git config --global core.autocrlf false
  ```

- This repository includes a conservative `.gitattributes` that marks common binary extensions with `-text` to prevent EOL conversion.

3) Commit hygiene
- Don’t edit binary files in text editors. If you must change large binaries, consider using Git LFS and file locking.
- Run the link-checker before opening PRs:

  ```powershell
  python scripts/check_links.py
  ```

4) Integrity checks
- If you suspect a corrupt object locally, use:

  ```powershell
  git fsck --full
  ```

5) Questions or migrations
- If you want to move existing large files to LFS or change repository policies, open an issue or discuss in a PR so we can coordinate history-rewrite steps.

Thanks — small precautions above keep binary assets safe and the repo fast for everyone.
