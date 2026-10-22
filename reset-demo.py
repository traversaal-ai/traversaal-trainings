"""First-time setup for the Sam Reed demo.

Creates the working folders inside advisor-followup/ and your own
advisor-followup/config.md from config.local.md (the fully local setting),
so a fresh clone runs with no connectors.

It never overwrites an existing config.md, and it never touches the
playbooks, the templates, team.md or the plugin. Sam's story itself is
played by journey.py.

Usage, from the repository root (macOS: python3 instead of python):
  python reset-demo.py
  python journey.py start
"""

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent / "advisor-followup"
FOLDERS = ["inbox", "outbox", "ledger", "households", "briefs", "client-files", "salesforce"]
CONFIG = ROOT / "config.md"
TEMPLATE = ROOT / "config.local.md"


def main():
    if not TEMPLATE.is_file():
        raise SystemExit(f"{TEMPLATE} not found. Run this from the repository folder.")

    created = []
    for name in FOLDERS:
        folder = ROOT / name
        if not folder.exists():
            folder.mkdir(parents=True)
            created.append(name)
    if created:
        print("Working folders created: " + ", ".join(created))
    else:
        print("Working folders: already present")

    if CONFIG.exists():
        print("config.md: already exists, left alone")
    else:
        shutil.copyfile(TEMPLATE, CONFIG)
        print("config.md: created from config.local.md (fully local setting)")

    print("Next: python journey.py start (macOS: python3)")


if __name__ == "__main__":
    main()
