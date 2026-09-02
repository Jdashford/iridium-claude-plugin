#!/usr/bin/env python3
"""Build the installable Iridium Claude plugin archive."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins" / "iridium-claude"
MARKETPLACE_MANIFEST = REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
ARCHIVE_ROOT = Path("iridium-claude")


def read_version(path: Path) -> str:
    return str(json.loads(path.read_text())["version"])


def build_archive(output: Path) -> str:
    plugin_version = read_version(PLUGIN_MANIFEST)
    marketplace = json.loads(MARKETPLACE_MANIFEST.read_text())
    marketplace_version = str(marketplace["plugins"][0]["version"])

    if plugin_version != marketplace_version:
        raise ValueError("Plugin and marketplace versions must match before packaging")

    files = sorted(path for path in PLUGIN_ROOT.rglob("*") if path.is_file())
    if PLUGIN_MANIFEST not in files:
        raise ValueError("Claude plugin manifest is missing")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive_path = ARCHIVE_ROOT / path.relative_to(PLUGIN_ROOT)
            info = ZipInfo(str(archive_path), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    with ZipFile(output) as archive:
        required_manifest = str(ARCHIVE_ROOT / ".claude-plugin" / "plugin.json")
        if required_manifest not in archive.namelist():
            raise ValueError(
                "Archive does not contain the Claude manifest at its valid root"
            )

    return plugin_version


def main() -> None:
    output = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else REPOSITORY_ROOT / "dist" / "iridium-claude.zip"
    )
    version = build_archive(output)
    print(f"Built Iridium Claude plugin {version}: {output}")


if __name__ == "__main__":
    main()
