# Iridium Reporting for Claude

Install this plugin from the Iridium Claude marketplace.

The plugin connects Claude Code to the Iridium Reporting MCP server at `https://connect.iridiumai.co/mcp`. Claude Code handles the browser sign-in flow. When Iridium asks you to sign in, reveal the one-time setup code on your private Iridium setup page and paste it only into the Iridium sign-in screen.

After authentication, start a new Claude Code session or run `/reload-plugins`. Ask: "Use Iridium Reporting to prepare a business update for this account."

If Claude Code shows the Iridium Reporting server as not authenticated, open `/mcp`, select `iridium_reporting`, and choose Authenticate.
