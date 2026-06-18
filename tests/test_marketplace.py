import json
from pathlib import Path


CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")
CLAUDE_REPORTING_PLUGIN_ROOT = Path("plugins/iridium-reporting-claude")


def plugin_text_assets(root: Path) -> str:
    return "\n".join(
        path.read_text()
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".json", ".md"}
    )


def test_claude_marketplace_exposes_claude_plugins():
    marketplace = json.loads(Path(".claude-plugin/marketplace.json").read_text())

    assert marketplace["name"] == "iridium-claude"
    assert marketplace["owner"]["name"] == "Iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-claude", "iridium-reporting-claude"}
    assert entries["iridium-claude"]["source"] == "./plugins/iridium-claude"
    assert entries["iridium-claude"]["description"] == (
        "Connect Claude Code to your private Iridium advisor memory."
    )
    assert entries["iridium-claude"]["category"] == "productivity"
    assert entries["iridium-reporting-claude"]["source"] == (
        "./plugins/iridium-reporting-claude"
    )
    assert entries["iridium-reporting-claude"]["description"] == (
        "Connect Claude Code to Iridium business reporting for an account."
    )
    assert entries["iridium-reporting-claude"]["category"] == "productivity"


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


def test_claude_reporting_plugin_points_to_claude_repository_and_gateway_without_private_data():
    manifest = json.loads((CLAUDE_REPORTING_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text())
    mcp = json.loads((CLAUDE_REPORTING_PLUGIN_ROOT / ".mcp.json").read_text())
    skill = (CLAUDE_REPORTING_PLUGIN_ROOT / "skills/iridium-reporting/SKILL.md").read_text()
    all_text = plugin_text_assets(CLAUDE_REPORTING_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-reporting-claude"
    assert manifest["repository"] == "https://github.com/Jdashford/iridium-claude-plugin"
    assert "codex" not in manifest["repository"].lower()
    assert mcp["mcpServers"]["iridium_reporting"]["url"] == "https://connect.iridiumai.co/mcp"
    assert mcp["mcpServers"]["iridium_reporting"]["type"] == "http"
    assert "resolve_reporting_scope" in skill
    assert "ask_business_report" in skill
    assert "prepare_business_report_context" in skill
    assert "ask_advisor" not in skill
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "Railway" not in all_text
    assert "up.railway.app" not in all_text
    assert "connection code" not in all_text.lower()
    assert "client_secret" not in all_text
