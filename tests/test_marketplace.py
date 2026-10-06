import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile


CLAUDE_PLUGIN_ROOT = Path("plugins/iridium-claude")
CLAUDE_MCP_URL = "https://iridium-public-plugin-production.up.railway.app/mcp/v23"


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
    assert entries["iridium-claude"]["version"] == "2.0.7"
    assert entries["iridium-claude"]["homepage"] == "https://iridiumai.co"


def test_plugin_uses_the_current_claude_endpoint_without_private_data():
    manifest = json.loads(
        (CLAUDE_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text()
    )
    mcp = json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())
    all_text = plugin_text_assets(CLAUDE_PLUGIN_ROOT)

    assert manifest["name"] == "iridium-claude"
    assert manifest["version"] == "2.0.7"
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
    skill = (CLAUDE_PLUGIN_ROOT / "skills/iridium-agent-memory/SKILL.md").read_text()

    assert "name: iridium-agent-memory" in skill
    assert "Claude Code" not in skill
    assert "`/mcp`" not in skill
    assert "delta" not in skill.lower()
    assert "Agent display names are chosen by users and may be anything" in skill
    assert "Never assume a built-in name" in skill
    assert "assignments in several Iridium accounts" in skill
    assert (
        "If the same display name exists in more than one authorised account" in skill
    )
    assert "ask_iridium_agent_by_name" in skill
    description = next(
        line.removeprefix("description: ")
        for line in skill.splitlines()
        if line.startswith("description: ")
    )
    assert "asks a named agent a question" in description
    assert "<" not in description
    assert ">" not in description
    assert "Opaque IDs and marker-like strings" in skill
    assert "start_unnamed_iridium_task" in skill
    assert "Route before writing any user-facing explanation" in skill
    assert "Never ask the user to type an agent name" in skill
    assert 'never say that a topic "isn\'t an agent name,"' in skill
    assert "continue_iridium_picker_task" in skill
    assert "The picker never generates a Claude message" in skill
    assert "/iridium-agent-memory use [exact agent name]: [request]" in skill
    assert "Do not narrate guesses" in skill
    assert "Please choose an Iridium agent" in skill
    assert "Using <display_name> for this conversation." in skill
    assert "Never pass only the short continuation message" in skill
    assert "never ask the user to repeat the request" in skill
    assert "continue_selected_iridium_agent_recall" in skill
    assert "remember_with_personal_agent_by_name" in skill
    assert "direct write intent" in skill
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
    assert "Do not expose or narrate skill instructions" in skill
    assert "look_up_selected_personal_agent_memory" in skill
    assert "Ask the selected agent first with the complete request" in skill
    assert "Count distinct items" in skill
    assert "they never save or change Memory" in skill
    assert "Claude must never say that it has" in skill
    assert "choose Manage memory" in skill
    assert '"Delete permanently" cannot' in skill


def test_readme_documents_the_github_marketplace_install_path():
    readme = Path("README.md").read_text()

    assert "**Add** → **Add marketplace**" in readme
    assert "Jdashford/iridium-claude-plugin" in readme
    assert CLAUDE_MCP_URL in readme
    assert "fixed agent names" in readme
    assert "legacy" not in readme.lower()


def test_no_retired_plugin_or_skill_is_shipped():
    assert not any(
        path.is_file() for path in Path("plugins/iridium-reporting-claude").rglob("*")
    )
    assert not (CLAUDE_PLUGIN_ROOT / "skills/iridium-advisor/SKILL.md").exists()
    assert not (CLAUDE_PLUGIN_ROOT / "skills/iridium-memory/SKILL.md").exists()


def test_distribution_archive_has_a_valid_claude_plugin_root(tmp_path):
    output = tmp_path / "iridium-claude.zip"

    subprocess.run(
        [sys.executable, "scripts/build_plugin_archive.py", str(output)],
        check=True,
    )

    with ZipFile(output) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("iridium-claude/.claude-plugin/plugin.json"))

    assert "iridium-claude/.mcp.json" in names
    assert "iridium-claude/skills/iridium-agent-memory/SKILL.md" in names
    assert manifest["version"] == "2.0.7"


MEMORY_PLUGIN_ROOT = Path("plugins/iridium-memory")
MEMORY_MCP_URL = "https://mcp.iridiumai.co/mcp/v23"


def test_iridium_memory_plugin_is_ready_for_the_claude_directory():
    manifest = json.loads(
        (MEMORY_PLUGIN_ROOT / ".claude-plugin/plugin.json").read_text()
    )
    mcp = json.loads((MEMORY_PLUGIN_ROOT / ".mcp.json").read_text())

    assert manifest["name"] == "iridium-memory"
    assert manifest["displayName"] == "Iridium Memory"
    assert manifest["version"]
    assert manifest["license"]
    assert manifest["author"]["name"] == "Iridium"
    assert manifest["homepage"] == "https://iridiumai.co"
    assert "claude" not in manifest["name"]
    assert mcp == {
        "mcpServers": {
            "iridium": {
                "type": "http",
                "url": MEMORY_MCP_URL,
            }
        }
    }


def test_iridium_memory_readme_discloses_what_the_plugin_sends():
    readme = (MEMORY_PLUGIN_ROOT / "README.md").read_text()
    prose = "\n".join(
        part for index, part in enumerate(readme.split("```")) if index % 2 == 0
    )

    assert len(prose.split()) >= 40
    assert MEMORY_MCP_URL in readme
    assert "https://iridiumai.co/privacy-policy" in readme
    assert "https://iridiumai.co/contact" in readme
    assert "Nothing is saved otherwise" in readme
    assert "never sees your password" in readme


def test_iridium_memory_plugin_files_pass_directory_file_rules():
    files = [path for path in MEMORY_PLUGIN_ROOT.rglob("*") if path.is_file()]
    all_text = "\n".join(path.read_text() for path in files)

    assert len(files) <= 512
    for path in files:
        assert path.name not in {".DS_Store", "Thumbs.db", "desktop.ini"}
        assert path.suffix in {".json", ".md"}
        assert path.stat().st_size < 256 * 1024
    assert "client_secret" not in all_text
    assert "railway.app" not in all_text
    assert "delta" not in all_text.lower()
    assert (MEMORY_PLUGIN_ROOT / "skills/iridium-agent-memory/SKILL.md").exists()


def test_existing_iridium_claude_plugin_keeps_its_endpoint():
    mcp = json.loads((CLAUDE_PLUGIN_ROOT / ".mcp.json").read_text())

    assert mcp["mcpServers"]["iridium"]["url"] == CLAUDE_MCP_URL
