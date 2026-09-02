# Iridium for Claude

This is the public Claude plugin marketplace for Iridium. The **Iridium** plugin gives Claude secure access to the signed-in person's assigned Iridium agents and their authorised Memory and Knowledge.

The plugin contains presentation and routing guidance only. It does not contain customer memories, Knowledge documents, prompts, credentials, OAuth tokens, account names, or fixed agent names.

## Install in Claude

1. Open **Customize** → **Plugins** in Claude.
2. Choose **Add** → **Add marketplace**.
3. Enter `Jdashford/iridium-claude-plugin` or this repository URL and choose **Sync**.
4. Install **Iridium** from the marketplace.
5. Open its connector, choose **Connect**, and sign in with your Iridium account.
6. Start a new Claude conversation after the Iridium tools have loaded.

The plugin uses the current Claude MCP resource:

`https://iridium-public-plugin-production.up.railway.app/mcp/v23`

## Use it naturally

Iridium agent names are chosen by users and can be anything. Claude asks Iridium to resolve the name against the signed-in person's current assignments. The plugin is not tied to Iridium X or any other account: OAuth and the server-side assignment catalogue scope every request, including people who are authorised across multiple accounts.

Examples:

- "Ask my personal agent what it remembers about my role."
- "Ask Project Desk what we agreed on the last call."
- "What does my Iridium agent know about our product?"
- "Ask my personal agent to remember that the launch review is next Tuesday."

Claude also supports an explicit skill command: `/iridium-agent-memory use [exact agent name]: [your request]`. The exact user-defined agent name routes directly; an unnamed request opens the picker once and keeps the selected agent for the conversation.

The plugin instructs Claude to retrieve broadly across authorised Memory and Knowledge, respect Iridium's continuation and sufficiency decisions, avoid exposing raw evidence packets, and save information only after an explicit request.

## Repository contents

- `.claude-plugin/marketplace.json` — the marketplace catalogue.
- `plugins/iridium-claude/.claude-plugin/plugin.json` — the plugin manifest.
- `plugins/iridium-claude/.mcp.json` — the authenticated Iridium MCP connection.
- `plugins/iridium-claude/skills/iridium-agent-memory/SKILL.md` — Claude-native routing, recall, continuation, presentation, and write guidance.
- `plugins/iridium-claude/resources/` — setup and privacy notes.

## Security

The public repository contains no secrets. Access is enforced by Iridium OAuth and the signed-in person's assignment catalogue. Read tools are non-mutating; durable writes require explicit user intent and an accepted Iridium receipt.

To remove access, disconnect Iridium in Claude or from the Iridium account connection page.
