#!/usr/bin/env python3
"""Build an installable Iridium Claude plugin archive.

Usage: build_plugin_archive.py [output.zip] [plugin-name]
The plugin name defaults to iridium-claude.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_MANIFEST = REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json"
DEFAULT_PLUGIN = "iridium-claude"


def read_version(path: Path) -> str:
    return str(json.loads(path.read_text())["version"])


def build_archive(output: Path, plugin_name: str = DEFAULT_PLUGIN) -> str:
    plugin_root = REPOSITORY_ROOT / "plugins" / plugin_name
    plugin_manifest = plugin_root / ".claude-plugin" / "plugin.json"
    archive_root = Path(plugin_name)
    plugin_version = read_version(plugin_manifest)
    marketplace = json.loads(MARKETPLACE_MANIFEST.read_text())
    entry = next(
        (item for item in marketplace["plugins"] if item["name"] == plugin_name),
        None,
    )
    if entry is None:
        raise ValueError(f"{plugin_name} is not listed in the marketplace")
    if plugin_version != str(entry["version"]):
        raise ValueError("Plugin and marketplace versions must match before packaging")

    files = sorted(path for path in plugin_root.rglob("*") if path.is_file())
    if plugin_manifest not in files:
        raise ValueError("Claude plugin manifest is missing")

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive_path = archive_root / path.relative_to(plugin_root)
            info = ZipInfo(str(archive_path), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    with ZipFile(output) as archive:
        required_manifest = str(archive_root / ".claude-plugin" / "plugin.json")
        if required_manifest not in archive.namelist():
            raise ValueError(
                "Archive does not contain the Claude manifest at its valid root"
            )

    return plugin_version


def main() -> None:
    plugin_name = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PLUGIN
    output = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else REPOSITORY_ROOT / "dist" / f"{plugin_name}.zip"
    )
    version = build_archive(output, plugin_name)
    print(f"Built {plugin_name} {version}: {output}")


if __name__ == "__main__":
    main()
