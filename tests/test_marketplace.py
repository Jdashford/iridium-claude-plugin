import json
from pathlib import Path


CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")
CLAUDE_MCP_URL = (
    "https://iridium-public-plugin-production.up.railway.app/mcp/v23"
)


def plugin_text_assets(root: Path) -> str:
    return "\n".join(
        path.read_text()
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".json", ".md"}
    )


def test_marketplace_exposes_one_current_iridium_plugin():
    marketplace = json.loads(Path(".claude-plugin/marketplace.json").read_text())

    assert marketplace["name"] == "iridium-claude"
    assert marketplace["owner"]["name"] == "Iridium"
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    assert set(entries) == {"iridium-claude"}
    assert entries["iridium-claude"]["source"] == "./plugins/iridium-claude"
    assert entries["iridium-claude"]["description"] == (
        "Give Claude secure access to your assigned Iridium agents and their "
        "authorised Memory and Knowledge."
    )
    assert entries["iridium-claude"]["category"] == "productivity"
    assert entries["iridium-claude"]["version"] == "2.0.0"
    assert entries["iridium-claude"]["homepage"] == "https://iridiumai.co"


def test_plugin_uses_the_current_claude_endpoint_without_private_data():
    manifest = json.loads(
        (CLAUDE_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text()
    )
    mcp = json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())
    all_text = plugin_text_assets(CLAUDE_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-claude"
    assert manifest["version"] == "2.0.0"
    assert manifest["repository"] == (
        "https://github.com/Jdashford/iridium-claude-plugin"
    )
    assert manifest["homepage"] == "https://iridiumai.co"
    assert "codex" not in manifest["repository"].lower()
    assert mcp == {
        "mcpServers": {
            "iridium": {
                "type": "http",
                "url": CLAUDE_MCP_URL,
            }
        }
    }
    assert "connect.iridium.ai" not in all_text
    assert "https://iridium.ai" not in all_text
    assert "connect.iridiumai.co/mcp" not in all_text
    assert "one-time setup code" not in all_text.lower()
    assert "client_secret" not in all_text


def test_skill_covers_natural_routing_recall_and_explicit_writes():
    skill = (
        CLAUDE_PLUGIN_ROOT / "skills/iridium-memory/SKILL.md"
    ).read_text()

    assert "name: iridium-memory" in skill
    assert "Claude Code" not in skill
    assert "`/mcp`" not in skill
    assert "delta" not in skill.lower()
    assert "Agent display names are chosen by users and may be anything" in skill
    assert "Never assume a built-in name" in skill
    assert "assignments in several Iridium accounts" in skill
    assert "If the same display name exists in more than one authorised account" in skill
    assert "ask_iridium_agent_by_name" in skill
    assert "start_unnamed_iridium_task" in skill
    assert "continue_iridium_picker_task" in skill
    assert "continue_selected_iridium_agent_recall" in skill
    assert "remember_with_personal_agent_by_name" in skill
    assert "save_with_selected_team_agent" in skill
    assert "complete substantive request" in skill
    assert "broad ranked Memory and Knowledge baseline" in skill
    assert "Never reduce retrieval breadth merely to shorten the response" in skill
    assert "structured context or evidence packet as a successful tool result" in skill
    assert "recall_next_action.action" in skill
    assert "insufficient_evidence" in skill
    assert "memory_write_pending" in skill
    assert "receipt_id" in skill
    assert "Reporting agents are read-only" in skill
    assert 'Do not describe stateless routing as "connecting to" an agent' in skill


def test_readme_documents_the_github_marketplace_install_path():
    readme = Path("README.md").read_text()

    assert "**Add** → **Add marketplace**" in readme
    assert "Jdashford/iridium-claude-plugin" in readme
    assert CLAUDE_MCP_URL in readme
    assert "fixed agent names" in readme
    assert "legacy" not in readme.lower()


def test_no_retired_plugin_or_skill_is_shipped():
    assert not any(
        path.is_file()
        for path in Path("plugins/iridium-reporting-claude").rglob("*")
    )
    assert not (
        CLAUDE_PLUGIN_ROOT / "skills/iridium-advisor/SKILL.md"
    ).exists()
