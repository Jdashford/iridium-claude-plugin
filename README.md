# Iridium for Claude

This repository contains the Iridium plugin marketplace for Claude Code.

The plugins connect Claude Code to the Iridium gateway at `https://connect.iridiumai.co/mcp`. They do not contain customer Railway URLs, setup codes, OAuth tokens, private memories, uploaded documents, advisor prompts, or client names.

## Install

Add this GitHub repository as a Claude plugin marketplace, then install the plugin for your setup:

- `iridium-claude` for private advisor memory.
- `iridium-reporting-claude` for account-scoped business reporting.

After installation, Claude Code asks you to connect Iridium. Open the private setup page from your advisor, reveal the one-time setup code, and paste that code only on the Iridium sign-in screen.

If Claude Code shows the Iridium server as not authenticated, open `/mcp`, select `iridium`, and choose Authenticate. After authentication, start a new Claude Code session or run `/reload-plugins`.

## Contents

- `.claude-plugin/marketplace.json`: Claude plugin marketplace entries.
- `plugins/iridium-claude/.claude-plugin/plugin.json`: Claude plugin manifest.
- `plugins/iridium-claude/.mcp.json`: gateway MCP server configuration.
- `plugins/iridium-claude/skills/iridium-advisor/SKILL.md`: Claude Code skill guidance for advisor usage.
- `plugins/iridium-claude/resources/`: setup and privacy notes.
- `plugins/iridium-reporting-claude/.claude-plugin/plugin.json`: Claude reporting plugin manifest.
- `plugins/iridium-reporting-claude/.mcp.json`: gateway MCP server configuration.
- `plugins/iridium-reporting-claude/skills/iridium-reporting/SKILL.md`: Claude Code skill guidance for reporting usage.
- `plugins/iridium-reporting-claude/resources/`: setup and privacy notes.

## Security

The one-time setup code binds a Claude OAuth connection to the correct account runtime at the gateway. Runtime deployments remain separate and are reached only through authenticated, short-lived gateway service tokens.
