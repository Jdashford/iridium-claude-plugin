# Iridium for Claude

This is the public Claude plugin marketplace for Iridium. The **Iridium Memory** plugin gives Claude secure access to the signed-in person's assigned Iridium agents and their authorised Memory and Knowledge.

The plugin contains presentation and routing guidance only. It does not contain customer memories, Knowledge documents, prompts, credentials, OAuth tokens, account names, or fixed agent names.

## Install in Claude

1. Open **Customize** → **Plugins** in Claude.
2. Choose **Add** → **Add marketplace**.
3. Enter `Jdashford/iridium-claude-plugin` or this repository URL and choose **Sync**.
4. Install **Iridium Memory** from the marketplace.
5. Open its connector, choose **Connect**, and sign in with your Iridium account.
6. Start a new Claude conversation after the Iridium tools have loaded.

Iridium Memory uses the Claude MCP resource:

`https://mcp.iridiumai.co/mcp/v26`

### Already using the previous Iridium plugin?

The previous **Iridium** plugin (`iridium-claude`) stays in this marketplace and keeps working against its existing resource:

`https://iridium-public-plugin-production.up.railway.app/mcp/v23`

To move to Iridium Memory, install it, connect it once, and then remove the previous plugin so Claude shows one set of Iridium tools.

## Download the latest plugin

The marketplace is the recommended installation path because Claude can keep
the plugin synchronized from this repository. Correctly rooted installable
ZIPs are also published with every release:

`https://github.com/Jdashford/iridium-claude-plugin/releases/latest/download/iridium-memory.zip`

The previous plugin remains available at:

`https://github.com/Jdashford/iridium-claude-plugin/releases/latest/download/iridium-claude.zip`

In Claude, open **Customize** → **Plugins**, choose **Add** → **Upload plugin**,
and select the downloaded ZIP. The stable URLs always resolve to the latest
published plugin versions.

## Use it naturally

Iridium agent names are chosen by users and can be anything. Claude asks Iridium to resolve the name against the signed-in person's current assignments. The plugin is not tied to Iridium X or any other account: OAuth and the server-side assignment catalogue scope every request, including people who are authorised across multiple accounts.

Examples:

- "Ask my personal agent what it remembers about my role."
- "Ask Project Desk what we agreed on the last call."
- "What does my Iridium agent know about our product?"
- "Ask my personal agent to remember that the launch review is next Tuesday."

Claude also supports explicit skill commands. `/iridium-agent-memory [your request]` opens the agent picker when no agent is already selected. `/iridium-agent-memory use [exact agent name]: [your request]` routes directly. The selected agent remains in use for the conversation until the user changes it.

The plugin instructs Claude to retrieve broadly across authorised Memory and Knowledge, respect Iridium's continuation and sufficiency decisions, avoid exposing raw evidence packets, and save information only after an explicit request.

## Repository contents

- `.claude-plugin/marketplace.json` — the marketplace catalogue.
- `plugins/iridium-memory/` — the Iridium Memory plugin (manifest, MCP connection, skill, README).
- `plugins/iridium-claude/.claude-plugin/plugin.json` — the previous plugin's manifest.
- `plugins/iridium-claude/.mcp.json` — the authenticated Iridium MCP connection.
- `plugins/iridium-claude/skills/iridium-agent-memory/SKILL.md` — Claude-native routing, recall, continuation, presentation, and write guidance.
- `plugins/iridium-claude/resources/` — setup and privacy notes.

## Security

The public repository contains no secrets. Access is enforced by Iridium OAuth and the signed-in person's assignment catalogue. Read tools are non-mutating; durable writes require explicit user intent and an accepted Iridium receipt.

To remove access, disconnect Iridium in Claude or from the Iridium account connection page.
