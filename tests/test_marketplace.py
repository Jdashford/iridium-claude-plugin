import json
from pathlib import Path


CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")


def plugin_text_assets(root: Path) -> str:
    return "\n".join(
        path.read_text()
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".json", ".md"}
    )


def test_claude_marketplace_exposes_claude_plugin():
    marketplace = json.loads(Path(".claude-plugin/marketplace.json").read_text())

    assert marketplace["name"] == "iridium"
    assert marketplace["owner"]["name"] == "Iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-claude"}
    assert entries["iridium-claude"]["source"] == "./plugins/iridium-claude"
    assert entries["iridium-claude"]["description"] == (
        "Connect Claude Code to your private Iridium advisor memory."
    )
    assert entries["iridium-claude"]["category"] == "productivity"


def test_claude_plugin_points_to_claude_repository_and_gateway_without_private_data():
    manifest = json.loads((CLAUDE_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text())
    mcp = json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())
    all_text = plugin_text_assets(CLAUDE_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-claude"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-claude-plugin"
    assert "codex" not in manifest["repository"].lower()
    assert mcp["mcpServers"]["iridium"]["url"] == "https://connect.iridiumai.co/mcp"
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "connection code" not in all_text.lower()
    assert "client_secret" not in all_text
